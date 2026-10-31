# Pull Request Review Checklist

### Standards (Axis 1)
- [ ] Conforms to repository formatting and lint rules
- [ ] No unhandled exceptions or empty catch/except blocks
- [ ] Types are annotated without using unsafe escape hatches (`any`, raw dicts)
- [ ] Unit or integration tests cover changed code paths
- [ ] No security anti-patterns (unparameterized SQL, unescaped HTML, leaked secrets)

### Specification (Axis 2)
- [ ] Fulfills all explicit requirements from the ticket/issue
- [ ] Correctly handles zero, null, boundary, and negative input states
- [ ] No regressions introduced in unrelated components
- [ ] Public API contracts preserved or versioned appropriately
