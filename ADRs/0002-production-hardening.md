# ADR-0002: Production hardening
The versioned API edge is FastAPI with OpenTelemetry tracing. Kubernetes defines bounded probes/resources; Helm packages releases; Terraform owns infrastructure inputs. Trivy/CycloneDX enforce security and SBOM; contract/property tests protect the HTTP surface; Locust provides load traffic.
Production externalizes state, secrets, telemetry and rate-limit coordination.
