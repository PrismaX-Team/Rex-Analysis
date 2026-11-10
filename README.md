# Rex-Analysis 网站

面向研究型智能体的评测基准合集。现在有两个 bench：ResearchClaw Bench（RCB）和 AgentFrontierExam 1.0（AFE1.0）。

静态前端。Vue 3 + Vite，样式是 SCSS，页面逻辑是 JavaScript。

设计依据见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 本地看

```bash
cd web
npm install
npm run dev
```

浏览器打开终端里打印的地址。首页是 bench 总览，点卡片进入该 bench 自己的榜、题和说明。每个 bench 的 GitHub 链接只在它自己的页面上出现，首页不放。

## 部署到 8090

```bash
web/deploy/serve.sh          # 构建 dist/，在 tmux 会话 rex-analysis 里起静态服务（0.0.0.0:8090）
tmux attach -t rex-analysis  # 看日志；Ctrl-b d 退出
```

`serve_dist.py` 对无扩展名的路径回退到 `index.html`，所以刷新 `/rcb/1.0/tasks/Physics_001` 还是这一页。这台机器的端口记录不放进仓库。

## 部署到 GitHub Pages

仓库里已经带好了 `.github/workflows/pages.yml`。推到 `main` 后，Actions 会构建 `web/` 并发布到 `https://<owner>.github.io/<仓库名>/`。

第一次需要在仓库 Settings → Pages → Source 选 **GitHub Actions**。

- 站点挂在 `/<仓库名>/` 子路径下，构建时用 `BASE` 环境变量告诉 Vite 和路由（workflow 已经设好）。本地和 8090 不设，仍是 `/`。
- GitHub Pages 没有重写规则，直接打开 `/afe/1.0/tasks/xxx` 这类深链会落到 `404.html`。`npm run build:pages` 会把 `index.html` 复制成 `404.html`，前端路由接管后照常显示这一页（HTTP 状态码仍是 404，浏览器里看不出来）。
- 用自定义域名或 `<owner>.github.io` 仓库时，把 workflow 里的 `BASE` 改成 `/`。

本地模拟 Pages 的构建：

```bash
cd web && BASE=/Rex-Analysis/ npm run build:pages
```

## 数据

`content/` 是网站唯一的数据来源。

| 文件 | 来源 |
|---|---|
| `benches.json` | 手写，bench 清单、各自的 GitHub 和页面文案 |
| `rcb/versions.json` | 手写，RCB 版本清单 |
| `rcb/1.0/leaderboard.json`、`pass5.json` | `tools/build_content.py` 生成 |
| `rcb/1.0/runs/*.json` | `tools/build_content.py` 生成 |
| `rcb/1.0/tasks.json` | 从任务包 `task_info.json` 迁移的公开字段 |
| `rcb/1.0/about.md` | 手写，说明页正文 |
| `rcb/1.0/atlas.json` | 手写，星图的学科、中文短名和方法线 |
| `afe/versions.json` | 手写，AFE 版本清单 |
| `afe/1.0/about.md` | 手写，说明页正文 |
| `fields.json` | `tools/build_fields.py` 生成：任务数只统计 RCB 公开任务，领域和二级领域名取自 AFE 版本管理表 |
| `committee.json` | 手写，首页团队区；照片放 `web/public/committee/` |

重新生成榜单：

```bash
python3 tools/build_content.py
```

脚本只读 `sources/content.lock.json` 里登记的输入。RCB 1.0 的输入是官方 `ResearchClawBench-Home` 的 `data/leaderboard.json` 快照，存在 `sources/1.0/`。要更新榜，先换快照、改 lock 里的日期，再跑脚本。排名规则和官方站一致：均分按一位小数比，平分时比覆盖题数；智能体和独立大模型分开排。

重新生成 AFE 任务和领域版图（AFE 先跑，领域版图要读它）：

```bash
python3 tools/build_fields.py ../_AgentFrontierExam版本管理.xlsx
```

AFE 的题目内容不公开：仓库里没有 AFE 任务数据，也没有生成它们的脚本。AFE 在站上只是展示页（设计、任务特性、任务包结构、委员会）。

不要把 `target_study/` 或任何评分材料放进 `content/`。
