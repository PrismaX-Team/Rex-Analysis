# Rex-Analysis 网站系统架构

状态：与当前实现同步。本文只定边界、数据和页面职责，不写页面样式。

读者：做这个站的人。

## 1. 这个站是什么

Rex-Analysis 是面向研究型智能体的评测基准合集。一个站上挂多个 bench，每个 bench 有自己的榜、题和评分规则。

现在上线两个 bench：

| bench | 状态 | 内容 |
|---|---|---|
| ResearchClaw Bench（RCB） | live | 40 题、10 个学科、单版本 1.0，RADS 0–100 |
| AgentFrontierExam 1.0（AFE1.0） | live，展示页 | 只展示设计哲学、任务特性、任务包结构和委员会入口；题目内容不公开 |

首页为后续 bench 预留了空位。新 bench 上线的步骤见第 11 节。

参考 xbench 的用法，不复制它的站点：先看到站上有哪些 bench，进入之后才是这个 bench 的详细界面。

## 2. 不做什么

明确不做：

- 用户账号、登录、权限。
- 网页上传一次运行。
- 在线评测、裁判模型、任务执行。
- 跨 bench、跨版本合成一个总分。
- 数据库、缓存、后端服务。
- 展示 `target_study/`：checklist、目标论文、参考图、数值答案。
- 展示 discovery 任务的目标论文题名和 DOI。

首页也不做某一个 bench 的专属视觉。首页属于全体 bench，单个 bench 的表达留在它自己的入口页。

提交一次运行，现在只在说明页写清交付格式和联系方式。真要在网页上收结果时，再在那个点加一个只负责写入榜的服务。

## 3. 三层界面

### 3.1 首页 `/`

首页只回答两件事：站上有哪些 bench，怎么参与。

- 顶栏：站名、导航（Benchmarks / 排行榜 / 评测说明 / 提交科学问题）。只有 Benchmarks 在首页内滚动，其余都去别的页：排行榜去全站榜 `/leaderboard`，评测说明去全站说明 `/about`，提交科学问题外链到 ReX 页面。右侧只有主题切换，首页不放 GitHub。往下滚时吸顶。
- 首屏：站名大字、一句话说明、「浏览 Benchmarks」按钮。右侧是榜单轮播，每个 bench 一张，显示该 bench 的前 5 名；最多 3 张（`benches.json` 的 `carousel`），live 的 bench 先放，不够时用占位骨架补齐。轮播 6 秒自动切换，鼠标悬停或键盘聚焦时暂停，可点圆点或箭头手动切换。
- Benchmarks 区：每个 live bench 一张卡片，显示任务数、学科数、提交数、最高分；后面跟 `placeholders` 个 COMING SOON 空位。
- 关于 ReX：一块与榜单轮播同尺寸的卡片。左边是 ReX 名字的含义（Re = Research / Recursive，X = 任意科学任务）、一句合作方式和「提交科学问题」按钮，按钮外链到书生·端砚的 ReX 页面；右边是 L1–L3 三级任务和四步合作流程；四步是可点的标签，点哪一步，下方显示那一步的说明。内容是从 ReX 页面浓缩的，不照搬表单细节。
- Leaderboard 总榜：在「关于 ReX」下面，参考 xbench 的总榜。每个 live bench 按排名分组各占一行（RCB 是大模型榜、智能体榜两行）：Benchmark、分类、1st–5th（名字、所用模型和分数）、详情。整行可点，进入该 bench 的完整榜并切到对应分组（`?group=agent`）。行数据从 `benches.json` 读，前五名按生成脚本写好的 `rank` 取，前端不重排。现在只有 RCB 两行；未上线的 bench 不占行，不显示占位。
- 覆盖领域：在总榜下面，统计站上所有数据集（现在是 RCB 和 AFE）。左边是领域数和二级领域数两个大数字，右边是每个领域的条形，按数据集分段：实色是已上线，浅色是规划中；页面上统一叫「方向」，RCB 一道题算一个方向。下面三行循环滚动二级领域的名字（不放题目名），旁边是已有任务的领域数和各数据集覆盖的领域数。左上两个数字是一级领域数和二级领域数。方向还没定，这一块不出现「方向」的数字。数据来自 `content/fields.json`。
- 团队：每个委员会一排，循环滚动，悬停或键盘聚焦时暂停，点卡片去本人主页。数据来自 `content/committee.json`，成员为空的组不显示（学术委员会现在就是这样）。系统设置了减少动态时不自动滚动，改成手动横向滚动。
- 如何参与：选 bench、跑完全部任务、评分上榜，三张卡片各自可点，分别进说明页、GitHub 任务包和排行榜。
- 页脚：跨 bench 分数不可横比的说明和联系方式。

