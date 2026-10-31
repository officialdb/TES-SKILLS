# Test Plan Template

**Target Feature / Bugfix:** [Name]  
**Primary Test Framework:** [e.g. pytest, vitest, jest]  

---

## 1. Test Matrix

| Test Scenario | Test Type | Expected Outcome |
|---|---|---|
| Valid input happy path | Unit | Returns success payload with status 200 |
| Empty input payload | Unit | Raises `ValidationError` with descriptive message |
| Network timeout during call | Integration | Retries 3 times, then falls back gracefully |
| Concurrent access race condition | Integration | Atomic lock prevents double-spend |

---

## 2. Test Execution & Pass Proof
```bash
# Command used to run tests
pytest tests/unit/test_feature.py -v
```
