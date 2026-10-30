---
name: teach
description: Teach the user a new skill or concept, within this workspace.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request - they intend to learn the topic over multiple sessions.

## Teaching Workspace

Treat the current directory as a teaching workspace. The state of their learning is captured in this directory in several files:

- `MISSION.md`: A document capturing the _reason_ the user is interested in the topic. This should be used to ground all teaching. Use the format in [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `./reference/*.html`: A directory of reference materials. These are the compressed learnings from the lessons - cheat sheets, reference algorithms, syntax, yoga poses, glossaries. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: A list of resources which can be explored to ground your teaching in contextual knowledge, or to acquire knowledge and wisdom. Use the format in [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./learning-records/*.md`: A directory of learning records, which capture what the user has learned. These are loosely equivalent to architectural decision records in software development - they capture non-obvious lessons and key insights that may need to be revised later, or drive future sessions. These should be used to calculate the zone of proximal development. They are titled `0001-<dash-case-name>.md`, where the number increments each time. Use the format in [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single HTML page, working offline, that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.
- `FEEDBACK.md`: The log of how the user did in each lesson: the questions they missed, how many tries each took, what they said was unclear, and which answers they asked to see. Append each lesson's follow-up prompt here when the user pastes it back. Read it before every lesson and at the start of every session: it shows what the user does not know yet, and how they like to be taught.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Before the `RESOURCES.md` is well-populated, your focus should be to find high-quality resources which will help the user acquire knowledge. Never trust your parametric knowledge.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

You should be careful to split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is the main thing you produce — the unit in which knowledge and skills reach the user. Each lesson is one HTML file that works offline when opened from disk (no CDN, no network calls; it may link the workspace's `./assets/`), saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time. If possible, open the lesson file for the user by running a CLI command.

Every lesson is an **interactive explorer**: a live picture of the real material, with a guided path of short steps on top of it. The user takes one idea at a time, sees it happen in the picture, and shows they understood it before moving on. Pages of text with a quiz at the end are what this replaces: they feel like a test, not like learning.

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development.

A lesson should be **beautiful** — clean, readable typography and layout — since the user will return to these later to review. The default look is dark with a light toggle, a system sans-serif for text, a monospace font for code and data, and one warm accent colour for what is active; [starter.css](./starter.css) sets it.

### The picture

Pick the picture the topic really has: a diagram of a system or a data model, code that runs, a simulation with a slider, a timeline, a sequence of poses. Build it from the real material (a schema, a config, real code, real measurements) wherever you can, so it stays true. Show each idea in the picture before explaining it. Motion carries change: light what takes part, move a marker along a link, play the before and after.

### Shape

- **Start screen.** Name the subject in plain, specific words, say in two lines what it is, and say what the user will be able to do at the end. Only then show how the lesson works, compactly rather than in sentences, and one obvious place to start. Free exploration stays available, but the guided path comes first.
- **Layout.** Two areas only: the picture, and one side pane beside it (below it on a phone). The pane holds everything that is words or controls: the step, its questions and feedback, Back and Next, the part map, the folded foundations, the legend, the zoom buttons, the lesson title and links, and the theme toggle. Nothing floats over the picture except the labels that belong to it.
- **Steps.** One idea per step, a caption of one or two sentences, and the parts it talks about lit in the picture. More detail appears on demand, never by default.
- **Parts.** A bigger topic splits into a few parts along one route. The first part teaches the foundations every later part relies on, on a small slice of the real material. After that, the foundations stay one click away, folded by default. The first step of each part says what it is, why it matters for the mission, and where it sits among its neighbours, on a small map.
- **Questions.** A question step follows each idea worth testing, plus one at the end of each part. See [Questions](#questions).

### Rules

1. **The view follows the step.** Each step brings what it talks about into the middle of the picture area with a short glide, so the eye follows instead of searching. The user's own pan, zoom or scroll always wins.
2. **The user sets the pace.** Nothing advances on a timer. Each step waits for an explicit Next, but the first step of a part is already on screen when it opens. The last step of a part leads straight on to the next one and names it.
3. **A detour or a refresh never costs the place.** Free exploration is allowed; coming back resumes at the step the user left, and says which. The address holds the part and the step, so a reload reopens them.
4. **Teach at the level of the subject, not below it.** Assume the user's general background. Define each term the subject brings in the first time it appears, with a small example in the subject's real shape, then state the rule. Use real output or real data where you have it; make an example up only when the real one is too big or not available, and say once that it is made up. When a mechanism of an underlying tool matters, give its effect in one clause instead of teaching it. Prefer more examples to fewer. Say a standing caveat once, where it is first needed.
5. **Every connection says what it joins.** When a link, an arrow or a cause is active, show what it joins at both ends and what kind of relation it is, so it has a meaning and not just a direction.
6. **Nothing covers what it explains.** Labels in the picture sit above everything, in free space, and keep clear of each other and of the lit parts at every window size. On a phone, the picture and the current step fit on one screen together, the step controls stay in reach, and the page never scrolls sideways.
7. **Format text and code so the eye lands on the step.** Code and raw output get quiet syntax colours (keywords, strings, comments, values) as spans, written by hand or by a small tokenizer of the lesson's own in `./assets/`, never a third-party highlighter. Inside a block, the line, token or field the step is about takes the accent and the rest dims, as in the picture; the accent wins over any other colour. One thing has one colour everywhere: give each kind of thing in the subject a colour in `course.css`, in cool hues that keep clear of the accent, with light-theme variants, and use it for that kind's names and identifiers and for each term where it is defined, in the caption text, the code and the picture alike. Leave everyday mentions of the word uncoloured. In running text, bold only a new term where it is defined and the verdict in feedback; headings and buttons keep their own weight.

### Questions

- The user commits first: picks a choice, or does the thing itself in the picture (clicks the part, sets the slider).
- While they look, nothing on screen hints at the answer: no highlight, no dimming. Written choices have the same number of words (and characters, if possible); when the answer is clicked in the picture, every candidate looks the same.
- Every wrong choice is a mistake people really make, and picking it explains that mistake without giving away the right answer.
- The path waits until the answer is right. After a wrong try, the user can keep trying, ask to be shown the answer, or say what is unclear. Nothing is scored.
- **Show me** marks the right answer; the user still picks it to move on, and the question counts as missed.
- **What is unclear.** After a wrong try, offer a small optional form: a few ready answers ("A term I don't know", "The wording of the question", "Which part it means", "I mixed it up with something else") and a free-text box. It stays available after the user gets the question right, since a question missed on the way can still leave something unclear. Asking never blocks the path.
- **The lesson keeps a log.** For every question it records each wrong answer in order, the number of tries until the right one, whether the answer was shown, and what the user said was unclear. Keep the log in the browser's storage too, so a refresh keeps it. The log feeds the follow-up prompt.
- A question the user never tries to answer tests nothing: always ask for an answer before anything is revealed.

### The follow-up prompt

At the end of every lesson, show a short prompt the user copies back to the agent, with a Copy button that falls back to selecting the text. This drives recursive learning: each lesson's mistakes become the next lesson. The prompt must tell an agent that reads nothing else what to teach next. It names the lesson, and for every question the user got wrong at least once it gives the question, each wrong answer they picked, the misunderstanding that answer stands for, the right answer, the number of tries, whether they asked to be shown, and what they said was unclear, in their words. It ends with what they got right first time. When nothing was missed, the prompt says so and names the next lesson on the route. Keep the planned route of lessons in `NOTES.md`.

```
Lesson 0003 HTTP caching: 2 of 5 questions missed at first.
- Q2 "Who decides a response may be cached?" picked "the browser alone" (thinks the client decides, not the server's headers), then "the proxy" (same idea); right: "the server's Cache-Control". 3 tries, asked to be shown. Unclear: "A term I don't know": "what counts as a proxy here?"
- Q4 "What does ETag let the client skip?" picked "the request" (confuses revalidation with expiry); right: "the body". 2 tries.
Right first time: Q1 freshness, Q3 max-age, Q5 private vs public.
Build a follow-up lesson that teaches the missed ideas in more depth, from a different angle, then re-tests them.
```

When the user pastes it back, append it to `FEEDBACK.md`, record the insight in a learning record, then build the follow-up lesson on those mistakes. Anything they said was unclear is a gap to close first.

### Before handing it over

Drive the lesson in a real browser at a desktop and a phone width, through every step, with your set's browser-driving skill if one exists: no page errors, nothing covers a lit part, each question unlocks only on its right answer, a reload keeps the place and the log, and the follow-up prompt lists exactly the mistakes, tries and unclear notes made.

### Links and sources

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch. This should be the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers — anything a second lesson could reuse.

Reuse is the default, not the exception. Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it — never inline code a future lesson would duplicate.

A shared stylesheet is the first component every workspace earns; start it by copying [starter.css](./starter.css) to `./assets/course.css`: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning about the topic.

If the user is unclear about the mission, or the `MISSION.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. This is normal - make sure to update the `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading their `learning-records`
- Figuring out the right thing to teach them based on their mission
- Teach the most relevant thing that fits in their zone of proximal development

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge should first be gathered from trusted resources. Use `RESOURCES.md` to keep track of them. Lessons should be littered with citations - links to external resources to back up any claim made. This increases the trustworthiness of the lesson.

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, with questions inside the path (see [Questions](#questions)) and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

## Acquiring Wisdom

Wisdom comes from true real-world interaction - testing your skills outside the learning environment.

When the user asks a question that appears to require wisdom, your default posture should be to attempt to answer - but to ultimately delegate to a **community**.

A community is a place (online or offline) where the user can test their skills in the real world. This might be a forum, a subreddit, a real-world class (budget permitting) or a local interest group.

You should attempt to find high-reputation communities the user can join. If the user expresses a preference that they don't want to join a community, respect it.

## Reference Documents

While creating lessons, you should also create reference documents. Lessons can reference these documents - they are useful for tracking raw units of knowledge useful across lessons.

Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

Glossaries, in particular, are an essential reference. Once one is created, it should be adhered to in every lesson.

## `NOTES.md`

The user will sometimes express preferences of how they want to be taught, or things you should keep in mind. This is the place to record those preferences, so you can refer back to them when designing lessons or working with the user.
