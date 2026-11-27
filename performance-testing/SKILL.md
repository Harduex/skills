---
name: performance-testing
description: Load-tests and benchmarks a change in the running system, on any layer (UI, API, database, background jobs, queues, scripts), to find out how it and the components around it behave as data, users or traffic grow, and decides first whether such a test is worth running at all. Use when asked to load-test, stress-test, benchmark or performance-test a feature, endpoint, query or job, to find out how a change scales or where it gets slow, or when a change adds work whose cost grows with items, users, requests, concurrency or frames and is about to ship.
---

# Performance Testing

Find out how this change behaves under growing load, and where the cost really lands. Measure and report; fix nothing.

**Decide first.** Run when the change adds work that grows with something: rows stored or rendered, requests, concurrent users, payload size, per-frame or per-keystroke work, new queries, jobs or assets. Skip when the cost cannot grow, such as copy, styling or logic over small fixed inputs. Say in one line which it is and why. When asked to run it anyway, run it.

**Map what the load touches, on every layer.** Follow the feature's data from where it is written to every place it is read, stored, sent or drawn: endpoints, queries and their indexes and limits, jobs, caches, sync, and the screens that show it. The feature's own code is one target. The components that handle the same data are the other: the other readers and writers of the same tables, the pools and locks they share, the lists and renderers that draw it. The cost often shows there, not in the new code.

**Measure before loading.** Record a baseline with the same script you will rerun at each step, and note what can skew it: dev or production build, hardware, cold or warm caches, a display refresh cap.

**Load the way real use would, in steps.** Create the data through the system's own write path. Cover every option the feature offers and its worst cases (largest, longest, most varied). Mark the data so it can be found. Grow two things separately, the amount of data and the number of simultaneous users or requests, in steps such as realistic, heavy and beyond. Rerun the same measurements at each step. Before changing data other people use, say so. Follow the requester's instruction on keeping or removing it.

**Check that the load landed.** Compare what you wrote with what the system returns and shows. A silent limit, cap, missing page or lost write is a finding.

**Measure what users and callers feel.** Pick metrics for the layer: latency percentiles, throughput and error rate for an endpoint; query time and plan for the database; wall time and memory for a job; frame time and long tasks for a UI. Measure while the data is in use: concurrent reads and writes, the job running next to normal traffic, interacting with and listing it on screen. Idle numbers alone prove little. A fast machine hides costs, so repeat the key measurements with less CPU, a weaker device or a smaller pool.

**Attribute before you blame.** Profile each slow moment and split its cost between the feature's code and the rest. Check whether the hot code is part of this change. Report an older bottleneck as older, and never blame the feature for it.

**Report**, worst first:
- A table of the baseline against each load step.
- The feature's own cost as a number.
- Each finding, with its evidence and whether this change caused it.
- What you did not test.
- The data you left behind and how to remove it.

Say "fast enough" only about what you measured, and call dev-build numbers relative.
