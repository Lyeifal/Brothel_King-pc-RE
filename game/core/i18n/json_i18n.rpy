## BK Evolution — JSON 国际化注册与辅助工具
##
## EN: Provides convention-based i18n registration for JSON data files.
##     All translatable text fields in JSON must use the `_i18n` suffix
##     (e.g. "name_i18n", "description_i18n").
##
## ZH: 为 JSON 数据文件提供基于约定的国际化注册。
##     JSON 中所有可翻译文本字段必须使用 `_i18n` 后缀（如 "name_i18n"、
##     "description_i18n"）。

init -3 python:
    import json, os, glob
    _builtins_dict = __import__('builtins').dict

    # =====================================================================
    # 1. 可翻译字段约定
    # =====================================================================

    # 约定：字段名以 _i18n 结尾即为可翻译文本。例如：
    #   "name_i18n": "Stolen underwear"
    #   "description_i18n": "So you're into these, eh?"

    # 已知不需要翻译的文件名后缀
    _I18N_SKIP_EXTS = (
        ".webp", ".png", ".jpg", ".jpeg",
        ".ogg", ".wav", ".mp3", ".mp4", ".webm",
    )

    # 已知不需要翻译的值前缀（代码片段、标识符等）
    _I18N_SKIP_PREFIXES = (
        "Effect(", "BK_", "img_", "IT_",
    )

    def _is_i18n_value(value):
        """EN: Check if a raw string value is likely translatable.
           ZH: 判断一个原始字符串值是否可能是可翻译文本。"""
        if not isinstance(value, (str, unicode)) or not value.strip():
            return False

        v = value.strip()

        # 跳过空字符串和单字符
        if len(v) <= 1:
            return False

        # 跳过图片/音频/视频路径
        if any(v.lower().endswith(ext) for ext in _I18N_SKIP_EXTS):
            return False

        # 跳过颜色代码 (#RGB / #RRGGBB / #AARRGGBB)
        if v.startswith("#") and len(v) in (4, 7, 9):
            # 额外检查是否全是 hex 字符
            hex_body = v[1:]
            if all(c in "0123456789ABCDEFabcdef" for c in hex_body):
                return False

        # 跳过纯数字（含小数和负数）
        try:
            float(v)
            return False
        except ValueError:
            pass

        # 跳过已知代码片段前缀
        if v.startswith(_I18N_SKIP_PREFIXES):
            return False

        # 跳过 Ren'Py 图片/音频标签
        if v.startswith(("{image=", "{sound=", "{movie=")):
            return False

        return True

    def _is_i18n_field(key, value):
        """EN: Check if a dict key/value pair represents translatable text.
           ZH: 判断一个字典键值对是否代表可翻译文本。"""
        if not _is_i18n_value(value):
            return False

        return key.endswith("_i18n")

    def _scan_i18n_strings(obj, collected, parent_key=None):
        """EN: Recursively scan a JSON object and collect translatable strings.
           ZH: 递归扫描 JSON 对象，收集所有可翻译字符串。"""
        if isinstance(obj, _builtins_dict):
            for key, value in obj.items():
                if _is_i18n_field(key, value):
                    collected.add(value)
                # 如果父字段以 _i18n 结尾（如 help_dict_i18n），其字典值也视为可翻译
                elif parent_key and parent_key.endswith("_i18n") and _is_i18n_value(value):
                    collected.add(value)
                _scan_i18n_strings(value, collected, key)
        elif isinstance(obj, list):
            # 对于列表，如果 parent_key 是可翻译字段，列表中的字符串也需要翻译
            for item in obj:
                if isinstance(item, (str, unicode)) and _is_i18n_field(parent_key, item):
                    collected.add(item)
                _scan_i18n_strings(item, collected, parent_key)

    def _register_json_translations():
        """EN: Walk all JSON data files and register translatable strings
               with Ren'Py's translation system. Called during init so that
               `generate translations` can pick them up at runtime.
           ZH: 遍历所有 JSON 数据文件，将可翻译字符串注册到 Ren'Py
               翻译系统。在 init 阶段调用，以便 `generate translations`
               能在运行时收集到它们。"""
        # Use __file__ to locate the data directory without depending on config
        i18n_dir = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(i18n_dir, "..", "data")
        json_dir = os.path.normpath(json_dir)

        # Fallback: try config.gamedir if the relative path doesn't exist
        if not os.path.isdir(json_dir):
            try:
                json_dir = os.path.join(config.gamedir, "core", "data")
                json_dir = os.path.normpath(json_dir)
            except Exception:
                pass

        collected = set()
        skip_patterns = (".schema.json", "_schemas")
        count_files = 0
        _dev_mode = False
        try:
            _dev_mode = config.developer
        except Exception:
            pass

        # Use os.walk for reliable recursive file discovery
        if os.path.isdir(json_dir):
            for root, dirs, files in os.walk(json_dir):
                for f in files:
                    if not f.endswith(".json"):
                        continue
                    jf = os.path.join(root, f)
                    if any(sp in jf for sp in skip_patterns):
                        continue
                    try:
                        with open(jf, "r", encoding="utf-8") as _f:
                            data = json.load(_f)
                            _scan_i18n_strings(data, collected)
                        del _f
                        count_files += 1
                    except Exception as e:
                        if _dev_mode:
                            print("[I18N] Warning: failed to scan %s — %s" % (jf, e))
        elif _dev_mode:
            print("[I18N] Warning: JSON data directory not found: %s" % json_dir)

        # 注册到 Ren'Py 翻译系统
        # 在 `generate translations` 运行时，这些调用会被记录
        for s in collected:
            try:
                __(s)
            except Exception:
                # 某些字符串在 init 阶段可能因上下文缺失而无法翻译，忽略
                pass

        if _dev_mode:
            print("[I18N] Scanned %d JSON files, registered %d translatable strings" % (count_files, len(collected)))

    # 立即执行注册
    _register_json_translations()