首页不放题目列表，也不放某个 bench 的完整榜。

### 3.1.1 全站页 `/leaderboard`、`/about`

导航里的「排行榜」「评测说明」不进某一个 bench，而是进这两个全站页，加 bench 时不用改导航。

- `/leaderboard`：首页同款总榜（`OverallBoard.vue`，每个 bench 每个分组一行、前五名），下面是每个 live bench 一张卡片，点进它的完整榜。
- `/about`：全站通用规则，正文来自 `content/about.md`（这个站测什么、榜单怎么读、如何参与、提交科学问题）；末尾每个 live bench 一张卡片，点进它自己的评分规则。

两页的顶栏不带 bench 面包屑，导航是「排行榜 / 评测说明」。

### 3.2 Bench 入口 `/rcb`、`/afe`

每个 bench 自己的入口页，外形相同（左边标题、数字、按钮，右边一块展示区），展示区按 bench 不同。GitHub 链接只在入口页和内页的顶栏出现，地址在 `benches.json` 的 `github`；首页不放 GitHub。

AFE 的描述文字（入口页、`benches.json`、`afe/versions.json`、`afe/1.0/about.md`）都取自 [AFE 任务站](https://prismax-team.github.io/AgentFrontierExam-Tasks/zh/)，不另外撰写；改文案先看任务站。

**AFE 入口 `/afe`**：左边是标题、三个数字（任务、领域、提交）和四个按钮（浏览任务、排行榜、评测说明、参与共建；参与共建外链到端砚的 ReX 页面）。右边是已接入领域的卡片，每个领域一张：题数、三道题的中文短名，点卡片进入按该领域筛选的任务列表。运行方式写在说明页，入口页不重复。

**RCB 入口 `/rcb`**：

一个 bench 的介绍页，回答「这个 bench 测什么、有多少题、现在谁领先」。

- 顶栏：站名 / ResearchClaw Bench，可以点回首页。
- 左侧：bench 标题、一句话说明、四个数字（任务、学科、提交、最高分）、三个按钮：排行榜、浏览 40 个任务、展开星图。
- 右侧：任务星图。十个学科排成一圈，每个学科四颗星；彩线是方法线，连接用到同一类方法或研究同一类对象的题。
- 展开星图后：星图占满主区域，右侧出现说明面板。悬停星星或学科时，图上只保留相关部分，面板显示题名、它和谁通过哪条方法线相连；点击可以钉住，再点取消。点星星或学科旁的入口进入对应的题面或任务列表。

### 3.3 Bench 内页

顶栏：

```text
[Rex-Analysis] / [ResearchClaw Bench]     排行榜   任务   说明        GitHub ↗
[Rex-Analysis] / [AgentFrontierExam 1.0]  排行榜   任务   说明        GitHub ↗
```

内页是两个 bench 共用的一套组件，从 URL 的 `:bench` 段读出是哪个 bench。页眉小字、任务页导语、排行榜导语、空榜文案、单题页的「不公开」说明都来自 `benches.json`，组件里不写死某个 bench 的文案。

版本是 Bench 名旁边的下拉框，只在版本多于一个时出现。现在只有一个版本，所以不显示。

| 项 | 职责 |
|---|---|
| 排行榜 | 这一版的提交，按组分开排名，可展开分题成绩 |
| 任务 | 这一版的公开题目，按学科筛选 |
| 说明 | 这一版的任务包结构和评分规则 |

领域不是导航项，是任务页上的筛选。

**排行榜页**：最上面是 Pass@1 / Pass@5 切换。

Re-Discovery / New-Discovery 不单独画图，直接落在表格里：50 分以下的格子用五档蓝色（Re-Discovery），50 分及以上换成一档绿色（New-Discovery）。学科格、展开后的分题小格、色阶图例都用这套色。另有一列「New」，写这一行有几道题达到 50，悬停能看到是哪几道；展开一行时，题格上方先列出这些题。前三名卡片上也有「New-Discovery × n」标记。

Pass@5 表格每题取五次里的最高分。学科格分两行：上面是五次取最好的学科均分，下面是该学科全部尝试的均值 ± 标准差。末列是全部 200 次尝试的均值 ± 标准差。小格悬停能看到五次分数、均值 ± σ、最低 / 最高和计入的尝试数。Pass@5 只有官方公布的 6 个独立大模型，不分组，没有前三名卡片，也没有单次提交页。

Pass@1 表格：顶部分「大模型」「智能体」两组，默认先看大模型。组标签下面一行写「N 个模型（或智能体）· 数据更新于 某日」，日期是榜单快照的抓取日期（`leaderboard.json` 的 `updated`，由生成脚本从 lock 文件写入）。前三名是三张卡片。表格的主列是模型，Harness 单独一列：智能体行的 Harness 是智能体名（有主页时可点）；大模型行是该组共享的 Harness（`groups[].harness`，RCB 是 ResearchHarness）。其余列是均分、十个学科的均分、New 题数、题数、单题成本、单题用时、来源（社区 / 内测）。均分、单题成本、单题用时三列可以点表头排序，再点一次反向；名次列始终是官方名次，不随排序改变。

**分数与成本图**（`CostChart.vue`）：在 Pass@1 表格下面，跟随当前分组。横轴单题成本（对数刻度），纵轴均分（从最低分下方的整十开始），点的面积表示单题用时。Pareto 前沿连成一条线并标名：在不多花钱的前提下分数最高的提交。只给前沿上的点标名，放不下的就不标，悬停或键盘聚焦任意点都有提示。Pass@5 和没有成绩的 bench 不显示这张图。点一行展开四十道题的小格，按学科分组，全榜最高的题带标记。点小格进题面。

**单次提交页**：均分、模型、题数、成本、日期、来源，然后按学科列出每道题的分数条。50 分处有一条竖线，表示达到原论文的证据水平。没评分的题写「未评分」。

**任务页**：卡片显示题号、学科、中文短名和题面摘要。学科颜色同时用在一级筛选和卡片左边线。

**单题页**：左边是题面和数据文件，右边是跟随滚动的信息卡（学科、版本、题型、数据文件数）。RCB 的题面是一段纯文本；AFE 的题面是智能体看到的完整 markdown，用中文短名作标题，英文原题放在下面。信息卡的按钮：有单题公开地址时是「公开任务包」，没有时是「项目仓库」，指向该 bench 的 GitHub。

**AFE 排行榜**：现在没有公开成绩，页面显示「暂无公开成绩」和去任务列表的入口；首页轮播和总榜同样处理，不显示空表。站上不写任务数是阶段进度，也不写评分校准之类的内部状态。

**说明页**：左侧目录，右侧正文，章节之间用分隔线。正文来自 `about.md`。

## 4. 路由

一个 Vue 3 应用：

| 路径 | 页面 |
|---|---|
| `/` | bench 总览 |
| `/leaderboard` | 全站榜：各 bench 前五名 |
| `/about` | 全站评测说明 |
| `/rcb` | RCB 入口 |
| `/afe` | AFE 入口 |
| `/:bench/:version/leaderboard` | 榜 |
| `/:bench/:version/runs/:runId` | 一次提交 |
| `/:bench/:version/tasks` | 任务列表 |
| `/:bench/:version/tasks/:taskId` | 一题的公开题面 |
| `/:bench/:version/about` | 这一版的规则 |

`:bench` 只接受 `benches.json` 里 live 的 id（现在是 `rcb|afe`），别的值不匹配任何路由。`:version` 不在该 bench 的版本清单里，就回到该 bench 的入口页，不渲染空详情页。

版本段保留在 URL 里，即使现在只有一个版本。以后加版本时路由模板不变，把顶栏的下拉框放出来即可。

入口页每个 bench 一个组件；内页共用，靠 `:bench` 区分。

## 5. 数据

网站不连接数据库。所有数据是构建时就能读到的静态文件，前端只读。

```text
content/
  benches.json            手写：bench 清单、GitHub、页面文案
  about.md                手写：全站评测说明
  fields.json             tools/build_fields.py 生成：领域版图
  committee.json          手写：委员会成员
  rcb/
    versions.json         手写：RCB 版本清单
    1.0/
      leaderboard.json    脚本生成
      tasks.json          从任务包迁移的公开字段
      runs/<run_id>.json  脚本生成
      pass5.json          脚本生成：Pass@5 榜
      about.md            手写：说明页正文
      atlas.json          手写：入口页星图的学科、短名和方法线
  afe/
    versions.json         手写：AFE 版本清单
    1.0/
      about.md            手写：说明页正文
```

AFE 没有 `leaderboard.json`，前端按空榜处理。成绩发布后照 RCB 的格式生成即可，页面不用改。

RCB 2.0 的旧草稿不在仓库里。

`content/` 里哪些是生成物、哪些是手写，见第 8 节。不要把 `target_study/` 或任何评分材料放进这个目录。

### 5.1 benches.json

首页和轮播的唯一来源。

```json
{
  "benches": [
    {
      "id": "rcb",
      "slug": "rcb",
      "name": "ResearchClaw Bench",
      "short": "RCB",
      "tagline": "智能体复现一篇论文",
      "summary": "...",
      "status": "live",
      "entry": "/rcb",
      "task_type": "任务包 · 开放域复现",
      "scoring": "RADS 0–100",
      "accent": "#2f4bff",
      "accent_dark": "#6f86ff",
      "category": "科研智能体",
      "version": "1.0"
    }
  ],
  "placeholders": 3
}
```

`launched` 是上线月份（`YYYY-MM`），首页顶部的提示条显示最新上线的 bench 和这个月份，例如「v2026.11 AgentFrontierExam 1.0 已上线」；加新 bench 时记得填。`category` 是首页总榜里的分类标签，没有时退回 `task_type`。`version` 是总榜读哪一版的榜，没有时用 `1.0`。

`status` 现在只用到 `live`。`placeholders` 是首页 Benchmarks 区预留的空位数量。`carousel` 是榜单轮播的总张数，live 的先放，余下用占位补齐，不超过 `placeholders`。

`accent` 在浅色主题用，`accent_dark` 在深色主题用。卡片和轮播的颜色都从这里取，不在组件里按 id 写死。

### 5.2 versions.json

版本清单。顶栏下拉框、路由校验和页头的分数说明都读它。

```json
{
  "versions": [
    {
      "id": "1.0",
      "label": "1.0",
      "status": "current",
      "score_name": "RADS",
      "score_note": "0–100。50 表示达到原论文的证据水平，70 以上表示超过。定性 checklist。"
    }
  ]
}
```

`status` 只有 `current` 和 `history`。多于一个版本时顶栏才出现下拉框。

页头的分数说明用 `score_note`，不在组件里写死某个版本的文案。

### 5.3 leaderboard.json

一次提交一行。排序和名次由生成脚本算好写进文件，前端不重新排名。

```json
{
  "version": "1.0",
  "source": "InternScience/ResearchClawBench-Home data/leaderboard.json",
  "note": "...",
  "domains": ["Astronomy", "Chemistry", "..."],
  "groups": [
    { "id": "agent", "label": "智能体", "en": "Agents" },
    { "id": "llm", "label": "独立大模型", "en": "Standalone LLMs", "note": "全部用 ResearchHarness 运行。" }
  ],
  "frontier": { "Astronomy_000": { "score": 94.7, "run_id": "jiutian-deepinsight" } },
  "rows": [
    {
      "run_id": "jiutian-deepinsight",
      "group": "agent",
      "system": "jiutian-DeepInsight",
      "model": "Qwen3.8-Max",
      "source": "community",
      "source_url": "https://...",
      "score": 41.36,
      "task_count": 40,
      "date": "2026-09-22",
      "cost_usd": 11.0,
      "duration_seconds": 14580,
      "domains": { "Astronomy": 55.6, "Chemistry": 36.2 },
      "rank": 1
    }
  ]
}
```

- `rank` 在组内编号，所以两个组各有一个第 1 名。
- `frontier` 是每道题的全榜最高分和拿到它的提交，用于在分题格子上打标记。
- 缺一次提交、或这次提交没有覆盖全部题目时，`task_count` 照实写。不把未覆盖的题算成 0 分再去和完整提交比名次。
- `source` 是 `community` 或 `internal`，决定表格里显示「社区」还是「内测」。

### 5.4 runs/<run_id>.json

一次提交的详情，点开一行时用。

```json
{
  "run_id": "claude-code",
  "version": "1.0",
  "system": "Claude Code",
  "model": "Claude-Opus-4.6",
  "group": "agent",
  "source": "internal",
  "date": "2026-04-02",
  "score": 21.53,
  "task_count": 40,
  "cost_usd": 5.25,
  "duration_seconds": 1560,
  "report_note": "分题报告、代码和评分理由仍在原项目站。",
  "report_url": "https://internscience.github.io/ResearchClawBench-Home/",
  "tasks": [
    { "task_id": "Astronomy_000", "score": 23.5, "cost_usd": 0.2, "duration_seconds": 120 }
  ]
}
```

`tasks` 里每道题都在，没评分的写 `score: null`，页面显示「未评分」，不省略。

这里的分题分数是已经公开的结果。不放 checklist 原文、裁判理由里的答案，或数值目标。

### 5.5 tasks.json

只含公开字段。

```json
{
  "version": "1.0",
  "tasks": [
    {
      "task_id": "Astronomy_000",
      "title": "...",
      "domain": "Astronomy",
      "domain_label": "天文学",
      "task_type": "reconstruction",
      "summary": "...",
      "task": "...",
      "data": [
        { "name": "...", "path": "data/...", "type": "feature_data", "description": "..." }
      ],
      "source_url": "https://github.com/InternScience/ResearchClawBench"
    }
  ]
}
```

- `title` 是论文原句截断后的英文，可能在词中间断掉。页面优先显示 `atlas.json` 里的中文短名，没有短名时才退回 `title`。
- `summary` 给卡片用，`task` 是完整题面，给详情页用。
- `task_type` 三种：`reconstruction`、`discovery`、`abstraction`。
- discovery 任务的 `title`、`summary`、`task` 和 `data[].description` 不得含目标论文题名或 DOI。

### 5.6 atlas.json

首页星图用的整理数据，只有 RCB 有。

```json
{
  "version": "1.0",
  "note": "人工整理：每题一个短名；方法线把共享同一方法或研究对象的题连起来。",
  "domains": [
    { "id": "Astronomy", "label": "天文学", "en": "Astronomy", "color": "#6a4cff", "color_dark": "#8c75ff" }
  ],
  "labels": { "Astronomy_000": "超轻玻色子约束" },
  "threads": [
    { "id": "graph", "label": "图神经网络", "tasks": ["Chemistry_000", "Material_000"] }
  ]
}
```

- `labels` 是四十道题的中文短名，任务页和单题页也用它当标题。
- `threads` 是方法线。每条的 `tasks` 按顺序连成一条链，跨学科的连线在图上穿过中心。
- `color_dark` 是深色主题下的提亮版本，和深色背景的对比度不低于 5.5:1。
- 这份文件是人工整理的，不是生成物。改短名或方法线会影响首页、任务页和单题页三处。

### 5.7 about.md

说明页正文，按版本放。用最小的 markdown 子集渲染：`#`、`##`、段落、列表、行内代码、代码块、链接。写清公开侧和隐藏侧；隐藏侧只说明「存在、不公开」，不贴内容。

## 6. 前端结构

```text
web/
  index.html               主题预置脚本
  src/
    main.js                入口，注册路由和样式
    router.js              路由和版本校验
    data/
      client.js            唯一读 content/ 的地方
      markdown.js          最小 markdown 渲染
    theme/
      useTheme.js          浅色 / 深色切换与持久化
    data/useBench.js       从 URL 读 bench、版本和链接前缀
    pages/
      Home.vue             bench 总览
      Rcb.vue              RCB 入口（含星图）
      Afe.vue              AFE 入口（领域卡片）
      Leaderboard.vue      榜
      Run.vue              一次提交
      Tasks.vue            任务列表
      Task.vue             单题
      About.vue            说明
    components/
      TopBar.vue           bench 内页顶栏
      VersionSelect.vue    版本下拉框（仅多版本时显示）
      ThemeToggle.vue      主题切换
      ScoreNote.vue        分数说明
      LeaderboardTable.vue 榜表格和分题格子（pass1 / pass5 两种模式）
      CostChart.vue        分数与成本散点图、Pareto 前沿
      TaskList.vue         任务卡片
      Atlas.vue            任务星图
    styles/
      main.scss            全局变量、内页
      hub.scss             首页
      home.scss            RCB 入口
      board.scss           榜和提交页
```

约束：

- `client.js` 是唯一读 `content/` 的地方。组件不直接写文件路径。它的读取函数都先传 bench、再传版本，例如 `getTasks("afe", "1.0")`。
- 组件里不出现 `if (version === "1.0")` 或 `if (bench === "rcb")` 这种分支。bench 和版本的差异放在 JSON 和 markdown 里。
- 榜的排序、名次、是否入榜，不在浏览器里重算。
- 颜色、间距、字体走 CSS 变量，组件里不写死颜色。主题差异只改变量值。
- 首页和 bench 入口是两个页面，不靠条件在一个页面里切换形态。

## 7. 主题

浅色和深色两套，用户可切换。

- `index.html` 在首屏渲染前读 `localStorage` 的 `rcb-theme`，没有就跟随系统，把结果写进 `<html data-theme>`。这样打开时不会先闪一下浅色。
- `useTheme.js` 负责切换和持久化，切换时给 `<html>` 加 350ms 的过渡类，避免整页跳变。
- 变量定义在 `main.scss` 的 `:root` 和 `:root[data-theme="dark"]`。语义色阶（背景、纸面、正文、弱化、线、强调、紫、青、读数面板、光晕）两套各给一组值。
- 图形里的颜色不能只靠 CSS 变量时（SVG 渐变、星图的学科色），在 JS 里按当前主题选值。学科的深色版本存在 `atlas.json` 的 `color_dark`。
- 排行榜 50 分以下的五档色阶是一套单色蓝，50 分以上是一档绿（New-Discovery），两套主题各有一组步进值，数字文字始终保持正文色。刻度按 0–10、10、20、30、40–50、50+ 分档，没有分数用斜纹。

## 8. 生成与更新

```text
tools/
  build_content.py        RCB 榜
  build_fields.py         领域版图（读上面两者的产物和版本管理表）
sources/
  content.lock.json       按 bench 登记输入：rcb.1.0.*、afe.1.0.tasks
  1.0/rcb-home-leaderboard.json
```

AFE 的题目内容不公开：仓库里没有生成 AFE 任务的脚本，也没有 `tasks.json`。站上的 AFE 只是展示页。

`sources/content.lock.json` 登记每一份输入的路径、来源 URL 和抓取日期。脚本只从登记过的路径读。

`build_content.py` 负责 `content/rcb/1.0/leaderboard.json` 和 `content/rcb/1.0/runs/*.json`：

1. 读 `content.lock.json` 里 1.0 的榜快照。
2. 按官方站规则排名：已评分题目的均分，先比一位小数，平分时比覆盖题数，再比原始均分。智能体和独立大模型分组各排各的。
3. 写出榜和每个提交的详情，写入前清掉旧的 `runs/`。
4. 检查输出里没有 `checklist`、`target_study`、`paper.pdf`、`tolerance` 这些字段或路径；有就整体失败，一个字都不写。

任务数据不在这个脚本里：

- `tasks.json` 是从任务包 `task_info.json` 一次性迁移的公开字段。
- `about.md`、`atlas.json`、`benches.json`、`versions.json` 是手写的。

更新榜单的流程：

```bash
# 1. 换快照：下载官方 data/leaderboard.json 到 sources/1.0/
# 2. 更新 sources/content.lock.json 里的 fetched 日期
cd web && npm run dev            # 看效果
python3 tools/build_content.py   # 重新生成 content/rcb/1.0/
```

脚本失败时不要用上一版生成物冒充这一次成功；先把失败原因修掉。

`tools/build_fields.py <版本管理表.xlsx>` 负责 `content/fields.json`。任务数只统计 RCB 公开任务（`content/rcb/1.0/`）；一级和二级领域名取自 AFE 版本管理表，不含任何 AFE 题目。表里还有负责人、合作方、项目来源、进度和 2.0 内部计划，这些一律不导出。RCB 的学科对不上表里的领域时整体失败。表本身不进仓库。

## 9. 和任务包的对应

AFE 用 Harbor 任务包（`task.toml`、`instruction.md`、`environment/`、`tests/`、`solution/`、`authoring/`）。这些内容都不公开：站上只有 AFE 的展示页，仓库里不存任务数据和生成脚本。

RCB 网站不发明第三套任务格式。任务包仍是：

```text
tasks/<Domain>_<NNN>/
  task_info.json          公开
  data/                   公开
  related_work/           公开
  target_study/           隐藏，不进网站
```

`task_info.json` 里用 `benchmark_version` 标明版本。网站的版本目录由这个字段决定，不由文件夹名字决定。

内部任务 id 可以带 `RCB_` 前缀和配额后缀。网站上的 `task_id` 用官方题号，例如 `Astronomy_000`。配额后缀不是另一题，不单独占一行。

## 10. 部署

构建产物是静态文件：

```bash
cd web && npm run build     # 输出 web/dist/
```

需要支持第 4 节的全部路径。刷新 `/rcb/1.0/tasks/Physics_001` 必须还是这一页，不能落到服务器的 404，用前端路由的回退配置解决，不为此加应用服务器。

现在机器上的部署是 `web/deploy/serve.sh`：`npm run build` 后在 tmux 会话 `rex-analysis` 里跑 `serve_dist.py`，监听 `0.0.0.0:8090`。`serve_dist.py` 自己做了 SPA 回退（无扩展名的路径返回 `index.html`），并有 `.webp`、`.woff2` 的 MIME。进程随 tmux 存活，`tmux attach -t rex-analysis` 可以看输出。

GitHub Pages：`.github/workflows/pages.yml` 在推到 `main` 时构建并发布。站点在 `/<仓库名>/` 子路径下，构建时的 `BASE` 环境变量同时设置 Vite 的 `base` 和路由的 `createWebHistory(import.meta.env.BASE_URL)`；照片地址也从 `BASE_URL` 拼出来。Pages 不能配置 SPA 回退，所以 `npm run build:pages` 额外写一份 `404.html`（就是 `index.html`），深链落到它后由前端路由渲染。

除了构建时的 `BASE`，没有运行时的环境变量、没有数据库迁移、没有缓存失效。

## 11. 以后才加的东西

| 需求 | 加在哪 | 现在为什么不加 |
|---|---|---|
| 新 bench | `benches.json` 加一项（含 `github` 和文案）、`placeholders` 减一；新增 `content/<id>/versions.json` 和 `content/<id>/<版本>/`；在 `client.js` 的 `books` 里登记；写一个入口页并在 `router.js` 加 `/<id>` 一条。内页路由不用加。AFE 就是这样接入的 | — |
| 第二个版本 | `versions.json` 加一项、加 `content/<版本>/`、生成脚本读出它 | 当前只有 1.0 |
| 网页提交一次运行 | 说明页上的一个写入动作，只追加榜的一行 | 还没有人从网页交结果 |
| 登录后的未公开榜 | 单独的部署，不混进这个静态站 | 这个站的定义是公开榜 |

加后端时优先做一个只写 `leaderboard.json` 的小服务，不因为加了提交就引入数据库。等榜的行数、并发或权限真的需要，再换存储。

## 12. 验收

下面几条都满足，架构才算落地，而不是只写了页面：

1. 首页列出 RCB 一张真卡片和三个空位，轮播能切到空位那张。
2. 从首页卡片进 `/rcb`，再能进排行榜、任务、说明。
3. 直接打开 `/rcb/1.0/tasks/Physics_001` 落到该题；打开 `/rcb/9.9/tasks` 回到 `/rcb`。
4. 只有一个版本时，顶栏不出现版本下拉框。
5. 任意页面的数据里搜不到 checklist、目标论文、参考图、数值答案。
6. 深色主题下星图、榜表格和首页卡片都看得清；切换后刷新仍是同一个主题，首屏不闪。
7. 跑 `python3 tools/build_content.py`，`content/rcb/1.0/` 能完整重建；脚本遇到非法字段时整体失败。
8. 关掉生成脚本后，前端仓库里没有第二份手写的榜。
