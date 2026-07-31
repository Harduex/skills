# Naming: the Controlled Vocabulary

A codebase is a controlled language: a closed set of approved terms, each with
one meaning, extended only through a deliberate act (a glossary entry). These
rules keep the vocabulary closed.

## Rules

| ID | Rule |
|---|---|
| N1 | Every name comes from an approved source: the project glossary, the codebase's existing vocabulary, the platform's established terms, or the domain's terminology. Search for the existing name before inventing one. |
| N2 | One name, one meaning. Never reuse a name for a second concept. |
| N3 | One concept, one name, everywhere. Synonym drift (`user`/`customer`/`account` for one entity) is a defect. |
| N4 | Name by role: functions are verb phrases, types and values are noun phrases, booleans are predicates (`is`/`has`/`can`). Never a noun-named function or a verb-named type. |
| N5 | One approved form per word: imperative verb stems for actions (`createUser`, not `creatingUser`/`userCreation`); past participles only as state descriptors (`parsedConfig`, `isLocked`); gerunds only when the platform itself uses them. |
| N6 | Compound names have at most 3 words. A concept that needs more gets a shorter term defined in the glossary. |
| N7 | Names are short, plain, and pronounceable. No slang, humor, regionalisms, or unexplained abbreviations. |
| N8 | Prefer the platform/framework/industry's established term over a house synonym. |
| N9 | One spelling locale — American English unless the project directs otherwise — in every identifier and doc. |

Ticket and chat vocabulary does not override the codebase: when a ticket says
"members" and the code says `Subscriber`, the code's term wins (N3). Propose a
rename separately if the codebase term is wrong — never mix both.

## Starter vocabulary

Universal approved verbs — one meaning each. A project's glossary can extend or
override this table, never silently fork it.

| Verb | Approved meaning | Not for |
|---|---|---|
| get | return a value already available; cheap, failure unexpected | remote calls (fetch), searches (find) |
| fetch | retrieve across a boundary (network, disk); can fail or be slow | local reads (get) |
| find | search that can legitimately return nothing | lookups guaranteed to exist (get) |
| list | return all items of a kind | single item (get/find) |
| create | bring a new persisted entity into existence | in-memory assembly (build) |
| build | assemble an in-memory value from parts; nothing persisted | persistence (create, save) |
| update | modify an existing persisted entity | in-memory assignment (set) |
| delete | destroy permanently | detaching from a collection (remove) |
| remove | detach from a collection or relationship; the item may live on | permanent destruction (delete) |
| set | assign a value | |
| is / has / can | boolean predicates | non-boolean returns |
| validate | check and report all violations | boolean checks (is*), assertions (assert) |
| parse | turn text/bytes into a structured value; fails loudly on bad input | |
| init | prepare something for first use, once | repeated setup (configure) |
| send | transmit to an external receiver | |
| start / stop / run | lifecycle of a process or job | spinUp / kickOff / teardown (C3) |

Banned vague words — each with the approved move (the STE dictionary format:
unapproved word → approved alternative):

| Banned | Why | Instead |
|---|---|---|
| data, info | name no content | name the content: `invoiceRows`, `retryPolicy` |
| item, thing, entry, element, obj | generic container words | the actual noun |
| manager, processor, handler, helper, util(s), misc, common | doer-nouns and junk drawers that hide the responsibility (S7) | a verb for the action, a noun for the real topic; `handler` only as the platform's own callback term (N8) |
| do, perform, execute, process, handle | verbs that name no action | the specific verb |
| temp, tmp, foo, `x2`, `newX`, `oldX` | placeholder names | the role: `previousBalance`, `migratedSchema` |
| flag, status (bare) | which condition? | the predicate or state: `isRetryable`, `deliveryState` |
| check | ambiguous: validate? boolean? assert? | validate / is* / assert |

## The project glossary

Each project keeps a `GLOSSARY.md` — its own dictionary Part 2. Template:

```markdown
# Project Glossary

One term per concept. One meaning per term. New domain terms are added here
before first use.

| Term (kind) | Approved meaning | Example in code | Do not use → use this term |
|---|---|---|---|
| subscriber (noun) | person or system receiving notifications | `countSubscribers()` | user, member, recipient → subscriber |
```

Maintenance rules:

- A new domain term is added **before** its first use in code (C4).
- A rename is a migration: every reference changes in one commit.
- The "do not use" column grows every time review catches drift (N3).
- One meaning per term — a second meaning gets a second term (N2).

No glossary in the project yet? Offer to seed `GLOSSARY.md` from the template
with the 5–10 domain terms the current codebase already uses most.
