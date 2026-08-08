# Functional Programming Reference

Functional programming rules with stable IDs in seven bands, adapted to
TypeScript/React — cite them in reviews (e.g. "violates D3"). The bands hold
the rules; the three numbered "In Practice" sections illustrate bands C, A,
and I with examples and carry no separate rules. When reviewing, cite IDs for
FP findings; report adjacent non-FP defects separately, uncited. Severity and
finding format come from your set's review workflow.

## Band C — Classify code

- **C1 — Classify every piece of code as an action, a calculation, or data.**
  The classification decides how you test, reuse, and place the code.
- **C2 — Treat code that depends on when or how many times it runs as an
  action.** Sending a request, reading a database, `Date.now()`, reading a
  mutable global — all actions.
- **C3 — Write calculations: same inputs, same outputs, no writes outside
  them.** No dependence on when or how often they run — and no mutation of
  inputs: a deterministic function that mutates its argument is a write, not
  a calculation (I2).
- **C4 — Treat data as facts about events.** Data does not run; it must be
  interpreted, and the same data can serve many future interpretations.
- **C5 — Prefer data over calculations, and calculations over actions.** Data
  is easiest to work with; calculations are easiest to test.
- **C6 — Know that actions spread.** One action called inside a function makes
  the whole function an action. Contain the blast radius by extracting the
  calculations out.
- **C7 — Think of calculations as planning and actions as execution.** The
  calculation produces a decision (data); the action carries it out.
- **C8 — Keep entities in general-purpose data structures.** Plain objects and
  arrays keep data open to interpretations you can't predict; a narrow class
  API forecloses them. Add an abstraction barrier (D4) as an optional
  interface instead.
- **C9 — Fold knowledge into data.** When choosing between complex code and
  complex data, choose the data — a lookup table over an if-chain, a config
  object over a hardcoded rule.

## 1. Data — Prefer Immutable, Transparent Values (C4, C8, C9, I1)

Data is the most tractable element. It is simple, predictable, and cannot
inadvertently break your system.

### Principles

- **Variables do not vary.** Once a value is set, it cannot be modified. Always create new objects/arrays via spread or map — never mutate in place. (I1)
- **Concurrency without fear.** Immutable data eliminates race conditions, deadlocks, and concurrent update problems at the root.
- **Fold knowledge into data.** When choosing between complex procedural code and complex data structures, choose the data. Shift complexity from code into data — it's easier for humans to reason about. (C9)

### In Practice (TypeScript/React)

```ts
// BAD: mutation
user.role = 'admin';
items.push(newItem);

// GOOD: derive new values
const updatedUser = { ...user, role: 'admin' };
const updatedItems = [...items, newItem];
```

```ts
// GOOD: fold knowledge into data
const PERMISSIONS = {
  admin: ['read', 'write', 'delete'],
  editor: ['read', 'write'],
  viewer: ['read'],
} as const;

// Instead of:
function getPermissions(role: string) {
  if (role === 'admin') return ['read', 'write', 'delete'];
  if (role === 'editor') return ['read', 'write'];
  // ...
}
```

## 2. Calculations — Pure Functions (C3, C7)

When you must write logic, prefer pure functions that transform input data
into output data without affecting anything else.

### Principles

- **Guaranteed consistency.** Same inputs always produce the same output, no matter how many times called. (C3)
- **No observable side effects.** Must not change program state, mutate data, or interact with external systems. Only returns a derived value or new object.
- **Referential transparency.** No hidden inputs (globals, `Date.now()`, `Math.random()`) or hidden outputs (exceptions thrown for control flow, database writes). A call can be replaced by its return value without changing behavior.
- **Segregate queries from commands.** Strictly separate functions that calculate/return data (queries) from functions that change state (commands). Asking a question should never change the answer. (A5)

### In Practice

