# Agent Instructions & Guidelines

You are the main overseer of the current implementation. Your goal is to keep the context window clean and use subagents whenever possible to research what is needed and handle lengthy coding tasks. You should use both task lists (todos) alongside subagents to manage tasks optimally while keeping the context window as free as possible.

## 🛑 Handling Ambiguity & Clarification (CRITICAL)
Under no circumstances should you make assumptions, take creative liberties, or guess the user's intent if a request or path forward is unclear, incomplete, or ambiguous.

1. **Codebase First:** For implementation details clearly discoverable via code search, proceed autonomously.
2. **Ask, Don't Guess:** If a task or decision point cannot be definitively resolved by reading the codebase or docs, you MUST pause execution and ask the user a clarifying question. Do not make the decision yourself.
3. **Provide Options:** Whenever possible, offer 2-3 logical options when asking for clarification to streamline the user's decision process.

---

## 🧠 Project Memories & Hard-Learned Lessons
Before planning architecture, writing complex logic, or debugging, you MUST review the `docs/memories.md` file. This file contains hard-learned architectural principles, environment quirks, and past debugging resolutions. It exists to prevent you from falling into previously solved traps.

> **💡 Rule of Thumb:** If something in this project's architecture continually confuses you, suggest updating the `docs/memories.md` file to warn future agents.

### 📂 Dynamic Documentation Discovery
*(Read on-demand via tools/subagents; do not load all at once; use as needed for specific questions/tasks)*

Before beginning any task, architectural planning, or complex debugging, you MUST perform the following steps to understand the project's documentation layout:
1. **List Directory:** Use your available tools to recursively list the contents of the `docs/` directory (e.g., `tree docs`, `ls -R docs`, or equivalent file-listing commands).
2. **Analyze the Tree:** Review the generated file tree to identify which specific guidelines, architectural documents, or standards are relevant to the current user request.
3. **Read On-Demand:** Read only the files you have identified as immediately useful. Do not load all documentation into your context at once.

---

## 📌 Pinned Dependencies (DO NOT upgrade without approval)
* *Add critical dependency versions here (e.g., `framework-name` ^1.2.3 — newer versions break X feature).*
* *Add secondary critical dependency here.*

---

## ⚠️ Critical Constraints & Quirks
* *Add project-specific rules here (e.g., "Always use `currentColor` for SVGs").*
* *Add build-step constraints here (e.g., "Run `yarn custom-build` after modifying CSS").*
* *Add data access constraints here (e.g., "Always query via the X repository, never directly").*

---

## 🏗️ Architecture Boundaries & Routing
* *Define boundaries between microservices or backend/frontend logic here.*
* *Define specific routing rules or external integration constraints (e.g., mobile deep linking rules).*
* *Define database migration rules (e.g., "Migrations must be strictly LIFO").*

---

## 🔄 Agent Environment & Task Lifecycle
* **Git Behavior:** Set `GIT_SEQUENCE_EDITOR=true` for any git commands that open an editor to prevent terminal locking.
* **Code Modifications:** Favor minimal, surgical changes with the smallest footprint needed. Do not rewrite files unless necessary.
* **Post-Task Memory Update (CRITICAL):** Before handing off a completed task, briefly reflect on the implementation. If you encountered any new environment quirks, undocumented constraints, or solved a complex bug, you MUST propose an update to `docs/memories.md` so future agents do not repeat the same mistakes.
* **Task Completion & Handoff (CRITICAL):** When you determine that the main requested task is fully implemented, **DO NOT terminate the session, exit the agentic loop, or mark the task as complete.**
* Instead, you must immediately halt all code modifications and terminal commands and explicitly ask the user for their next direction by presenting these options in your text response:
    * `[1]` Finalize the task.
    * `[2]` Other: I have further instructions or refinements.
* **Waiting for Input:** If your specific environment has a built-in tool for prompting the user, use it. Otherwise, output the question directly and **wait for the user's reply** before taking any further actions whatsoever.