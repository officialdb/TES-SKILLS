# Reference: Background Processing & Asynchronous Systems

## 1. When to Use Background Workers

Do not introduce distributed queues when ordinary synchronous processing suffices. Use asynchronous background task queues specifically for:
- Operations with high latency (generating PDFs, processing videos, resizing images).
- External communications susceptible to transient network delays (sending emails, SMS, webhook dispatches).
- Periodic scheduled maintenance (daily reporting, data aggregations, archiving expired records).
- Batch ingestion and bulk imports.

## 2. Queue Technologies by Ecosystem

- **Python:** Celery (Redis/RabbitMQ broker), Dramatiq, RQ (Redis Queue), Arq.
- **PHP:** Laravel Queues (database, Redis, SQS driver), Symfony Messenger.
- **JavaScript / TypeScript:** BullMQ (Redis-based), Temporal, RabbitMQ / AMQP clients.
- **Java:** Spring Batch, JMS, Kafka, RabbitMQ listeners.

## 3. Idempotency & Exactly-Once Semantics

In distributed queue architectures, network timeouts and retries guarantee **at-least-once delivery**, not exactly-once delivery. Consequently, every background worker job must be strictly **idempotent**: executing a job multiple times with the same payload must produce the exact same result without unintended duplicates.

### Implementing Idempotency Keys
```python
def process_payment_webhook(event_id: str, payload: dict):
    # Check if event was already recorded and processed
    with transaction.atomic():
        processed = ProcessedWebhookEvent.objects.select_for_update().filter(event_id=event_id).first()
        if processed:
            logger.info("Skipping duplicate webhook event", extra={"event_id": event_id})
            return

        # Record event before executing mutations
        ProcessedWebhookEvent.objects.create(event_id=event_id, status="PROCESSING")
        apply_payment_update(payload)
        ProcessedWebhookEvent.objects.filter(event_id=event_id).update(status="COMPLETED")
```

## 4. Retries, Backoff & Dead-Letter Queues (DLQ)

- **Exponential Backoff with Jitter:** When a transient error occurs (e.g. external payment API timeout), retry with exponentially increasing delays (`delay = base * (2 ** retry_count) + random_jitter`) to prevent hammering downstream services.
- **Max Retry Limits:** Enforce strict retry caps (e.g. 3–5 attempts). Never allow infinite retry loops that exhaust queue capacity.
- **Dead-Letter Queue (DLQ):** Route messages that persistently fail beyond maximum retry thresholds to a dedicated dead-letter queue. Trigger alerts for operational inspection.
- **Graceful Shutdown (`SIGTERM`):** Workers must handle shutdown signals by completing current in-flight jobs and rejecting new jobs before exiting.

