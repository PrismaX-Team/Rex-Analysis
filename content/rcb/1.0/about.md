# 任务包

RCB 公开 40 题，十个领域，每个领域四题。编号从 `Astronomy_000` 到 `Physics_003`。

一个任务是一个目录：

```text
tasks/<Domain>_<NNN>/
  task_info.json     题面和数据说明
  data/              只读输入
  related_work/      参考文献
  target_study/      评分材料，不公开
```

求解器只看得到前三项。它需要交出 `report/report.md` 和 PNG 图。

本站任务页只展示 `task_info.json` 里的公开字段。目标论文、checklist 和参考图不在这个站上。

# 评分

分数叫 RADS，0 到 100。裁判模型按隐藏 checklist 的权重给每条打分，再汇总。

50 分是分界线。50 以下是 Re-Discovery：在复现原论文，分数表示复现到了几成。50 以上是 New-Discovery：报告里的证据超过了原论文，70 分以上表示明显超过。高于 50 只说明证据更强，不是已经证实的新发现。

排行榜里 50 分以下的格子是蓝色，50 分及以上是绿色；「New」一列是这次提交有几道题达到 50。

条目是文本或图像，属于定性评分。

## Pass@1 与 Pass@5

主榜是 Pass@1：每题跑一次。Pass@5 每题跑五次取最高分，失败或未评分的尝试按 0 计，同时给出五次的平均分和标准差，用来看结果的稳定性。Pass@5 目前只覆盖部分独立大模型，两种分数不能直接横比。

# 提交

第一版不在网页上收结果。一次完整提交需要覆盖这一版的全部题目，并给出每次运行的公开均分。分题报告仍以原项目站为准。

原项目站：https://internscience.github.io/ResearchClawBench-Home/

任务包：https://github.com/InternScience/ResearchClawBench
