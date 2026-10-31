# Threat Modeling Checklist

- [ ] Have all external entities and third-party APIs been identified?
- [ ] Are trust boundaries clearly drawn between untrusted and trusted zones?
- [ ] Has STRIDE been systematically applied to each boundary-crossing data flow?
- [ ] Are threats scored by impact and likelihood (e.g. DREAD or CVSS)?
- [ ] Is every identified threat paired with an actionable mitigation?
- [ ] Have mitigations been translated into automated unit or integration tests?
