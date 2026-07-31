---
name: filming-verification
description: Record a short, caption-annotated screen video that proves a change works, instead of a written test report. Use when asked to film/record/screen-capture a verification run, to show a change working, or to produce a walkthrough a reviewer can watch; also use to decide whether a verification artifact should be a video, chat prose, or a file at all — and before writing any test/verification report to disk.
---

# Filming Verification

A film is a verification artifact for a **human who wasn't watching**. Each step burns its
*measured* value into the frame, so the video reads without a transcript beside it.

It replaces the written test report — never produce both.

## Decide first: film, prose, or nothing

| Situation | Deliverable |
|---|---|
| Change is user-visible (UI, copy, a flow) **and** prose wouldn't settle it | **Offer** a film |
| Human explicitly asks to see it / for a video | Film |
| Backend, schema, refactor, test-only, or the diff speaks for itself | Chat prose. Don't mention filming |
| Verification for the person you're talking to | **Chat prose with stable IDs** (`TC-3`, `F2`) they can reply to |
| A reader who is *not* in the conversation (MR body, ticket, PM handoff) | Written artifact is justified |

**Never film unprompted.** Offer once, in one sentence, and drop it if declined — a film
costs a full run plus a transcode. **Never write a verification report to disk unless the
human asked or a non-participant will read it** — the same bar your set's
verify-before-claiming-done workflow applies to evidence.

Before filming, check what will be on screen: a recording captures whatever is visible,
including tokens, other people's data, and unrelated tabs. Say so if the flow touches any.

## The method

1. **Pick the driver** — prefer one that *asserts* (see Drivers). A film that only shows
   pixels can display a confident caption over a broken app.
2. **Script the run as numbered steps.** Each step: navigate → measure → caption → hold.
3. **Caption with measured values, never expected ones.** Read the value from the live
   DOM/response and print *that*. A caption echoing the claim is theatre — the whole point
   is that the frame shows what the app actually returned.
4. **Suppress first-run chrome** — welcome dialogs, "what's new" modals, dev overlays.
   They cover every frame. Restore the storage state your login flow saved.
5. **Hold each caption ~2.5s.** Long values (MIME lists, JSON) need the time.
6. **Verify the film before delivering it** — extract 2–3 frames and *look at them*. This
   is not optional: a blocking modal or a clipped caption is invisible until you look.
7. **Speed up to the readability ceiling, not to a round number.** Captions dominate the
   runtime, so the ceiling is usually **~1.5x**. Report the final duration. If the human
   wants faster, they want a shorter script, not a faster one.
8. **Tear the harness down** — delete the temp config/spec, leave the tree clean, and say
   the film's path.

## Where the artifact goes

- `docs/reports/<date>-<slug>/` (or the project's equivalent), **untracked**.
- Never `git add` a film unless asked — video bloats history and is worthless post-merge.
- **No text report, no screenshot gallery, when a film exists.** One artifact.
- If an untracked artifact under the reports directory disappears mid-session, **assume the
  human removed it**. Say so in one line and move on. Do not probe the filesystem, git, or
  your own tooling, and do not recreate it.

## After the film

List the filmed cases the automated suite does **not** cover, and offer to promote them to
real tests. Filming walks surfaces nobody wrote specs for — that discovery is worth more
than the video. Don't add the specs unasked.

## Drivers

Bind the concrete details from the project's own test skill; only the shape is generic.

**A — Test runner with built-in recording** (Playwright, Cypress, …) — preferred, because
assertions fail the run when reality disagrees.

- Add a throwaway config that mirrors the project's existing secondary config (smoke,
  sanity) and turns recording on unconditionally, serial, one worker.
- Name the script so the suite does **not** collect it (e.g. `*.ts` where specs are
  `*.spec.ts`), and delete it afterwards. It is not a spec and must not be reviewed as one.
- **If the project's page objects build their own browser context, nothing records.**
  Recording is a context-creation option; a context made inside a POM's `init()` never sees
  the config. Swap in a recording context carrying the same stored auth and let the POM
  helpers drive it.
- Reuse fixtures for data and POM helpers for navigation — a film that hand-rolls setup
  drifts from what the suite actually asserts.

**B — Browser-automation MCP + OS screen recorder** — for projects with no suite.

- Drive the browser as usual; record the screen out-of-band.
- **It can show, not assert.** State that limitation when delivering, and read every value
  back into a caption so the frame still carries evidence.
- Wayland/X11 recorder availability varies; check before promising a film.

See [REFERENCE.md](REFERENCE.md) for the caption helper, the throwaway config, frame
extraction, and speed-up commands (ffmpeg and a GStreamer fallback for boxes without it).
