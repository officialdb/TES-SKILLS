# Reference: Database Persistence, Transactions & Data Integrity

## 1. Persistence Patterns & ORM Hygiene

Object-Relational Mappers (ORMs) simplify data access, but improper usage introduces severe performance regressions and concurrency hazards.

### Eliminating the N+1 Query Antipattern
The N+1 problem occurs when an application executes 1 query to fetch N parent records, and then sequentially executes N additional queries in a loop to fetch child associations.

- **Bad (N+1 Queries):**
  ```python
  posts = db.query(Post).limit(50).all()  # 1 query
  for post in posts:
      print(post.author.name)             # 50 separate queries!
  ```
- **Good (Eager Loading via Joins):**
  ```python
  # Python / SQLAlchemy: joinedload or selectinload
  posts = db.query(Post).options(joinedload(Post.author)).limit(50).all()
  
  # PHP / Laravel Eloquent: eager loading
  # $posts = Post::with('author')->limit(50)->get();
  
  # Node.js / Prisma: include
  # const posts = await prisma.post.findMany({ include: { author: true }, take: 50 });
  ```

### Selecting Only Necessary Columns
Avoid `SELECT *` on wide tables with heavy JSONB or text blobs. Project only the columns required for the current use case (`.values('id', 'name')` or `.select(['id', 'email'])`).

## 2. Transactions & Concurrency Control

### Concurrency Hazards
- **Lost Updates:** Two processes read balance \$100, one adds \$20, the other subtracts \$10, leading to inaccurate overwrites.
- **Race Conditions:** Two simultaneous requests redeem the last available ticket.

### Locking Strategies
- **Optimistic Locking:** Add an integer `version` or timestamp column. Update succeeds only if `version == expected_version`. If a collision occurs, retry or reject the transaction. Recommended for read-heavy workflows.
- **Pessimistic Locking (`SELECT ... FOR UPDATE`):** Locks the targeted database rows until the current transaction commits. Prevents race conditions during critical balance or inventory changes:
  ```sql
  SELECT * FROM bank_accounts WHERE id = 42 FOR UPDATE;
  ```

## 3. Database Migrations & Zero-Downtime Releases

- **Deterministic Version-Controlled Migrations:** Every schema alteration (tables, columns, indexes, foreign keys) must be tracked via migration files (Alembic, Flyway, Laravel Migrations, Prisma Migrate).
- **Expand / Contract Pattern for Zero-Downtime Deployments:**
  1. *Phase 1 (Expand):* Add new column as nullable; deploy code that writes to both old and new columns.
  2. *Phase 2 (Backfill):* Run a background migration to backfill historical records.
  3. *Phase 3 (Switch):* Deploy code reading exclusively from the new column.
  4. *Phase 4 (Contract):* Drop the deprecated old column in a subsequent release.
- **Index Creation on Production:** Avoid locking production tables when adding indexes. Use concurrent indexing options where supported (e.g. `CREATE INDEX CONCURRENTLY` in PostgreSQL).

