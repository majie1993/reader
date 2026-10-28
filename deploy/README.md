# 本 fork 的说明

上游：hectorqin/reader（旧 Java 版「阅读3」服务器）的社区延续线。本 fork 基于
dumpmemory/reader 的 master（上游原仓库 master 已被作者清空，旧源码只存于 fork 网络），
与线上部署的 changshengyu/reader:2.5.4-slim 同属一个代码系。

## 与上游唯一的源码差异

`web/src/views/Index.vue` 删除 14 行：`.status-bar-light-bg` 与
`.status-bar-light-bg-dialog` 两条 CSS 规则。

原因：该渐变（顶部 36px、rgba(0,0,0,.2) → 透明）只在 iOS 把页面添加到主屏幕
（PWA standalone，`window.navigator.standalone` 为 true）时加到书架容器上，
本意是给 black-translucent 状态栏垫底；但下拉时整页橡皮筋下移，这道渐变会
被带到屏幕上方，形成一条明显的灰色遮罩带。状态栏图标在本机为黑字白底，
不需要这层垫底，故直接删掉。

## 自建镜像

后端 jar 与 changshengyu/reader:2.5.4-slim 逐字节相同，只把 jar 内
`BOOT-INF/classes/web/` 的前端资源换成本仓库源码构建的产物（后端零回归风险；
哪天需要改后端，再打通 Dockerfile.source 的全量源码构建）。

在仓库根目录构建：

```bash
docker build -f deploy/Dockerfile -t jeff/reader:2.5.4-slim-patched1 .
```

- 前端构建用 Node 16；仓库没有 lockfile，今日解析出的依赖中有要求
  Node ≥18 的小包（node-releases），故 yarn install 带 `--ignore-engines`。
- 换上游版本时：改 deploy/Dockerfile 里的 `changshengyu/reader` 标签后重跑构建。

## 部署（a1，reader.codinging.com）

`~/reader/docker-compose.yaml` 里 reader 服务的 image 改为自建标签后
`docker compose up -d`；storage、logs 卷与环境变量都不动。
回滚：image 改回 `changshengyu/reader:2.5.4-slim` 再 up -d。
