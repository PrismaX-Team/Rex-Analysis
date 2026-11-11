# What this bench measures

Measure true innovation at scientific frontiers where the optimum is still unknown.

Agent Frontier Exam evaluates whether research agents can independently investigate real, unresolved frontier problems in an open environment, propose and validate improvements, make measurable progress and advance the boundary of the problem.

# Design philosophy

A benchmark designed to keep moving.

- **Live Question**: the benchmark targets real frontier questions whose solutions remain open and worth advancing, not static problems with known solution paths.
- **Live Environment**: agents can investigate frontier methods in an open environment. Public knowledge is the starting point of research, not information to isolate.
- **Live Metric**: scoring rules stay fixed while the comparison frame keeps moving; every result is measured against other agents and the current frontier.
- **Live Community**: the benchmark is not a closed, one-off task set. Researchers, domain experts and other contributors continuously discover, build and improve it together.
- **Innovation**: the benchmark measures whether an agent can turn investigation into a tested improvement that makes measurable progress on an unresolved scientific problem.
- **Deterministic verification**: the verifier is frozen before a run and scores offline. The same frozen input, validation history, context and submission must produce the same result.
- **Controlled evaluation**: resource and network boundaries are fixed, and the research process is recorded and audited to prevent hacking, hidden-input access and invalid high scores.

# Task requirements

- **Scientific importance**: a better result should advance a real research question or a significant computational bottleneck.
- **Verifier credibility**: the scoring algorithm, inputs, constants, tolerances, aggregation and invalid-output handling are fully fixed and run locally, offline and deterministically.
- **Frontier headroom**: the best attainable result is still unknown, and there is credible evidence of substantial room for improvement.
- **Long-term sustainability**: data, software and the verification path remain reliably available, without fragile services, secret credentials or irreproducible external behaviour.

# Task packages

Every task is a Harbor-format package. `task.toml` is the configuration entry point and `instruction.md` is the agent-facing directive. The solving environment and the scoring environment are strictly isolated. Scoring runs once, offline and deterministically, against the frozen submission. The best attainable result is unknown in advance.

```text
task_package/
├── task.toml                 run configuration and artifact paths
├── instruction.md            task directive visible to the agent
├── environment/
│   ├── Dockerfile            solving environment definition
│   ├── input/                agent-visible inputs
│   └── tools/                agent tools (if any)
├── tests/
│   ├── Dockerfile            isolated scoring environment definition
│   ├── test.sh               scoring entry point
│   ├── check_outputs.py      scoring implementation
│   ├── input/                independent scoring input copy
│   └── tools/                scoring tools or judge (if any)
├── harness/                  integration conventions and scheduler adapters (if any)
└── solution/                 reference solution, private (if any)
```

- `task.toml`: run configuration — task name, authorship, resource limits, timeout, network mode, and artifact paths.
- `instruction.md`: the complete task directive for the agent, including input description, output format, constraints, and success criteria.
- `environment/`: build context for the solving image. The Dockerfile installs runtime dependencies; `input/` holds the agent-visible scientific inputs; `tools/` holds agent-callable tool code and interface documentation (when present).
- `tests/`: build context for the scoring image, isolated from the solving environment. Agent modifications to the solving inputs do not affect the scoring baseline. Scores are written to `/logs/verifier/reward.json`; detailed records go to `metrics.json`.
- `harness/`: integration conventions and any external scheduler adapter, documenting how the task connects to Harbor or another orchestration framework (when present).
- `solution/`: reference solution for oracle validation only; never copied into the solving image (when present).

# Contributing

Help us find important frontier scientific problems and turn them into evaluable AFE task packages.

Send the problem to Intern·Discovery, which brings models and agents to bear: see [Submit a scientific question](https://discovery-home.intern-ai.org.cn/home/event/rex/index.html).
