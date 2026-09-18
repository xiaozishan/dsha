# DSHA · 千钧魔改版（v0.3.0）

> **本仓库是 [DSH-APP/DSHA](https://github.com/DSH-APP/DSHA) 的魔改分支**，
> **原作者 [@qiannianhuanxiang](https://github.com/qiannianhuanxiang)**，
> **上游维护者 [@ym2025szz](https://github.com/ym2025szz)**，
> 魔改发行 **[@XiaoZishannb](https://github.com/XiaoZishannb)**（派蒙代打 🍗）。
> 上游许可证：MIT。请优先支持上游！

## 魔改内容（v0.3.0）

| 特性 | 说明 |
|:---|:---|
| 🌗 **深色图标** | 自适应图标 + **monochrome 单色图层**，ColorOS / 原生 Android 深色主题与主题图标自动适配 |
| 🎨 **跟随系统深浅色** | 应用主题默认「跟随系统」（含 values-night 全套暗夜资源） |
| 🛒 **插件市场** | 插件页内置 1024 商店目录：远程拉取 → 本地缓存 → 内置兜底三级降级，一键安装（复用既有链接安装管线，含单测） |
| 🙏 **署名** | 关于页明确致谢原作者与上游维护者 |

## 与上游的差异

- `compileSdk/targetSdk 36`（上游 37，公共 SDK 源暂未发布 37）
- 本地单测兼容：用 `TestIo` 等价实现替代 `Files.readString/writeString`（JDK21+bootclasspath 组合下不可见）
- 其余功能代码与上游 v0.1.5-rc2 保持一致

## 构建

```bash
# JDK 17+，Android SDK（platform-36 + build-tools 36），Python 3.9+，Node 18+
cd tools/web-compat && npm ci && cd ../..
node tools/prepare-web-compat.mjs
cd tools/dsh-runtime && npm ci --os=linux --cpu=arm64 --ignore-scripts && cd ../..
python tools/build-dsh-runtime.py --source tools/dsh-runtime --output app/src/main/assets/dsh-runtime.bin
# 完整包需 app/src/main/assets/offline-rootfs.bin（Ubuntu rootfs，取自上游发布版或 CI 工件）
./gradlew :app:assembleStandardRelease
```

## 安装注意

本魔改版使用**独立签名密钥**，与上游 DSHA **签名不同** —— 若已装上游版需先卸载再装本版（数据不互通），反之亦然。

其余使用说明与上游一致：见 [上游 README](https://github.com/DSH-APP/DSHA#readme) 与 [AGENTS.md](AGENTS.md)。
