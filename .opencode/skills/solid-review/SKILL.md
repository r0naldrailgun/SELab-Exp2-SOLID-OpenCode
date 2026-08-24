---
name: solid-review
description: Analyze a codebase for concrete SOLID violations, separate design smells from confirmed violations, propose minimal refactorings, require explicit approval before implementation, and verify behavior afterward.
compatibility: opencode
---

# solid-review Skill

## Purpose
A project-local OpenCode skill for systematic SOLID principle analysis. Helps agents:
1. Inspect a codebase for all five SOLID principles
2. Identify **concrete, code-specific** violations (not generic textbook examples)
3. Map each violation to exact file/class/method
4. Explain **why** it violates that specific principle
5. Recommend **minimal, appropriate** refactoring patterns
6. Explain expected benefits
7. **Never refactor without explicit user approval**
8. Implement only approved changes
9. Verify behavior after implementation

---

## Core Rules

### 1. No Generic Answers
- Every finding must reference: exact file, class, method, line numbers, code snippet
- No "consider using interfaces" — say "introduce `PaymentStrategy` protocol at `payment.py:4`"
- No "decouple modules" — say "constructor-inject `DiscountCalculator` into `OrderService.__init__`"

### 2. Strict SOLID Definitions
- **SRP**: Multiple independent *reasons to change* (behavioral), not just multiple methods/fields
- **OCP**: Must modify existing code to add new behavior (if/elif chains, hardcoded types)
- **LSP**: Subtype breaks behavioral contract of supertype (observable misbehavior)
- **ISP**: Client/implementation forced to depend on operations it doesn't need
- **DIP**: High-level policy directly constructs low-level concretions

### 3. Separate Design Smells from SOLID Violations
- Direct property access (`order.customer.credit_card`) = coupling/Law of Demeter, **not DIP**
- Large class = maintenance concern, **not automatically SRP/ISP**
- Data-rich entity = domain modeling, **not automatically SRP**

### 4. Approval Gate
- Present findings → user approves specific refactorings → implement only approved
- One refactoring at a time; verify after each

---

## Workflow

### Phase 1: Discovery (Read-Only)
```
1. Map project structure: entrypoints, domain models, services, infrastructure
2. Identify high-level orchestrators (use-case classes like OrderService)
3. Identify concrete implementations (PaymentProcessor, MySqlDatabase, etc.)
4. Trace dependencies: who constructs whom, who calls whom
```

### Phase 2: Principle-by-Principle Analysis
For each principle, produce findings in this format:

```
**Principle:** [SRP/OCP/LSP/ISP/DIP]
**Status:** Violated / Followed / Partially
**Location:** `path/file.py`, `ClassName.method()` (lines X-Y)
**Evidence:** [code snippet or behavioral description]
**Why this violates [PRINCIPLE]:** [specific to this code, not textbook]
**Consequence:** [practical impact in this project]
**Refactoring:** [minimal pattern: protocol, composition, injection, etc.]
**Benefit:** [testability, extensibility, isolation, etc.]
**Confidence:** High/Medium/Low
```

### Phase 3: Synthesis
- Summary table: principle → primary violation → action
- Confirmed violations (clear SOLID match)
- Design smells (not SOLID)
- Refactoring order (dependencies first)

### Phase 4: Approval & Implementation
- Present proposed refactorings before implementation
- Wait for explicit user approval
- Approval may cover one specific refactoring or the complete reviewed plan
- Implement only the approved changes
- Verify after implementation

---

## Principle-Specific Guidance

### SRP
- Look for: orchestrators doing validation + pricing + payment + persistence + notification + formatting
- Ask: "If shipping rules change, must I touch the payment code?"
- Refactor: extract single-responsibility collaborators; orchestrator coordinates

### OCP
- Look for: `if/elif/else` on type strings, `isinstance` chains, hardcoded concrete classes
- Ask: "Can I add a new payment method without editing this file?"
- Refactor: Strategy pattern with protocol + registry/dict dispatch

