# Coding Review Checklist

> Comprehensive review checklist for software development Tasks/Features.

---

## 1. Goal Achievement ⭐

> The most important question: "Did this Task accomplish what it set out to do?"
> Failure to meet goals or acceptance criteria is always 🔴 Critical.

- [ ] Does the work accurately achieve the defined goals?
- [ ] Are all acceptance criteria satisfied?
- [ ] Is there any scope creep?
- [ ] Are there missing requirements?

---

## 2. Design Quality ⭐

> Design quality is the foundation of code. Review after confirming goal achievement.

**Design Principles:**
- [ ] **SOLID** compliance
  - Single Responsibility: Does each unit have exactly one responsibility?
  - Open/Closed: Is it open for extension, closed for modification?
  - Liskov Substitution: Is substitutability guaranteed?
  - Interface Segregation: Are interfaces properly separated?
  - Dependency Inversion: Does it depend on abstractions?
- [ ] **YAGNI** — Is only what's actually needed implemented?
- [ ] **DRY** — Is there unnecessary repetition?
- [ ] **KISS** — Are there unnecessarily complex parts?

**Architecture Quality:**
- [ ] Is the separation of responsibilities between layers/modules clear?
- [ ] Is the direction of dependencies correct? (pointing inward?)
- [ ] Are there circular dependencies?
- [ ] Is coupling appropriate?
- [ ] Is cohesion high?

**Extensibility & Maintainability:**
- [ ] Is the scope of modification limited when adding new features?
- [ ] Are there parts that are fragile to change?
- [ ] Is the structure easy to test?
- [ ] Is it easy for other developers to understand?

**Consistency:**
- [ ] Does it conflict with decisions recorded in `refs/decisions/`?
- [ ] Is it consistent with the overall project architecture?
- [ ] Does it follow existing patterns, or does it introduce new ones?

---

## 3. Code Quality ⭐

> Code is the embodiment of design. Review whether design intent is properly reflected in code.

**Functional Correctness:**
- [ ] Does the code accurately implement the requirements?
- [ ] Are all edge cases handled?
- [ ] Is error handling adequate and consistent?
- [ ] Does the system behave safely under exceptional conditions?

**Code Structure:**
- [ ] Do functions/methods have a single responsibility?
- [ ] Are functions/methods an appropriate length? (not too long?)
- [ ] Is nesting depth reasonable?
- [ ] Are conditionals free of unnecessary complexity?
- [ ] Is there duplicated code?

**Readability:**
- [ ] Are names clear and intention-revealing?
- [ ] Are comments present where needed? (parts not self-evident from code)
- [ ] Are there unnecessary comments? (parts already clear from code)
- [ ] Are there magic numbers or magic strings?
- [ ] Is code formatting consistent?

**Convention Compliance:**
- [ ] Does it match the project's coding style?
- [ ] Are there linter/formatter warnings?

**Security:**
- [ ] Is input validation sufficient?
- [ ] Are there SQL Injection, XSS, or similar vulnerabilities?
- [ ] Is sensitive information hardcoded?
- [ ] Is authentication/authorization logic correct?
- [ ] Does logging include sensitive information?

**Performance:**
- [ ] Are there unnecessary computations or calls?
- [ ] Are there N+1 query problems?
- [ ] Is there potential for memory leaks?
- [ ] Are there anticipated bottlenecks?
- [ ] Are there parts that need caching?

**Error Handling:**
- [ ] Are all error paths handled?
- [ ] Are error messages useful to users/developers?
- [ ] Is error logging adequate?
- [ ] Is there an error recovery strategy?

---

## 3-1. Code Smells (Fowler's Refactoring) ⭐

> Code smells are surface symptoms of deeper problems. Consider refactoring when any of the following are detected.

**Bloaters:**
- [ ] Long Function — Is the function excessively long or handling multiple stages at once?
- [ ] Large Class — Does the class carry too many fields, methods, or responsibilities?
- [ ] Long Parameter List — Are there too many parameters? (can they be grouped into an object?)
- [ ] Primitive Obsession — Are domain concepts represented as primitives (string, number, boolean)?
  - e.g., `status: string` → `Status` enum/union; `money: number` → `Money` value object
- [ ] Data Clumps — Is the same group of data passed together in multiple places?
  - e.g., if `(startDate, endDate)` recurs, extract a `DateRange`

**Object-Orientation Abusers:**
- [ ] Repeated Switches — Does the same switch/if-else chain appear in multiple locations?
  - Can it be replaced with polymorphism?
- [ ] Temporary Field — Are there fields only populated under certain conditions?
  - Should they be extracted into a separate class or expressed as Optional?
- [ ] Refused Bequest — Does a subclass inherit methods/properties it does not use?
  - Should inheritance be replaced with composition?
- [ ] Alternative Classes with Different Interfaces — Do classes serving the same role have different interfaces?
  - Can they be unified under a common interface?

