# Testing Checklist

- [ ] Does every new feature or bugfix have a corresponding automated test?
- [ ] Are edge cases tested (empty input, boundaries, invalid types)?
- [ ] Are tests deterministic (no sleeps, hardcoded future dates, unseeded randoms)?
- [ ] Do tests use isolated temporary fixtures (`tmp_path`) without side-effects on disk?
- [ ] Are failure messages descriptive when an assertion fails?
- [ ] Does the full test suite run and pass without warnings?
