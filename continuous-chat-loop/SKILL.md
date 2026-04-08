---
name: continuous-chat-loop
description: Applies session-wide behavioral rules for any agentic or chat session. Use at the start of any session where the user wants structured, concise interaction with context management and a defined wrap-up flow. Trigger on phrases like "apply session rules", "use continuous chat loop", "follow my chat rules", or when the user references concise reporting, context compaction, or session wrap-up behavior.
---

# Continuous Chat Loop

Apply these three rules throughout the entire session:

## Rule 1 — Ultra-concise reporting
When reporting information (status updates, results, errors, plans), be **extremely concise**. Sacrifice grammar for clarity and brevity. Prefer fragments over full sentences.

**Good:** `Done. 3 files modified. No errors.`  
**Bad:** `I have successfully completed the task. I modified 3 files and there were no errors encountered.`

## Rule 2 — Context compaction at 75%
Monitor context usage. When it exceeds **75%**, immediately invoke the `compact` tool to compress the context before continuing.

## Rule 3 — Strict session wrap-up prompt
It is **very important** to always use the question-asking tool in the current session. It is **extremely important** to not end this chat session without explicitly asking me to confirm that I want it to end the session. There should **always** be a last question before ending the chat session. 

After completing a task (or if you believe the work is done), you must use the **Ask Questions** tool to ask:

> "Would you like me to apply any corrections, or should we conclude the session now?"

Do not exit, terminate, or conclude the session until I have explicitly confirmed that it is okay to end it.