**Change Preventers:**
- [ ] Divergent Change — Is a single module frequently changed for unrelated reasons?
  - Symptom of SRP violation. Does it need to be split by responsibility?
- [ ] Shotgun Surgery — Does a single change require scattered modifications across many modules?
  - Should related logic be consolidated in one place?
- [ ] Parallel Inheritance Hierarchies — Does adding a class to one hierarchy require adding one to another?

**Dispensables:**
- [ ] Lazy Element — Are there classes, functions, or interfaces that don't justify their existence?
  - Elements that only delegate or contain too little substance
- [ ] Data Class — Are there classes with only getters/setters and no behavior?
  - Should the logic that uses this data be moved into the class?
- [ ] Speculative Generality — Are there abstractions, parameters, or interfaces built for hypothetical future needs?
  - Abstractions created "just in case" without current justification
- [ ] Dead Code — Is there unused code? (functions, variables, imports, conditional branches)
- [ ] Comments (as smell) — Are there comments compensating for poor code structure?
  - Is the need for a comment caused by the code itself being unclear?

**Couplers:**
- [ ] Feature Envy — Does a method use another object's data more than its own?
  - Should the method be moved to the class that owns the data?
- [ ] Inappropriate Intimacy — Do two classes/modules excessively reference each other's internals?
- [ ] Message Chains — Do long method chains (a.b().c().d()) expose internal structure?
  - Violation of the Law of Demeter
- [ ] Middle Man — Does a class delegate most of its methods to another object?
  - Would removing the intermediary and calling directly be better?
- [ ] Insider Trading — Do modules exchange internal information excessively?
  - Does one module depend on another's implementation without a formal interface?

**Other:**
- [ ] Global Data — Is there mutable shared data accessible from anywhere via globals or singletons?
- [ ] Mutable Data — Is there data that could be made immutable but isn't?
- [ ] Loops — Are there imperative loops replaceable with pipelines (map/filter/reduce)?

---

## 4. Test Quality ⭐

> Tests safeguard the quality of design and code. The quality of tests themselves matters equally.

**Test Coverage:**
- [ ] Is core business logic tested?
- [ ] Are all public APIs tested?
- [ ] Are edge cases tested?
- [ ] Are error paths tested?
- [ ] Are boundary values tested?

**Implementation Correctness Verification:**
- [ ] Do tests accurately verify actual requirements?
- [ ] Can you be confident the feature works correctly when tests pass?
- [ ] Are there weak tests that would pass even with an incorrect implementation?
- [ ] Are assertions sufficiently specific?

**Test Design:**
- [ ] Are tests independent? (can run without affecting each other)
- [ ] Are tests deterministic? (always produce the same result)
- [ ] Are tests fast? (maintaining the feedback loop)
- [ ] Are tests separated into meaningful units?

**Test Quality:**
- [ ] Do test names clearly reveal their intent?
- [ ] Do tests follow the Given-When-Then / Arrange-Act-Assert structure?
- [ ] Does each test verify exactly one behavior?
- [ ] Is test code readable? (tests are documentation too)
- [ ] Is the test's intent immediately clear?

**Blackbox Testing Principles:**
- [ ] Do tests verify **behavior/outcomes** rather than implementation details?
- [ ] Do tests verify through the **public interface** rather than internal state?
- [ ] Will tests break unnecessarily when implementation changes?
- [ ] Do tests focus on "what" rather than "how"?

**Mock/Stub Minimization:**
- [ ] Are mocks used **only where essential**? (external dependencies, I/O, etc.)
- [ ] Do excessive mocks render any test meaningless?
- [ ] Are there places where real objects could replace mocks?
- [ ] Does mock behavior match the actual implementation?

**Test Maintainability:**
- [ ] Are there brittle tests prone to breaking?
- [ ] Is there excessive duplication in test code?
- [ ] Are test helpers/fixtures used appropriately?
- [ ] Is it easy to diagnose the root cause when a test fails?

**Test Type Balance:**
- [ ] Are there sufficient unit tests?
- [ ] Are integration tests appropriate?
- [ ] Are E2E tests present where needed?
- [ ] Is the test pyramid balanced?

---

## 5. Additional Review Criteria (Apply as Applicable)

> Apply the following criteria based on project characteristics.

**Concurrency/Parallelism** (when applicable):
- [ ] Is there a risk of race conditions?
- [ ] Is there a risk of deadlocks?
- [ ] Is it thread-safe?

**Database** (when applicable):
- [ ] Is the schema design properly normalized?
- [ ] Are indexes appropriate?
- [ ] Are transaction boundaries correct?

**API Design** (when applicable):
- [ ] Does it follow RESTful principles?
- [ ] Is there a versioning strategy?
- [ ] Are error responses consistent?

**UI/UX** (when applicable):
- [ ] Is accessibility (a11y) considered?
- [ ] Is the design responsive?
- [ ] Are loading/error states handled?

**Other:**
- [ ] Is logging sufficient and appropriate?
- [ ] Is configuration separated by environment?
- [ ] Is it ready for deployment?
