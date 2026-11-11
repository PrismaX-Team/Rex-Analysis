// UI text in both languages, keyed by the Chinese source string so an untranslated
// string still renders (in Chinese) instead of showing a raw key.
// Long-form prose lives in content/*.en.md instead; data files carry their own *_en fields.

export const dict = {
  // Chrome -------------------------------------------------------------------
  "主导航": { en: "Main navigation" },
  "排行榜": { en: "Leaderboard" },
  "评测说明": { en: "About" },
  "说明": { en: "About" },
  "任务": { en: "Tasks" },
  "提交科学问题 ↗": { en: "Submit a question ↗" },
  "切换到浅色": { en: "Switch to light" },
  "切换到深色": { en: "Switch to dark" },
  "浅色": { en: "Light" },
  "深色": { en: "Dark" },
  "当前": { en: "Current" },
  "历史": { en: "Earlier" },
  "规划中": { en: "Planned" },
  "中文": { en: "中文" },
  "English": { en: "English" },
  "切换语言": { en: "Switch language" },

  // Home ---------------------------------------------------------------------
  "已上线": { en: "is live" },
  "面向科研智能体的评测平台。真实研究任务，独立完成，公开评分。": {
    en: "An evaluation platform for research agents. Real research tasks, solved independently, scored in the open.",
  },
  "浏览评测榜单": { en: "Browse the leaderboards" },
  "查看全部 Benchmarks": { en: "All benchmarks" },
  "向下浏览": { en: "Scroll" },
  "评测榜单": { en: "Leaderboards" },
  "每个 bench 一张榜，自动轮播，鼠标停留时暂停。": {
    en: "One board per bench. Rotates automatically; pauses on hover.",
  },
  "排行榜轮播": { en: "Leaderboard carousel" },
  "切换榜单": { en: "Switch board" },
  "上一个": { en: "Previous" },
  "下一个": { en: "Next" },
  "榜单将在 bench 上线后出现": { en: "Board appears once the bench is live" },
  "完整榜单 →": { en: "Full board →" },
  "道任务已公开": { en: "tasks published" },
  "成绩公开后，这里会显示前五名。": { en: "The top five appear here once scores are published." },
  "浏览任务 →": { en: "Browse tasks →" },
  "个已上线，更多 bench 正在筹备。点卡片进入该 bench 的榜、题和说明。": {
    en: " live; more benches in preparation. Open a card for its board, tasks and notes.",
  },
  "即将上线的 bench": { en: "Bench coming soon" },
  "新的 bench 筹备中": { en: "New bench in preparation" },
  "新的研究任务包正在准备。上线后，这里会显示它的前五名。": {
    en: "A new task set is being prepared. Its top five appear here once live.",
  },
  "进入 →": { en: "Open →" },

  // ReX block ----------------------------------------------------------------
  "关于 ReX": { en: "About ReX" },
  "ReX 科学共研计划：把真实的科研难题交给模型和智能体，先和提出者对齐目标，再攻关、再验证。": {
    en: "ReX, a joint research programme: real research problems are handed to models and agents. Goals are agreed with the proposer first, then attacked and verified.",
  },
  "ReX 科学共研计划 · 上海人工智能实验室": { en: "ReX joint research programme · Shanghai Artificial Intelligence Laboratory" },
  "是 Research，也是 Recursive：求解、验证、反馈，循环往复。": {
    en: "stands for Research and for Recursive: solve, verify, feed back, repeat.",
  },
  "是任意一个科学任务。": { en: "stands for any scientific task." },
  "榜": { en: "board" },
  "研究者提交科学问题，书生·端砚调用基础模型、科学智能体和算力去攻关。每次合作只盯一个可独立验证的阶段目标，": {
    en: "A researcher submits a scientific question; Intern·Discovery brings foundation models, scientific agents and compute to bear. Each collaboration targets a single independently verifiable milestone, ",
  },
  "开工前先约定问题、可用的数据和条件，以及怎样算成功。": {
    en: "with the question, available data and conditions, and the definition of success agreed up front.",
  },
  "提交科学问题": { en: "Submit a scientific question" },
  "中英文均可": { en: "Chinese or English" },
  "合作流程": { en: "How a collaboration runs" },
  "成果再发现": { en: "Rediscovery" },
  "求解与创新": { en: "Solve and innovate" },
  "原创突破": { en: "Original breakthrough" },
  "开放问题": { en: "Open problem" },
  "隐去原结论，只给已有数据，看能否把关键发现重新做出来。": {
    en: "Hide the original conclusions, supply only the data, and see whether the key findings can be reproduced.",
  },
  "通过计算、分析或有限的湿实验，在开放问题上拿到可度量的进展。": {
    en: "Make measurable progress on an open problem through computation, analysis or limited wet-lab work.",
  },
  "提出原创假设，并用真实的湿实验去检验。": {
    en: "Propose an original hypothesis and test it in real wet-lab experiments.",
  },
  "提交科学问题": { en: "Submit a scientific question" },
  "评估并约定目标": { en: "Assess and agree goals" },
  "攻关与验证": { en: "Attack and verify" },
  "交付阶段报告": { en: "Deliver the milestone report" },
  "在 ReX 页面填写表单：团队信息、科学问题与阶段目标、任务设计与验证方式，并附一个带 README 的任务包。": {
    en: "Fill in the ReX form: team, scientific question and milestone, task design and verification, plus a task package with a README.",
  },
  "团队评估问题的科学价值、可行性和资源需求，与提出者商定任务等级、技术对接方式和阶段目标。": {
    en: "The team assesses scientific value, feasibility and resources, then agrees the level, technical setup and milestone with the proposer.",
  },
  "调用基础模型和科学智能体求解，每一步结果按事先约定的指标验证，不达标就回到求解。": {
    en: "Foundation models and scientific agents work the problem; every step is checked against the agreed metrics, and a miss sends it back.",
  },
  "交付阶段报告。经授权后，评测结果、失败案例和专家反馈会用于改进模型与智能体。": {
    en: "A milestone report is delivered. With permission, results, failure cases and expert feedback feed back into the models and agents.",
  },

  // Home: overall board, coverage, how ----------------------------------------
  "每个 bench 的模型前五名。分数只在同一个 bench 内可比。": {
    en: "Top five models per bench. Scores are comparable only within a bench.",
  },
  "覆盖领域": { en: "Field coverage" },
  "所有数据集的学科版图。": { en: "The disciplinary map behind the tasks." },
  "如何参与": { en: "Get involved" },
  "不论你是来看结果，还是来提交自己的智能体，都从这三步开始。": {
    en: "Whether you are here for the results or to submit your own agent, start with these three steps.",
  },
  "选一个 bench": { en: "Pick a bench" },
  "每个 bench 测一种科研能力。先读它的说明页：任务长什么样、怎么评分。": {
    en: "Each bench measures one research capability. Read its notes first: what the tasks look like and how they are scored.",
  },
  "读评测说明 →": { en: "Read the notes →" },
  "跑完全部任务": { en: "Run every task" },
  "下载公开任务包，让你的智能体独立完成每一题，按格式交出报告和结果文件。": {
    en: "Get the public task packages, have your agent complete each task independently, and submit reports and result files in the required format.",
  },
  "选一个 bench →": { en: "Pick a bench →" },
  "评分并上榜": { en: "Score and get listed" },
  "用官方评测流程打分，把完整运行目录发给我们，核对后进入排行榜。": {
    en: "Score with the official pipeline, send us the full run directory, and the entry goes on the board once checked.",
  },
  "看排行榜 →": { en: "See the board →" },
  "各 bench 的分数不可横比，评分规则见各自的说明页。": {
    en: "Scores are not comparable across benches; scoring rules are on each bench's notes page.",
  },
  "联系我们": { en: "Contact us" },

  // Leaderboard --------------------------------------------------------------
  "按均分排名。点一行展开分题成绩。": { en: "Ranked by mean score. Open a row for per-task results." },
  "计分方式": { en: "Scoring mode" },
  "每题一次": { en: "one run per task" },
  "五次取最好": { en: "best of five" },
  "先看任务 →": { en: "See the tasks →" },
  "这一版还没有公开提交。": { en: "No public submissions for this version yet." },
  "智能体": { en: "Agents" },
  "模型": { en: "Models" },
  "提交": { en: "submissions" },
  "个": { en: "" },
  "道题越过 50 分": { en: "tasks above 50" },

  // Table --------------------------------------------------------------------
  "均分": { en: "Mean" },
  "单题成本": { en: "Cost / task" },
  "单题用时": { en: "Time / task" },
  "题数": { en: "Tasks" },
  "来源": { en: "Source" },
  "模型 ": { en: "Model" },
  "分题成绩": { en: "Per-task results" },
  "未评分": { en: "Not scored" },
  "本题全榜最高": { en: "Best on this task" },
  "社区": { en: "Community" },
  "内测": { en: "Internal" },
  "查看这次提交 →": { en: "Open this run →" },
  "分数达到 50（原论文证据水平）的题数": { en: "Tasks scoring 50 or more (paper-level evidence)" },
  "五次尝试的单题平均分 ± 标准差": { en: "Mean ± std of all five attempts" },
  "单次均值 ± σ": { en: "Mean ± σ" },
  "悬停小格看五次尝试的分数、均值 ± 标准差和最低 / 最高": {
    en: "Hover a cell for the five runs, mean ± std, and min / max",
  },
  "Pass@5 学科格：上为五次取最好的均分，下为全部尝试的均值 ± 标准差": {
    en: "Pass@5 cells: best-of-five on top, mean ± std of all attempts below",
  },
  "颜色图例": { en: "Colour legend" },
  "学科均分": { en: "Domain mean" },
  "未评分 ": { en: "Not scored" },
  "这一版还没有公开任务。": { en: "No public tasks for this version yet." },
  "全部": { en: "All" },
  "查看题面 →": { en: "Open →" },
  "个数据文件": { en: "data files" },

  // Overall board ------------------------------------------------------------
  "Benchmark": { en: "Benchmark" },
  "分类": { en: "Category" },
  "详情": { en: "Details" },
  "查看 →": { en: "Open →" },
  "暂无公开成绩": { en: "No public scores yet" },

  // Cost chart ---------------------------------------------------------------
  "分数与成本": { en: "Score and cost" },
  "横轴是单题成本（对数刻度），纵轴是均分，点的面积表示单题用时。连线是 Pareto 前沿：在不多花钱的前提下分数最高的那些提交。": {
    en: "Cost per task on a log scale against mean score; point area is time per task. The line is the Pareto frontier: the submissions that score highest without costing more.",
  },
  "单题成本（美元，对数刻度）": { en: "Cost per task (USD, log scale)" },
  "Pareto 前沿": { en: "Pareto frontier" },
  "其他提交": { en: "Other submissions" },
  "面积 = 单题用时": { en: "Area = time per task" },
  "在 Pareto 前沿上": { en: "On the Pareto frontier" },

  // Field coverage -----------------------------------------------------------
  "科学领域": { en: "Fields" },
  "二级领域": { en: "Sub-fields" },
  "覆盖从基础科学到医学与工程的主要学科；条形是已上线的 RCB 任务数。": {
    en: "Major fields from basic science to medicine and engineering; bars are live RCB tasks.",
  },
  "各领域已上线的任务数": { en: "Live tasks per field" },
  "已有任务的领域": { en: "Fields with tasks" },
  "RCB 已上线": { en: "RCB live" },

  // Run page -----------------------------------------------------------------
  "← 排行榜": { en: "← Leaderboard" },
  "← 全部任务": { en: "← All tasks" },
  "分题分数尚未迁入。": { en: "Per-task scores not imported yet." },
  "社区提交": { en: "Community" },
  "在原项目站查看报告 ↗": { en: "Report on the project site ↗" },
  "模型 ": { en: "Model" },
  "日期": { en: "Date" },
  "没有这次提交。": { en: "No such run." },
  "竖线是 50 分：左边是 Re-Discovery（复现原论文），右边是 New-Discovery（证据超过原论文）。": {
    en: "The tick marks 50: left is rediscovery (matching the paper), right is new discovery (evidence beyond it).",
  },

  // Tasks / Task -------------------------------------------------------------
  "研究任务": { en: "Research task" },
  "数据": { en: "Data" },
  "数据文件": { en: "Data files" },
  "学科": { en: "Field" },
  "版本": { en: "Version" },
  "类型": { en: "Type" },
  "复现": { en: "Reconstruction" },
  "发现": { en: "Discovery" },
  "抽象": { en: "Abstraction" },
  "没有这一题。": { en: "No such task." },
  "公开任务包": { en: "Public task package" },
  "项目仓库": { en: "Project repository" },

  // About pages --------------------------------------------------------------
  "目录": { en: "Contents" },
  "这一版的任务包长什么样、怎么评分、怎么提交。": {
    en: "What a task package looks like, how it is scored, how to submit.",
  },
  "全站通用的规则在这里。每个 bench 的任务格式和评分细则，在它自己的说明页。": {
    en: "Rules that apply to the whole site. Task format and scoring for each bench are on its own notes page.",
  },
  "各 bench 的说明": { en: "Each bench's notes" },
  "评分规则 →": { en: "Scoring rules →" },
  "每个 bench 一张榜。这里是各榜的前五名，点一行进入该 bench 的完整榜。": {
    en: "One board per bench. Top five of each; open a row for the full board.",
  },
  "各 bench 的分数只在同一个 bench 内可比，不合成总分。": {
    en: "Scores are comparable only within a bench; no combined total.",
  },
  "各 bench 的完整榜": { en: "Full boards" },
  "完整榜 →": { en: "Full board →" },

  // AFE ----------------------------------------------------------------------
  "设计哲学": { en: "Design philosophy" },
  "一个能够持续向前的 Benchmark": { en: "A benchmark designed to keep moving" },
  "任务特性": { en: "Task requirements" },
  "一道题要满足四个条件": { en: "Four conditions every task must meet" },
  "科学重要性": { en: "Scientific importance" },
  "结果变好后，应能推进真实研究问题或重要科学计算瓶颈。": {
    en: "A better result should advance a real research question or a significant computational bottleneck.",
  },
  "Verifier 可信度": { en: "Verifier credibility" },
  "评分算法、输入、常数、容差、聚合和无效输出处理能够完整固定，并在本地、离线、确定性运行。": {
    en: "The scoring algorithm, inputs, constants, tolerances, aggregation and invalid-output handling are fully fixed and run locally, offline and deterministically.",
  },
  "前沿空间": { en: "Frontier headroom" },
  "当前最佳可达结果仍未知，并有可信证据表明存在实质改进空间。": {
    en: "The best attainable result is still unknown, and there is credible evidence of substantial room for improvement.",
  },
  "长期可持续性": { en: "Long-term sustainability" },
  "数据、软件和验证路径能够稳定获得，不依赖脆弱服务、秘密凭证或不可重复的外部行为。": {
    en: "Data, software and the verification path remain reliably available, without fragile services, secret credentials or irreproducible external behaviour.",
  },
  "团队": { en: "Team" },
  "由身处科学前沿的专家共同支持": { en: "Supported by experts working at the scientific frontier" },
  "由身处科学前沿的专家共同支持。": { en: "Supported by experts working at the scientific frontier." },
  "在未解决的科学问题上持续突破。": { en: "Advancing unsolved scientific problems." },
  "参与共建 ↗": { en: "Contribute ↗" },
  "评测说明 ↗": { en: "About ↗" },
  "顾问委员会": { en: "Advisory committee" },
  "支持任务遴选、科学审核与评测可信度。": {
    en: "Supports task selection, scientific review and evaluation credibility.",
  },
  "学术委员会": { en: "Academic committee" },

  // AFE design philosophy (from the AFE task site) ---------------------------
  "评测的不是解决办法明确的静态题目，而是仍未解决、并值得不断推进的真实前沿问题。": {
    en: "The benchmark targets real frontier questions whose solutions remain open and worth advancing, not static problems with known solution paths.",
  },
  "在开放环境下，模型可以检索调研问题的前沿方法，公开前沿是研究的起点，而不是需要隔离的信息。": {
    en: "Agents can investigate frontier methods in an open environment. Public knowledge is the starting point of research, not information to isolate.",
  },
  "评分规则固定，但比较坐标持续更新；每个结果都相对于其他 Agent 和当前前沿进行衡量。": {
    en: "Scoring rules stay fixed while the comparison frame keeps moving; every result is measured against other agents and the current frontier.",
  },
  "Benchmark 不是一次性封闭发布的题库，而由研究者、领域专家等贡献者持续共同发现、构建和完善。": {
    en: "The benchmark is not a closed, one-off task set. Researchers, domain experts and other contributors continuously discover, build and improve it together.",
  },
  "评测关注的不是完成既定步骤，而是 Agent 能否把调研转化为经过验证的改进，在尚未解决的科学问题上取得可衡量的进展。": {
    en: "The benchmark measures whether an agent can turn investigation into a tested improvement that makes measurable progress on an unresolved scientific problem.",
  },
  "Verifier 在运行前冻结，并在离线环境中评分；相同的冻结输入、Validation 历史、Context 和提交必须得到相同结果。": {
    en: "The verifier is frozen before a run and scores offline. The same frozen input, validation history, context and submission must produce the same result.",
  },
  "资源和网络边界预先固定，研究过程被完整记录与审计，防止 hacking、访问隐藏输入或通过绕过约束获得虚假高分。": {
    en: "Resource and network boundaries are fixed, and the research process is recorded and audited to prevent hacking, hidden-input access and invalid high scores.",
  },
  "Live Question": { en: "Live Question" },
  "Live Environment": { en: "Live Environment" },
  "Live Metric": { en: "Live Metric" },
  "Live Community": { en: "Live Community" },
  "Innovation": { en: "Innovation" },
  "确定性验证": { en: "Deterministic verification" },
  "受控评测": { en: "Controlled evaluation" },

  // RCB ----------------------------------------------------------------------
  "任务星图": { en: "Task map" },
  "RCB · 任务星图": { en: "RCB · Task map" },
  "1.0 任务星图：十个学科，四十道题，方法线连接跨学科的题": {
    en: "1.0 task map: ten fields, forty tasks, threads linking tasks across fields",
  },
  "← 返回": { en: "← Back" },
  "展开星图": { en: "Open the map" },
  "四十篇论文，": { en: "Forty papers," },
  "散落在十个学科。": { en: "scattered across ten fields." },
  "我们从十个学科各选了四篇论文，把每一篇还原成一个研究任务，交给智能体从头做一遍。": {
    en: "Four papers from each of ten fields, each turned back into a research task and handed to an agent to redo from scratch.",
  },
  "放在一起看，它们并不孤立。同一种方法会在不同学科里反复出现：图神经网络从分子走到晶体，": {
    en: "Seen together they are not isolated. The same method recurs across fields: graph networks travel from molecules to crystals ",
  },
  "又走到网络流量；连接组既是神经科学的问题，也是视觉的问题。图上的每一条彩线，都是这样一次跨界。": {
    en: "and on to network traffic; a connectome is a neuroscience question and a vision question at once. Every coloured thread on the map is one such crossing.",
  },
  "跨学科的线索": { en: "Threads across fields" },
  "停在一颗星上，看它是哪项研究；点一下把它留在这里。": {
    en: "Rest on a star to see which study it is; click to pin it here.",
  },
  "已选中 · 再点一次取消": { en: "Pinned · click again to release" },
  "点击可选中": { en: "Click to pin" },
  "它在这张图上独自成星。": { en: "It stands alone on this map." },
  "排行榜 →": { en: "Leaderboard →" },
  "看排行榜": { en: "Leaderboard" },
  "越过原论文": { en: "Beyond the paper" },
  "前沿（全榜每题最高分）达到 50 的题数": {
    en: "Tasks where the best score on the board reaches 50",
  },
  "每个任务包来自一篇真实的论文：题面、数据、相关工作都给你，答案藏在评分清单里。": {
    en: "Every task comes from a real paper: statement, data and related work are given, the answers sit in a hidden checklist.",
  },
  "智能体要像研究者一样，独立把这项研究做一遍。": {
    en: "The agent has to do the study again, on its own, the way a researcher would.",
  },
  "RADS · 0–100 · 50 以下 Re-Discovery，50 以上 New-Discovery": {
    en: "RADS · 0–100 · below 50 is rediscovery, above 50 is new discovery",
  },
};

export function translate(text, lang) {
  if (lang === "zh") return text;
  return dict[text]?.[lang] ?? text;
}
