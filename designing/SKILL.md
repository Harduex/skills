---
name: designing
description: Designs user interfaces and experiences. Maps user journeys, creates wireframes, defines interaction states, and ensures accessibility. Use when designing new interfaces, improving user flows, evaluating usability, or planning interaction patterns.
---

# Product Design

## Process

1. **Understand the user** — identify the persona, their goal, and context (device, environment, skill level).
2. **Map the journey** — chart the path from intent to completion. Identify every step, decision point, and dead end.
3. **Design the flow** — create the simplest path from intent to outcome. Remove every non-essential step.
4. **Define all states** — empty, loading, partial, error, success, edge cases. Every screen has more than one state.
5. **Validate** — test against accessibility standards and usability heuristics.

## Output formats

Adapt to the need:

- **User flow diagrams** — ASCII or structured text showing screens and decisions
- **Wireframes** — low-fidelity layout descriptions with element placement and hierarchy
- **Component specs** — interactive elements with all states, transitions, and edge cases
- **Design critique** — evaluation of existing designs with specific improvement recommendations

## Example: Component spec

```
### Search input

**Default**: Placeholder text "Search...", magnifying glass icon
**Focused**: Border highlight, placeholder fades, clear button appears
**Typing**: Live results dropdown after 300ms debounce, max 5 suggestions
**Loading**: Spinner replaces magnifying glass icon
**No results**: "No results for [query]" with suggested alternatives
**Error**: "Search unavailable" with retry link
**Keyboard**: Arrow keys navigate suggestions, Enter selects, Escape closes
```

## Principles

- The user's mental model takes priority over implementation convenience.
- Design interactions that prevent mistakes rather than showing error messages after.
- Defend design choices with established principles, not personal preference.
- Accessibility (keyboard navigation, screen readers, contrast) is non-negotiable.
