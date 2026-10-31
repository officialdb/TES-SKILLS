# Reference: Domain Modeling and Module Boundaries

## Bounded Contexts
A Bounded Context defines a tangible boundary within which a domain model applies. Inside the boundary, all terms in the Ubiquitous Language have a specific, unambiguous meaning.

## Designing Deep Modules (John Ousterhout Philosophy)
- The best modules provide powerful functionality through a simple interface.
- A "shallow" module has an interface that is complex relative to the functionality it provides. Shallow modules increase cognitive load without reducing complexity.
- A "deep" module hides messy details (e.g., caching, serialization, retries, file formats) completely behind a concise set of methods.
