# Coding Review Criteria

> Focused review criteria for coding Tasks — concentrate on essential questions.

---

## 1. Goal Achievement

- [ ] Does the work sufficiently achieve the defined goal?
- [ ] Are all acceptance criteria satisfied?
- [ ] Is there any out-of-scope or missing work?

---

## 2. Issues

- [ ] Are there functional bugs?
- [ ] Is error handling adequate? (including edge cases)
- [ ] Are there security vulnerabilities? (input validation, authentication/authorization, sensitive data exposure)
- [ ] Are there anticipated performance issues? (N+1 queries, unnecessary computation, memory leaks)
- [ ] Does the change cause regressions in existing functionality?

---

## 3. Code Readability & Maintainability

- [ ] Do names clearly convey intent? (Mysterious Name)
- [ ] Do functions/methods have a single responsibility and appropriate size? (Long Function)
- [ ] Are there unnecessary nesting or conditional chains in complex logic?
- [ ] Can another developer easily understand and modify this code?
- [ ] Is there duplicated code? (Duplicated Code)

---

## 3-1. Code Smells (Fowler's Refactoring)

> Flag any of the following as 🟡 Improvement or higher.

**Bloaters:**
- [ ] Large Class — Does the class carry too many fields, methods, or responsibilities?
- [ ] Long Parameter List — Are there more than 3 parameters where fewer would suffice?
- [ ] Primitive Obsession — Are domain concepts represented as primitive types (string, number)?
- [ ] Data Clumps — Is the same group of data passed together in multiple places?

**Object-Orientation Abusers:**
- [ ] Repeated Switches — Does the same switch/if-else chain appear in multiple locations?
- [ ] Temporary Field — Are there fields only populated under certain conditions?
- [ ] Refused Bequest — Does a subclass inherit methods/properties it does not use?
- [ ] Alternative Classes with Different Interfaces — Do classes serving the same role have different interfaces?

**Change Preventers:**
- [ ] Divergent Change — Is a single module frequently changed for unrelated reasons?
- [ ] Shotgun Surgery — Does a single change require scattered modifications across many modules?
- [ ] Parallel Inheritance Hierarchies — Does adding a class to one hierarchy require adding one to another?

**Dispensables:**
- [ ] Lazy Element — Are there classes/functions that don't justify their existence?
- [ ] Data Class — Are there classes with only getters/setters and no behavior?
- [ ] Speculative Generality — Are there abstractions built for hypothetical future needs?

**Couplers:**
- [ ] Feature Envy — Does a method use another object's data more than its own?
- [ ] Inappropriate Intimacy — Do two classes excessively reference each other's internals?
- [ ] Message Chains — Do long method chains (a.b().c().d()) expose internal structure?
- [ ] Middle Man — Does a class delegate most of its methods to another object?

**Other:**
- [ ] Global Data — Is there mutable data accessible from anywhere via globals or singletons?
- [ ] Mutable Data — Is there data that could be made immutable but isn't?
- [ ] Insider Trading — Do modules exchange internal information without formal interfaces?
- [ ] Loops — Are there imperative loops replaceable with pipelines (map/filter/reduce)?

---

## 4. Test Readability & Maintainability

- [ ] Are core behaviors and edge cases covered by tests?
- [ ] Do test names clearly describe what is being verified?
- [ ] Do tests verify behavior/outcomes rather than implementation details? (blackbox)
- [ ] Are mocks used minimally and only at boundaries (I/O)?
- [ ] Are tests independent and deterministic?

---

## 5. Guidelines Compliance

- [ ] Does the code follow project coding conventions?
- [ ] Does it comply with CLAUDE.md or project guideline rules?
- [ ] Is it consistent with decisions recorded in `refs/decisions/`?
- [ ] Is it consistent with existing codebase patterns?

---

## 6. Stale/Dead Cleanup

- [ ] Is there unused code (dead code) remaining?
- [ ] Is there commented-out code? (should be deleted)
- [ ] Are there obsolete TODO/FIXME comments?
- [ ] Are there unnecessary imports, variables, or files?
