# DSHA v0.3.0 · 千钧魔改版

> 基于 [DSH-APP/DSHA](https://github.com/DSH-APP/DSHA) v0.1.5-rc2（MIT 协议）
> 原作者 [@qiannianhuanxiang](https://github.com/qiannianhuanxiang) · 上游维护 [@ym2025szz](https://github.com/ym2025szz) · 魔改 [@XiaoZishannb](https://github.com/XiaoZishannb)

## ✨ 魔改特性

- 🌗 **深色图标** — 自适应图标 + monochrome 单色图层，ColorOS / 原生 Android 深色主题与主题图标自动适配
- 🎨 **深浅色跟随系统** — 应用主题默认跟随系统（values-night 全套暗夜资源）
- 🛒 **插件市场** — 插件页内置 1024 商店热门目录：远程拉取 → 本地缓存 → 内置兜底，三级降级，一键安装
- 🙏 **署名** — 关于页明确致谢原作者与上游维护者

## 📦 安装包

`dsha-v0.3.0-paimon.apk`（167 MB，完整离线运行库：Ubuntu rootfs + dsh 运行时 + Ubuntu 工具链）

⚠️ **签名说明**：本魔改版使用独立签名密钥，与上游 DSHA **签名不同**。若已装上游版需先卸载再装本版（数据不互通），反之亦然。

## 🔧 与上游的差异

- compileSdk/targetSdk 36（上游 37，公共 SDK 源暂未发布）
- 本地单测适配 JDK21 工具链（TestIo 等价实现）
- ubuntu-tools 锁更新：libperl 5.38.2-3.2ubuntu0.6
- 发布构建跳过 lint vital（网络环境限制）
- 其余功能与上游 v0.1.5-rc2 一致

## ✅ 验证

- 本地单测全部通过（含新增 MarketCatalogTest）
- 完整资产链构建：rootfs 81.8MB + dsh-runtime 35.5MB + ubuntu-tools 17.6MB
