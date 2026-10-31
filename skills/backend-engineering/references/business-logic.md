# Reference: Business Logic Encapsulation & Application Services

## 1. Encapsulating Business Rules

Business rules define how an organization creates, validates, transforms, and calculates domain data. They represent the core intellectual property of the software.

### Anti-Patterns to Eliminate
- **Fat Controllers:** Placing validation, business calculations, SQL queries, and email dispatch inside route handler functions.
- **Scattered Rules:** Duplicating the same pricing, discount, or tax calculations across web controllers, mobile API handlers, background workers, and frontend clients.
- **Anemic Domain Models:** Treating models solely as dumb property bags while all business procedures live in monolithic controller scripts.

### The Service Layer Pattern
Encapsulate cohesive use cases inside focused application service classes or functions:

```python
class CreateSubscriptionService:
    def __init__(self, user_repo, payment_gateway, billing_repo, event_bus):
        self.user_repo = user_repo
        self.payment_gateway = payment_gateway
        self.billing_repo = billing_repo
        self.event_bus = event_bus

    def execute(self, user_id: str, plan_id: str, payment_token: str) -> Subscription:
        # 1. Load domain entities
        user = self.user_repo.get_by_id(user_id)
        
        # 2. Check domain preconditions
        if user.has_active_subscription():
            raise SubscriptionConflictError("User already has an active subscription")

        # 3. Coordinate external service & persistence inside transaction
        with transaction.atomic():
            charge = self.payment_gateway.charge(payment_token, plan.amount)
            subscription = self.billing_repo.create_subscription(user, plan_id, charge.id)
            user.mark_subscribed()
            self.user_repo.save(user)

        # 4. Dispatch side-effects asynchronously
        self.event_bus.publish(SubscriptionCreatedEvent(subscription.id))
        return subscription
```

## 2. Transaction Boundaries & Invariant Protection

- **Atomic Transactions:** Wrap multi-record state changes in database transactions. If payment recording fails, user subscription state must not be committed.
- **Transaction Scope:** Keep database transactions as short as possible. Never execute slow external HTTP requests inside an open database transaction block. Execute external API calls before or after the atomic database commit.
- **State Machine Integrity:** Model complex entity lifecycles (e.g. `Order: Pending -> Paid -> Shipped -> Delivered -> Cancelled`) with explicit transition guards. Prevent illegal state jumps (e.g. `Delivered -> Pending`).

## 3. Error Handling and Domain Exceptions

- Define meaningful domain exceptions (`ResourceNotFoundError`, `InsufficientInventoryError`, `PaymentDeclinedError`) rather than throwing generic runtime errors.
- Let application services raise domain exceptions; allow outer HTTP middleware to catch and serialize them into standard HTTP status responses.