```ts
// GOOD: pure calculation — no side effects, no hidden inputs
function calculateTotal(items: ReadonlyArray<CartItem>): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// GOOD: query separated from command
function buildUpdatePayload(user: User, changes: Partial<User>): UpdatePayload {
  return { id: user.id, ...changes, updatedAt: new Date().toISOString() };
}
// The action (API call) happens elsewhere
```

```ts
// BAD: query mixed with command
function getAndIncrementCount(): number {
  count += 1;  // side effect hidden in a "getter"
  return count;
}

// BAD: hidden input
function formatGreeting(name: string): string {
  const hour = new Date().getHours(); // hidden input — not referentially transparent
  return hour < 12 ? `Good morning, ${name}` : `Hello, ${name}`;
}

// GOOD: make the dependency explicit
function formatGreeting(name: string, hour: number): string {
  return hour < 12 ? `Good morning, ${name}` : `Hello, ${name}`;
}
```

## 3. Actions — Isolate and Minimize Side Effects (Band A)

Actions are commands that interact with the outside world. They are necessary
but should be as thin and dumb as possible.

### Principles

- **A1 — Extract calculations from actions.** Pull the computation into its own function; convert implicit inputs to arguments and implicit outputs to return values.
- **A2 — Minimize implicit inputs and outputs, in actions too.** Implicit inputs are all inputs that are not arguments; implicit outputs are all outputs that are not the return value. Every one you remove makes the function more modular, testable, and reusable.
- **A3 — Pull things apart.** Small functions with one job compose back together; big ones don't come apart. Design is about pulling things apart.
- **A4 — Push actions to the edges.** Maximize pure calculations, minimize side-effect code. Expect the ratio to shift toward calculations as you apply A1–A3.
- **A5 — Segregate queries from commands.** A function either returns data or changes state, never both — asking a question must not change the answer.
- **A6 — Make actions dumb.** Functions executing side effects contain zero business logic. All complex logic belongs in pure calculations.
- **Functional core / mutable shell (R3).** The core makes all decisions with pure logic. The shell reads external state, feeds it to the core, and applies the core's output as side effects.

### In Practice

```ts
// BAD: business logic mixed into the action
async function handleSubmit(form: FormData) {
  const errors = [];
  if (!form.email.includes('@')) errors.push('Invalid email');
  if (form.password.length < 8) errors.push('Password too short');
  if (errors.length > 0) {
    showErrors(errors);  // side effect
    return;
  }
  const payload = { ...form, createdAt: Date.now() };
  await api.createUser(payload);  // side effect
  router.push('/welcome');  // side effect
}

// GOOD: functional core / mutable shell
// --- Core (pure calculations) ---
function validateForm(form: FormData): string[] {
  const errors: string[] = [];
  if (!form.email.includes('@')) errors.push('Invalid email');
  if (form.password.length < 8) errors.push('Password too short');
  return errors;
}

function buildCreateUserPayload(form: FormData, now: number): CreateUserPayload {
  return { ...form, createdAt: now };
}

// --- Shell (thin actions) ---
async function handleSubmit(form: FormData) {
  const errors = validateForm(form);
  if (errors.length > 0) {
    showErrors(errors);
    return;
  }
  await api.createUser(buildCreateUserPayload(form, Date.now()));
  router.push('/welcome');
}
```

### React Hooks: Functional Core / Mutable Shell

```ts
// Core: pure calculation hook (no effects, no mutations)
function useFilteredItems(items: Item[], searchTerm: string): Item[] {
  return useMemo(
    () => items.filter(item =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    ),
    [items, searchTerm]
  );
}

// Shell: thin action hook (effects and mutations only)
function useItemSearch(projectId: string) {
  const [searchTerm, setSearchTerm] = useState('');
  const { data } = useQuery(GET_ITEMS, { variables: { projectId } });
  const filtered = useFilteredItems(data?.items ?? [], searchTerm);
  return { filtered, searchTerm, setSearchTerm };
}
```

