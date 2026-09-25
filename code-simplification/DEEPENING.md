# Deepening Modules

A **deep module** has a small interface that hides a large implementation. Deep modules are easier to test at the boundary, easier to navigate, and cheaper to change. A **shallow module** has an interface about as costly to learn as the code it hides. It spreads knowledge out instead of hiding it.

Use this file for L3 candidates that restructure modules, not only inline a wrapper.

## Contents

- [Spotting candidates](#spotting-candidates)
- [Proving the candidate](#proving-the-candidate)
- [Dependency categories](#dependency-categories)
- [Design it twice](#design-it-twice)
- [Testing: replace, don't layer](#testing-replace-dont-layer)

## Spotting candidates

Friction you feel while navigating is the signal:

- Understanding one concept means bouncing between many small files.
- A module's interface is nearly as complex as its implementation.
- Pure functions were extracted only for testability, but the real bugs hide in how they are called.
- Tightly coupled modules create integration risk in the seams between them.
- One design decision leaks into several modules. A change to it edits all of them.
- Adding one instance of a concept touches many files. Count them.
- A part of the code is untested because it is hard to test through its current shape.

## Proving the candidate

- **Deletion test.** Merging the modules must concentrate complexity behind one interface. If it only moves the complexity, drop the candidate.
- **Real seams only.** One adapter is a hypothetical seam. Two adapters make a real one. Do not keep an interface for a second implementation nobody has written.
- **Past, not future.** A claim that "the next instance will be painful" needs past instances in `git log`.
- **Recorded decisions.** If an ADR chose the current split, surface the conflict only when the friction is real, and cite the ADR.

## Dependency categories

Classify what the deepened module depends on. The category decides how it is merged and tested.

1. **In-process.** Pure computation or in-memory state, no I/O. Always deepenable: merge the modules and test directly.
2. **Local-substitutable.** Has a local test stand-in (an in-memory database, an in-memory filesystem). Deepenable when the stand-in exists. Test the deepened module with the stand-in in the suite.
3. **Remote but owned.** Your own service across a network boundary. Define a port at the module boundary. The deep module owns the logic, and the transport is injected. Tests use an in-memory adapter. Production uses the real HTTP, gRPC, or queue adapter.
4. **True external.** A third-party service you do not control. Take it as an injected port and mock it at the boundary in tests.

## Design it twice

The first interface you think of is rarely the best one. Before applying a picked deepening candidate, sketch two interfaces yourself. No extra agents are needed.

- **Minimal**: one to three entry points.
- **Common caller first**: the everyday call is trivial, and rare cases take an extra argument or a second function.
- Add **ports and adapters** as a third sketch only when the module crosses a category 3 or 4 boundary.

For each sketch, show the signature, one usage example, what it hides, and its trade-offs. Recommend one, or a hybrid, and wait for the user's choice before editing. Never add flexibility nobody asked for.

## Testing: replace, don't layer

- Write new tests at the deepened module's interface.
- Tests assert observable outcomes through the public interface, not internal state. They survive internal refactors.
- Once boundary tests cover the behavior, delete the old tests on the shallow modules. Keeping both doubles the maintenance cost.
- Deleting old tests is a picked, visible step with its own commit. It never happens silently inside a refactoring commit.