### LSP
- Look for: inheritance where subtype initializes parent state incorrectly, overrides with exceptions
- Ask: "Does substituting subtype for supertype produce wrong output?"
- Refactor: composition + protocol, or fix behavioral contract

### ISP
- Look for: fat interfaces where implementations raise `NotImplementedError`, clients unused methods
- Ask: "Does any implementer stub out methods? Does any caller use only a subset?"
- Refactor: split into granular protocols; inject only needed ones

### DIP
- Look for: high-level class `new ConcreteLowLevel()` in `__init__`
- Ask: "Can I test this with a fake? Can I swap the DB without editing this class?"
- Refactor: constructor injection + protocols owned by high-level

---

## Refactoring Patterns Catalog (Minimal)

| Pattern | When | Example |
|---------|------|---------|
| **Protocol + Constructor Injection** | DIP violation | `OrderService.__init__(self, payment: PaymentProcessor)` |
| **Strategy + Registry** | OCP violation (if/elif on type) | `PaymentProcessor.strategies: Dict[str, PaymentStrategy]` |
| **Composition over Inheritance** | LSP violation (broken subtype) | `BundleOrder` has `orders: List[Order]`, implements `OrderLike` |
| **Interface Segregation** | ISP violation (fat interface) | Split `Notifier` → `EmailSender`, `SmsSender` protocols |
| **Single-Responsibility Extraction** | SRP violation (god method) | `OrderValidator`, `PricingService`, `ReceiptFormatter` |

---

## Verification Checklist
After each approved refactoring:
- [ ] Run existing demo: `python -m store.main` (or project equivalent)
- [ ] Compare output to `evidence/original-baseline.txt` if exists
- [ ] Verify all payment methods still work
- [ ] Verify discount rules unchanged
- [ ] Verify bundle behavior corrected (if LSP fix)
- [ ] No new dependencies added

---

## Example Output Format (for agent)

```
## SOLID Analysis: 02-Applied-OOD-Principles

### SRP — Violated
**Location:** `store/order_service.py`, `OrderService.process_order()` (15-43)
**Evidence:** 7 responsibilities in one method: validate, price, ship, pay, persist, notify, print
**Why:** Shipping change → edit payment code; notification change → edit validation code
**Refactoring:** Extract `OrderValidator`, `PricingService`, `PaymentProcessor`, `OrderRepository`, `NotificationSender`, `ReceiptFormatter`; `OrderService` orchestrates
**Benefit:** Each class has one reason to change; testable in isolation
**Confidence:** High

### OCP — Violated
**Location:** `store/payment.py`, `PaymentProcessor.process()` (8-24)
**Evidence:** `if method == "credit_card": ... elif method == "paypal": ...`
**Why:** Adding cash requires editing this method
**Refactoring:** `PaymentStrategy` protocol; `PaymentProcessor` holds `Dict[str, PaymentStrategy]`
**Benefit:** New payment = new class + registration, zero edits to processor
**Confidence:** High
...
```

---

## Usage Examples

Ask the Agent:

> Use the `solid-review` Skill to analyze
> `02-Applied-OOD-Principles`. Do not modify files.

For refactoring:

> Use the `solid-review` Skill and propose a minimal refactoring plan for the
> confirmed SOLID violations. Do not implement anything until I approve the plan.

For verification:

> Use the `solid-review` Skill to review the implemented refactoring and verify
> that the approved SOLID issues were addressed without unintended behavioral
> changes.

---

## Constraints
- **Avoid** unnecessary factories, dedicated registry classes, service locators,
  managers, deep hierarchies, and framework-like architecture.
- A simple injected dictionary/mapping of strategies is acceptable when it
  directly solves an OCP problem.
- **Always** preserve existing business behavior unless the behavior is the
  explicitly identified defect being refactored.
- Preserve existing payment flows and discount rules.
- `BundleOrder` behavior may change only as part of an explicitly approved LSP fix.
- **Never** propose: factories, registries, service locators, managers, deep hierarchies, framework code
- **Never** refactor without approval
- **Prefer** protocols over abstract base classes (Python 3.8+)
- **Prefer** composition over inheritance