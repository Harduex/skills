# Functional Programming Reference

## 1. Data — Prefer Immutable, Transparent Values

Data is the most tractable element. It is simple, predictable, and cannot inadvertently break your system.

### Principles

- **Variables do not vary.** Once a value is set, it cannot be modified. Always create new objects/arrays via spread or map — never mutate in place.
- **Concurrency without fear.** Immutable data eliminates race conditions, deadlocks, and concurrent update problems at the root.
- **Fold knowledge into data.** When choosing between complex procedural code and complex data structures, choose the data. Shift complexity from code into data — it's easier for humans to reason about.

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

---

## 2. Calculations — Pure Functions

When you must write logic, prefer pure functions that transform input data into output data without affecting anything else.

### Principles

- **Guaranteed consistency.** Same inputs always produce the same output, no matter how many times called.
- **No observable side effects.** Must not change program state, mutate data, or interact with external systems. Only returns a derived value or new object.
- **Referential transparency.** No hidden inputs (globals, `Date.now()`, `Math.random()`) or hidden outputs (exceptions thrown for control flow, database writes). A call can be replaced by its return value without changing behavior.
- **Segregate queries from commands.** Strictly separate functions that calculate/return data (queries) from functions that change state (commands). Asking a question should never change the answer.

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

---

## 3. Actions — Isolate and Minimize Side Effects

Actions are commands that interact with the outside world. They are necessary but should be as thin and dumb as possible.

### Principles

- **Push actions to the edges.** Maximize pure calculations, minimize side-effect code.
- **Functional core / mutable shell.** The core makes all decisions with pure logic. The shell reads external state, feeds it to the core, and applies the core's output as side effects.
- **Make actions dumb.** Functions executing side effects should contain zero business logic. All complex logic belongs in pure calculations.

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

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Fix |
|---|---|---|
| Mutating function arguments | Caller can't trust data after passing it | Return new objects |
| `Date.now()` / `Math.random()` inside calculations | Hidden input breaks referential transparency | Pass as parameter |
| Business logic in API handlers | Can't test without mocking IO | Extract to pure functions |
| Query that also mutates state | Violates command-query separation | Split into two functions |
| `useEffect` to derive state | Action where calculation suffices | Use `useMemo` or compute in render |
| Throwing exceptions for control flow | Hidden output breaks purity | Return error values (Result types, error arrays) |
