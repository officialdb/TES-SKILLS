# Reference: Caching & Performance Engineering

## 1. Evidence-Based Optimization

Never optimize based on assumptions. Profile and measure bottlenecks before introducing caching or complex concurrency:
- **Measure First:** Use APM tools, query logs (`pg_stat_statements`, slow query log), and memory profilers to identify where latency actually originates.
- **The Performance Hierarchy:**
  1. Fix algorithmic inefficiencies and eliminate unnecessary database round-trips (N+1 queries).
  2. Add appropriate database indexes (`EXPLAIN ANALYZE` verification).
  3. Introduce caching only after database access patterns are optimized.

## 2. Multi-Tier Caching Strategies

```text
Client / CDN Edge Cache (HTTP Cache-Control, ETag, 304 Not Modified)
           │
           ▼
Application Memory Cache (In-process LRU cache for static lookup tables)
           │
           ▼
Shared Cache Store (Redis / Memcached for session state, API responses)
           │
           ▼
Database Query Cache & Materialized Views
```

### Cache Patterns
- **Cache-Aside (Lazy Loading):**
  1. Application checks cache for key.
  2. If cache hit, return cached value.
  3. If cache miss, read from primary database, write to cache with TTL, and return result.
- **Write-Through / Write-Behind:** Write updates directly to both cache and database simultaneously, ensuring high cache consistency.

### Cache Invalidation: The Real Challenge
- **Time-to-Live (TTL):** Always attach a sensible expiration time (TTL) to cached entries. Never store indefinite keys without explicit eviction policies.
- **Event-Driven Invalidation:** When an entity is updated or deleted, broadcast a cache invalidation event targeting the specific entity key (e.g. `cache.delete(f"user:{user_id}")`).
- **Cache Stampede (Thundering Herd) Protection:** When a hot cache key expires, hundreds of concurrent requests may hit the database simultaneously. Mitigate using mutex locks (probabilistic early expiration or distributed locks) so only one process recomputes the cache while others await the result.

## 3. Concurrency & Resource Hygiene

- **Connection Pool Tuning:** Configure minimum and maximum connection pool sizes matching CPU core count and database server capacity. Release database and Redis connections back to the pool immediately upon request completion.
- **Non-Blocking I/O:** In async runtimes (Node.js, FastAPI / asyncio), never invoke blocking synchronous operations (e.g. `time.sleep()`, synchronous file reading) directly on the main event loop.

