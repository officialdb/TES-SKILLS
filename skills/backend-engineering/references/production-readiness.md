# Reference: Production Readiness & Operational Hygiene

## 1. Health Checks & Probes

Production container orchestrators (Kubernetes, ECS, Docker Swarm) require standardized health endpoints:

### Liveness Probe (`/health/live`)
- *Purpose:* Verifies that the application process is running and responding.
- *Behavior:* Returns `200 OK` immediately if the HTTP server process is responsive. If this check fails continuously, the orchestrator restarts the container.
- *Caution:* Do not query external databases or downstream dependencies in liveness probes. A database network hiccup must not cause cascading container restarts.

### Readiness Probe (`/health/ready`)
- *Purpose:* Verifies that the application is fully initialized and capable of accepting user traffic.
- *Behavior:* Performs lightweight checks on critical dependencies (database connection ping, Redis ping).
- *Response:* Returns `200 OK` when ready; returns `503 Service Unavailable` during startup, migration execution, or fatal connection loss. The load balancer routes traffic only to containers reporting ready.

## 2. Graceful Shutdown & Process Lifecycle

When a server container receives a termination signal (`SIGTERM` or `SIGINT`):
1. **Stop Accepting New Ingress:** The readiness probe flips to unready, causing the load balancer to remove the node from active rotation.
2. **Drain In-Flight Requests:** Complete all ongoing HTTP requests and transactions within a configured grace period (e.g. 15–30 seconds).
3. **Finish In-Flight Worker Jobs:** Background worker processes finish their active job and refrain from pulling new tasks off the queue.
4. **Close Persistence Pools:** Cleanly close database connection pools, Redis clients, and file handles.
5. **Exit Cleanly:** Terminate the process with status code 0.

## 3. Database Migration Pre-Flight Checks

- **Run Migrations Separately:** Execute schema migrations as a dedicated release pre-flight step (Kubernetes Job or CI/CD deployment phase) before routing traffic to newly deployed application containers.
- **Backward-Compatible Schema Changes:** Ensure database migrations are backward-compatible with currently running application instances so rollbacks can proceed without database corruption.

## 4. Resource Constraints & Worker Tuning

- **Worker Process Sizing:** In prefork or multiprocessing models (Gunicorn, uWSGI, PHP-FPM), size worker counts based on available CPU cores: `(2 * CPU_CORES) + 1` for I/O bound workloads.
- **Memory Thresholds:** Set memory limits per container and configure worker recycling (e.g. `max_requests = 1000`) to prevent slow memory leaks from exhausting server memory.