## Band I — Immutability disciplines

- **I1 — Default to immutable data.** Optimize with mutation only after
  something is proven too slow.
- **I2 — Copy-on-write for data you control: make a copy, modify the copy,
  return the copy.** Spread syntax is copy-on-write. It converts a write into
  a read — the function becomes a calculation. When converting an in-place
  mutator, keep a thin wrapper under the old name at existing call sites and
  migrate them in stages.
- **I3 — Treat reads of immutable data as calculations.** The more data is
  immutable, the more of your code becomes calculations.
- **I4 — Defensive copying at trust boundaries: deep-copy as data enters,
  deep-copy as data leaves.** Untrusted code — legacy modules, third-party
  libraries, anything that mutates — must never hold a reference into your
  immutable data.
- **I5 — Copy-on-write inside your codebase; defensive copying only at the
  boundary.** Copy-on-write is cheap: shallow copies share unchanged
  structure. Defensive deep copies are expensive; reserve them for the edge.

```ts
// I2: copy-on-write — shallow copy shares the unchanged items (cheap)
function setQuantity(cart: Cart, name: string, quantity: number): Cart {
  return cart.map(item => (item.name === name ? { ...item, quantity } : item));
}

// I4: defensive copy where an untrusted mutating library touches our data
function applyLegacyDiscount(cart: Cart): Cart {
  const input = structuredClone(cart);   // copy as data leaves the safe zone
  legacyDiscounter.process(input);       // mutates freely — only the copy
  return structuredClone(input);         // copy as data comes back in
}
// Serialization boundaries (HTTP, postMessage, workers) are implicit
// defensive copies — JSON in, JSON out.
```

## Band D — Stratified design

Organize functions into layers of abstraction; diagnose the design by its
call graph.

- **D1 — Each function calls only functions from the layer below it.**
  Typical strata: business rules → domain operations → utilities → language
  built-ins. A function whose calls reach into several different layers is in
  the wrong place or doing too much.
- **D2 — Write straightforward implementations.** The body solves the problem
  the signature states, at one level of detail. Too much detail is a code
  smell: a business rule that runs a `for` loop over array indexes mixes
  layers.
- **D3 — Do not hide complexity in helper functions.** Every layer must be
  straightforward, not only the top one. Moving a mess into `doStuffHelper()`
  is relocation, not design.
- **D4 — Build abstraction barriers to hide implementation details.** A
  barrier is a layer of functions below which the representation (array?
  Map? sorted?) is invisible. Both sides win: callers ignore the structure,
  implementers can swap it without telling anyone.
- **D5 — Keep interfaces minimal.** Let the operations on an important
  concept converge to a small, reliable set. Implement new features *above*
  the barrier by composing existing operations — don't widen the barrier for
  every feature.
- **D6 — Stop designing when the layers are comfortable.** Layers are for
  working in, not for sport. If the code is comfortable, relax; when
  discomfort returns, resume.
- **D7 — Business rules must not know low-level structure.** Rules change
  faster than representations. A pricing rule that knows the cart is an array
  will break when the cart becomes a Map.

```ts
// cart.ts — the abstraction barrier: nothing above this file
// knows (or may know) that a cart is an array
export type Cart = ReadonlyArray<CartItem>;
export const addItem = (cart: Cart, item: CartItem): Cart => [...cart, item];
export const removeItem = (cart: Cart, name: string): Cart =>
  cart.filter(i => i.name !== name);
export const isInCart = (cart: Cart, name: string): boolean =>
  cart.some(i => i.name === name);
export const calcTotal = (cart: Cart): number =>
  cart.reduce((sum, i) => sum + i.price, 0);

// promotions.ts — above the barrier: written purely in cart operations,
// survives any change of representation (D5, D7)
function addFreeGiftIfEligible(cart: Cart): Cart {
  return calcTotal(cart) >= 20 && !isInCart(cart, 'gift')
    ? addItem(cart, FREE_GIFT)
    : cart;
}
```

