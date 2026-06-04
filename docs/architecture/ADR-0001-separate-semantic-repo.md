# ADR-0001: Use a separate semantic repository

## Status

Accepted

## Decision

The Bible graph and chunking system should live in its own repository, separate from any future agent runtime or orchestration layer.

## Rationale

The Bible graph has different stability requirements from an agent runtime:

- source files must be immutable and license-tracked
- chunking and passage identity need scholarly validation
- schemas and relationship types need careful governance
- runtime agents will change more frequently than canonical data models

Separating the semantic repo lets the future runtime consume stable release artifacts without becoming the authority layer.

## Consequences

- Agent runtime integration must happen through export/API contracts.
- The semantic repo must have strong validation and release artifacts.
- Runtime-side tools may propose changes, but canonical changes still flow through repo governance.
