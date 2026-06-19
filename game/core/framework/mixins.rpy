################################################################################
## Mixins — Reusable behavior slices for BK Evolution
## EN: Common patterns extracted from classes.rpy, girlclass.rpy, farm.rpy, etc.
## ZH: 从 classes.rpy、girlclass.rpy、farm.rpy 等文件中提取的公共模式。
################################################################################

init -3 python:

    class EffectBearer(object):
        """EN: Provides get_effect / add_effects / remove_effects wrappers.
           ZH: 提供 get_effect / add_effects / remove_effects 包装方法。"""

        def get_effect(self, type, target, randomize=True):
            return get_effect(self, type, target, randomize=randomize)

        def add_effects(self, effects, apply_boost=False, spillover=False, expires=False):
            return add_effects(self, effects, apply_boost=apply_boost, spillover=spillover, expires=expires)

        def remove_effects(self, effects):
            remove_effects(self, effects)

    class PicHolder(object):
        """EN: Provides get_pic(x, y) for classes that store a self.pic Picture.
           ZH: 为持有 self.pic Picture 的类提供 get_pic(x, y)。"""

        def get_pic(self, x, y):
            return self.pic.get(x, y)

    class Trackable(object):
        """EN: Provides track(k, v=1) for defaultdict(int) tracking.
           Subclasses may override _on_track(k, v) for side effects.
           ZH: 为 defaultdict(int) 追踪提供 track(k, v=1)。
           子类可覆盖 _on_track(k, v) 以实现副作用。"""

        def track(self, k, v=1):
            self.track_dict[k] += v
            self._on_track(k, v)

        def _on_track(self, k, v):
            pass