## Band F — Refactorings & functional tools

Two named refactorings remove most duplication; functional tools replace
hand-written loops.

- **F1 — Smell: implicit argument in the function name.** Near-identical
  bodies whose names encode the differing value (`setPriceByName`,
  `setQuantityByName`, …). Fix: *express the implicit argument* — make the
  value a real parameter.
- **F2 — Refactor duplicated structure with *replace body with callback*.**
  Extract the varying middle as a callback to a higher-order function. Works
  on duplicated syntax (loops, try/catch) and even on a duplicated
  discipline like copy-on-write.
- **F3 — Replace hand-written loops with `map()`, `filter()`, `reduce()`.**
  They name the intent; a `for` loop makes the reader re-derive it.
- **F4 — Pass only calculations to functional tools.** An action inside a
  `map()` callback turns the whole pipeline into an action (C6).
- **F5 — Chain in small steps: make data, operate on the whole array, take
  many small steps.** Values a loop kept in local variables become explicit
  intermediate arrays.
- **F6 — Use an update-at-path helper for nested data.** Manual spread
  plumbing mirrors the nesting and breaks when the shape changes.
- **F7 — Put abstraction barriers over deeply nested data.** Callers say
  *what* to change (`incrementSize(cart, 'shirt')`), not *where it lives*.
- **F8 — Prefer the straightforward solution unless the higher-order one is
  clearly better.** Before keeping a clever abstraction, compare: is it
  really clearer? How much duplication does it actually remove? At two
  duplicates, stay straightforward unless a third is in sight; adopt the
  abstraction when it deletes more code than it adds or standardizes a
  discipline callers can get wrong (like copy-on-write).
- **F9 — Recursion for nested data, loops for flat iteration.**

```ts
// F1 + F2: express implicit argument, then replace body with callback
function setField<K extends keyof CartItem>(
  cart: Cart, name: string, field: K, value: CartItem[K],
): Cart {
  return cart.map(i => (i.name === name ? { ...i, [field]: value } : i));
}
// replaces setPriceByName, setQuantityByName, setShippingByName, ...

// F2 on a discipline: copy-on-write, standardized once
function withArrayCopy<T>(array: readonly T[], modify: (copy: T[]) => void): T[] {
  const copy = [...array];
  modify(copy);
  return copy;
}
const sorted = withArrayCopy(numbers, c => c.sort());  // in-place API, immutably

// F5: moving average — each step is data in, data out
const averages = range(0, xs.length)                 // 1. make data
  .map(i => xs.slice(i, i + windowSize))             // 2. whole array at once
  .map(average);                                     // 3. many small steps
```

## Band T — Timelines

An async boundary (`await`, callback, event) splits execution into timelines
whose steps can interleave. Possible orderings, not lines of code, are what
make async systems hard.

- **T1 — Fewer timelines are easier.** Every parallel fetch, subscription, or
  handler multiplies the orderings to account for.
- **T2 — Shorter timelines are easier.** Fewer steps per timeline means fewer
  interleavings. Collapse consecutive awaits that don't need to be separate.
- **T3 — Sharing fewer resources is easier.** Only steps that touch a shared
  resource (module state, the DOM, a cache) across timelines need order
  analysis. Pass values through instead of writing to shared state.
- **T4 — Coordinate the shared resources that remain.** Make timelines take
  turns; eliminate the orderings that produce a wrong result. Shell-owned
  mutable state is acceptable when it has a single writer and access is
  serialized — the queue below is how you serialize it.
- **T5 — Manipulate time as a first-class concept.** Build (or reuse) small
  primitives that reshape ordering and repetition: a queue linearizes,
  `Promise.all` joins, a `once()` wrapper deduplicates, an `AbortController`
  supersedes stale work.