# =====================================================================
# 2. 运行时辅助函数
# =====================================================================

init python:
    def get_i18n(data, key, default=None):
        """EN: Get a translatable string from a dict.

            Priority:
              1. key + "_i18n"  (explicit i18n field)
              2. key            (fallback for legacy JSON)

            The returned string is passed through __() for runtime translation.

           ZH: 从字典中获取可翻译字符串。

            优先级：
              1. key + "_i18n"（明确的国际化字段）
              2. key（兼容旧版 JSON 的 fallback）

            返回值会通过 __() 进行运行时翻译。"""
        if not isinstance(data, _builtins_dict):
            return default

        # 模式 1：_i18n 后缀（推荐）
        i18n_key = key + "_i18n"
        if i18n_key in data:
            val = data[i18n_key]
            if isinstance(val, (str, unicode)):
                return __(val)
            return val

        # 模式 2：普通字段（兼容）
        if key in data:
            val = data[key]
            if isinstance(val, (str, unicode)):
                return __(val)
            return val

        return default

    def get_i18n_raw(data, key, default=None):
        """EN: Same as get_i18n() but does NOT wrap the result in __().
            Use this when you need the raw English string (e.g. for dict keys
            or achievement identifiers).
           ZH: 与 get_i18n() 相同，但不包裹 __()。
            在需要原始英文字符串时使用（例如字典 key 或成就标识符）。"""
        if not isinstance(data, _builtins_dict):
            return default

        i18n_key = key + "_i18n"
        if i18n_key in data:
            return data[i18n_key]
        if key in data:
            return data[key]
        return default


# =====================================================================
# 3. I18nMixin（可选，供 from_dict() 使用）
# =====================================================================

init python:
    class I18nMixin(object):
        """EN: Mixin that resolves _i18n suffixed fields during from_dict().

            Usage:
                class MyEntity(I18nMixin):
                    @classmethod
                    def from_dict(cls, data):
                        d = cls._resolve_i18n(data)
                        return cls(name=d["name"], description=d.get("description"))

           ZH: 在 from_dict() 中解析 _i18n 后缀字段的 Mixin。

            用法：
                class MyEntity(I18nMixin):
                    @classmethod
                    def from_dict(cls, data):
                        d = cls._resolve_i18n(data)
                        return cls(name=d["name"], description=d.get("description"))"""

        @classmethod
        def _resolve_i18n(cls, data):
            """EN: Return a new dict where _i18n fields take precedence
                   and are translated via __().
               ZH: 返回一个新字典，其中 _i18n 字段优先，并通过 __() 翻译。"""
            result = {}
            i18n_keys = set()

            # 第一遍：收集所有 _i18n 字段并翻译
            for key, value in data.items():
                if key.endswith("_i18n"):
                    base_key = key[:-5]
                    i18n_keys.add(base_key)
                    if isinstance(value, (str, unicode)):
                        result[base_key] = __(value)
                    else:
                        result[base_key] = value

            # 第二遍：填充非 _i18n 字段（不覆盖已被 _i18n 处理的）
            for key, value in data.items():
                if key in i18n_keys:
                    continue
                if key.endswith("_i18n"):
                    continue
                result[key] = value

            return result
