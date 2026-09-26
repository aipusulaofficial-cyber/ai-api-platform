# AI API Platform

A contract-first API service for AI workloads, built around explicit validation, version boundaries, normalized failures and operational health signals.

## What this project does
The service validates API requests at the boundary, executes domain operations through replaceable adapters, and returns stable response and error contracts.

## Runtime architecture
```text
Client
  -> API boundary / validation
  -> domain service
  -> infrastructure adapters
  -> response contract
```

Operational endpoints expose separate liveness and readiness signals. Requests carry correlation context so failures can be traced across the service.

## Contracts
- Input validation happens before domain execution.
- API versions have explicit compatibility boundaries.
- Domain errors are translated into stable transport errors.
- External dependencies are not part of the public API contract.
- Malformed, unauthorized and dependency-failure paths are tested.

## Runtime & deployment
The container runs as non-root user `10001`, exposes port `8000`, and includes a live healthcheck. Kubernetes deployment uses two replicas with readiness and liveness probes.

The deployment manifest currently uses an image tag of `latest`; production promotion should use immutable release identifiers.

## Quality gates
CI, production tests and security/SBOM validation run on changes. The repository demonstrates an executable API lifecycle rather than a documentation-only architecture.

## Evidence
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Engineering contract: [docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md)
- Deployment: [deploy/kubernetes.yaml](deploy/kubernetes.yaml)