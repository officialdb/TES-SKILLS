# Architecture Review Checklist

- [ ] Does the proposed architecture respect existing system boundaries?
- [ ] Are interfaces explicit, strictly typed, and minimal?
- [ ] Is business logic cleanly decoupled from persistence and network protocols?
- [ ] Has an ADR been drafted if a new paradigm or core technology is introduced?
- [ ] Are failure modes, retry policies, and circuit breakers designed for network boundaries?
- [ ] Is there an obvious path for horizontal or modular scalability?
- [ ] Have security boundaries (trust levels, authentication points) been clearly demarcated?
