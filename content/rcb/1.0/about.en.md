# Task packages

RCB publishes 40 tasks across ten fields, four per field, numbered `Astronomy_000` through `Physics_003`.

A task is a directory:

```text
tasks/<Domain>_<NNN>/
  task_info.json     statement and data notes
  data/              read-only input
  related_work/      references
  target_study/      scoring material, not public
```

The solver sees only the first three. It must deliver `report/report.md` and PNG figures.

Task pages on this site show only the public fields of `task_info.json`. The target paper, the checklist and the reference figures are not here.

# Scoring

The score is called RADS, 0 to 100. A judge model scores each hidden checklist item by its weight and sums them.

50 is the dividing line. Below 50 is rediscovery: the report is reproducing the paper, and the score says how much of it was reproduced. Above 50 is new discovery: the evidence goes beyond the paper, and above 70 clearly so. A score above 50 means stronger evidence, not a confirmed new finding.

On the leaderboard, cells below 50 are blue and cells at or above 50 are green; the New column counts the tasks that reached 50.

Items are text or images, so scoring is qualitative.

## Pass@1 and Pass@5

The main board is Pass@1: one run per task. Pass@5 runs each task five times and takes the best, counting failed or unscored attempts as zero, and also reports the mean and standard deviation of the five attempts so stability is visible. Pass@5 currently covers only some standalone models, and the two scores cannot be compared directly.

# Submitting

The first version does not collect results on this site. A complete submission covers every task in the version and reports the public mean of each run. Per-task reports remain on the original project site.

Original project site: https://internscience.github.io/ResearchClawBench-Home/

Task packages: https://github.com/InternScience/ResearchClawBench
