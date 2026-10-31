# Code Quality Checklist

- [ ] Does the implementation adhere to existing naming and formatting conventions?
- [ ] Are all types annotated and checked via static analysis?
- [ ] Are external inputs properly checked and validated at boundaries?
- [ ] Are edge cases (null/None, empty lists, out-of-bounds, network timeouts) explicitly handled?
- [ ] Have all unnecessary dependencies been avoided?
- [ ] Are errors raised with helpful context rather than swallowed silently?
- [ ] Are tests included and passing for all changed code paths?
