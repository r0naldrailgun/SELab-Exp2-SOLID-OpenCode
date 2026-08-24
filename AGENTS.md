# AGENTS.md

## Project Overview

Python learning repo demonstrating OOD refactoring. Two identical copies of a store order-processing system:
- `01-Without-OOD-Principles/` — naive implementation
- `02-Applied-OOD-Principles/` — refactored version (currently identical to 01; refactoring in progress)

Each `store/` directory is a runnable Python package: `main.py` → `order_service.py` → `payment.py`, `pricing.py`, `storage.py`, `notification.py`.

## How to Run

```bash
# Run the demo (from repo root)
python -m 01_Without_OOD_Principles.store.main
python -m 02_Applied_OOD_Principles.store.main
```

Both versions print checkout receipts to stdout. No external dependencies; stdlib only.

## Key Facts

- **Language:** Python 3, dataclasses, type hints
- **No tests, no CI, no lint config, no requirements.txt** — repo is self-contained
- **`evidence/original-baseline.txt`** — binary baseline artifact (likely captured output for comparison)
- Both directories contain the same code; the `02-Applied-OOD-Principles/` variant is the target for OOD refactoring
- All imports use `store.` prefix (e.g. `from store.models import Order`), so each `store/` must be run as a package, not standalone scripts

## Experiment Rules

This repository contains two independent implementations of the same starter project.

- `01-Without-OOD-Principles` must preserve the original architecture.
- Do not refactor 01 while adding the cash-payment feature.
- `02-Applied-OOD-Principles` must be refactored for SOLID before cash payment is added.
- Never copy the cash implementation from 01 into 02.
- Before modifying code, describe the proposed changes and wait for user approval.
- Preserve existing credit-card, PayPal, and Bitcoin functionality.
- Run `python -m store.main` after implementation changes.
- Keep unrelated refactoring out of feature-specific changes.
