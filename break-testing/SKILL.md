---
name: break-testing
description: Hunts for bugs in a built feature by using the running system — web UI, API or CLI — the way real users and hostile clients would, and reports each bug with steps to reproduce. Use when asked to try to break a feature, run a bug-bash, a QA pass or exploratory testing, hunt for edge cases, or test a whole feature before release. Not for the quick check of a single change, before calling it done or while exercising it inside a code review.
---

# Break Testing

Try to break this feature through the running system, and report every bug with steps someone else can follow. Report only; fix nothing.

Before the first action, make sure you can run to the end without the human: signed in as a test account, on test data, on a build nobody else is changing. If you can't arrange that yourself, stop and say what is missing. If the build changes mid-run, re-confirm what you found.

Reach every state only by means a real user or client has; a script may click real controls and read state. A result that needed a called handler, hand-written storage, emulated input or a dev-only build is a lead to confirm the real way, not a bug.

Report only what you watched happen, worst first. Re-run each bug once from a clean state, or say it was seen once, and give what the spec says should have happened. Run the previous build before saying anything about it. Keep improvement ideas, and behavior the spec doesn't decide, apart from the bugs, as questions for the human. Say "works" only about the exact cases you ran, and list the rest as not tested.

Finish by removing your test data and showing it is gone.
