# ADR-0002: Production hardening and domain boundaries

## Context
The platform must demonstrate an executable domain model rather than a placeholder HTTP endpoint. The service boundary must remain stateless at request level, observable, testable and deployable.

## Decision
The core domain is implemented as API version validation and token-bucket admission control. FastAPI exposes the domain contract and maps expected validation failures to HTTP 400. Kubernetes and Helm provide bounded resources, probes, non-root execution, horizontal scaling and disruption protection. Terraform manages the Kubernetes Deployment and Service as infrastructure-as-code.

OpenTelemetry is configured through a dedicated module. Console export is the local fallback; when OTEL_EXPORTER_OTLP_ENDPOINT is present, spans are exported over OTLP. JSON logging keeps operational records machine-readable.

CI runs unit, contract/property, production smoke and supply-chain checks. Trivy scans dependencies/filesystem and CycloneDX emits an SBOM. Locust exercises the domain HTTP surface instead of a health-only endpoint.

## Failure modes
- Invalid domain input is rejected deterministically.
- State-machine violations fail closed with explicit errors.
- Expired or unauthorized data is rejected rather than silently accepted.
- Backend/telemetry failures must not corrupt domain state.
- Kubernetes readiness prevents traffic before the API is serving.

## Alternatives considered
A generic CRUD endpoint was rejected because it does not demonstrate domain invariants. External durable stores were not embedded in the reference implementation because that would couple the example to a provider; production deployments should externalize durable state, secrets and telemetry.

## Consequences
The repository now has an inspectable domain core, an API boundary, deployment contracts and operational controls. The next production integration point is replacing in-memory state with a durable store and configuring OTLP, secrets and cloud credentials through the deployment environment.
