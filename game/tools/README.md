# Translation Tools - 使用说明

## 清理编译缓存

修改 `.rpy` 脚本后，Ren'Py 会自动重新编译生成 `.rpyc` 文件。但如果之前编译出错或缓存异常，可能需要手动清理缓存以确保使用最新代码。

### Windows PowerShell

```powershell
# 删除编译缓存文件夹
Remove-Item -Recurse -Path game\cache

# 删除所有 rpyc 文件
Remove-Item -Path game\*.rpyc
Remove-Item -Path game\**\*.rpyc -Recurse
```

### 一键清理脚本

```powershell
Remove-Item -Recurse -Path game\cache; Remove-Item -Path game\*.rpyc; Remove-Item -Path game\**\*.rpyc -Recurse
```

删除后下次启动会稍慢（需要重新编译所有脚本），但能确保运行的是最新的 `.rpy` 代码。

---

## 翻译工作流

1. **提取字符串**：运行 `extract_translations.py` 生成模板
2. **翻译**：在 `game/tl/<语言>/strings.rpy` 中填写翻译
3. **测试**：启动游戏验证显示效果
4. **清理缓存**：如遇异常，执行上述清理命令