- **T6 — An async function's explicit output is its returned promise.** Never
  smuggle results out through shared state; return the value.
- **T7 — Model sharing on real-world protocols.** Queue at the checkout, lock
  on the door, one writer / many readers on the blackboard.
- **T8 — Sketch the timeline diagram when ordering is in doubt.** Timing bugs
  hide from tests and reviews; two lanes and their shared-resource arrows
  make them visible before production does.
- **T9 — Edge-trigger effects on state transitions.** An effect conditioned
  on a threshold must fire when the state *crosses* it — computed purely from
  the (before, after) pair — not re-fire on every step while the condition
  holds.

```ts
// BAD (T3/T4): two clicks → two timelines racing on shared state;
// the slower response wins, whichever it is
let total = 0;
async function addToCartHandler(item: Item) {
  const cost = await fetchCost(item);   // timeline splits here
  total += cost;                        // shared write, order-dependent
  renderTotal(total);
}

// GOOD (T5): a queue linearizes the action — clicks can't interleave
function makeQueue<J>(worker: (job: J) => Promise<void>) {
  const jobs: J[] = [];
  let running = false;
  return async (job: J) => {
    jobs.push(job);
    if (running) return;
    running = true;
    while (jobs.length > 0) {
      try {
        await worker(jobs.shift()!);
      } catch (err) {
        reportError(err); // a failed job must not strand the queued ones
      }
    }
    running = false;
  };
}
const enqueueAddToCart = makeQueue(addToCartHandler);
```

## Band R — Architecture

- **R1 — Use reactive architecture to decouple cause from effect.** Derive
  effects from state changes (store subscription, React re-render) instead of
  repeating the effect in every event handler that might trigger it.
- **R2 — Don't force reactive style onto strictly sequential flows.** It pays
  off where many causes converge on one effect or one cause fans out; a plain
  sequence of steps should stay a sequence. Reviewing a single handler in
  isolation, default to the sequence; recommend R1 only when a second cause
  or effect already exists.
- **R3 — Structure services as an onion.** Interaction layer (actions: HTTP,
  DB, UI) around a domain layer (calculations: the business rules) around a
  language layer (utilities). The functional core / mutable shell diagram in
  SKILL.md is this pattern.
- **R4 — Layers call inward and know nothing about outer layers.** The domain
  never imports the handler; the handler composes the domain.
- **R5 — Keep domain rules out of the database.** The interaction layer
  fetches, the domain computes, the interaction layer writes back. Same work,
  different call graph — and the domain stays testable without mocks.
- **R6 — Accept the paradigm's cost limits.** When a rule modeled as a
  calculation turns awkward, weigh readability against purity and choose
  deliberately.

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Fix |
|---|---|---|
| Mutating function arguments | Caller can't trust data after passing it | Return new objects (I2) |
| `Date.now()` / `Math.random()` inside calculations | Hidden input breaks referential transparency | Pass as parameter (A2) |
| Business logic in API handlers | Can't test without mocking IO | Extract to pure functions (A1) |
| Query that also mutates state | Violates command-query separation | Split into two functions |
| `useEffect` to derive state | Action where calculation suffices | Use `useMemo` or compute in render |
| Throwing exceptions for control flow | Hidden output breaks purity | Return error values (Result types, error arrays) |
| Near-identical functions, names encoding a value | Implicit argument in the name | Express the argument (F1) |
| Complexity moved into a "helper" | Layer below stays unclear | Make every layer straightforward (D3) |
| Business rule reads the data structure directly | Fast-changing rule coupled to representation | Abstraction barrier (D4, D7) |
| Shared variable written after an `await` | Timelines interleave on it | Pass values through; queue the action (T3–T5) |
| Same effect repeated in every event handler | Cause coupled to effect | Subscribe to the state change once (R1) |
| Threshold effect re-fires while the condition holds | Level-triggered instead of edge-triggered | Compute the crossing from (before, after) (T9) |
