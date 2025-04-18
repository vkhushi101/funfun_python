# 💳 Account Transaction & Payment Scheduler Service

## 📌 Overview

Design and implement a financial system that supports real-time and scheduled money operations across multiple accounts. The service must allow creation of accounts, transaction processing (deposits/withdrawals), and scheduling and cancellation of future payments. It must also produce structured, nested summaries of activity suitable for audit, reporting, and analytics.

You will be expected to implement core methods and consider edge cases for each. Clear data manipulation and proper handling of nested structured output are essential.

---

## 🧩 Functional Requirements

### `create_account(account_id: str, initial_balance: int) -> bool`

- Registers a new account with the given `initial_balance`.
- Returns `True` if successful, or `False` if the account already exists.

🧠 **You must consider**:
- Duplicate account creation
- Validity of initial balances (e.g., negative values)

---

### `deposit(timestamp: int, account_id: str, amount: int) -> bool`

- Deposits the given `amount` into the account at `timestamp`.
- Returns `False` if the account does not exist.

🧠 **Edge cases** to consider:
- Deposit of `0`
- Large amounts
- Invalid timestamps (e.g., past timestamps if applicable)

---

### `withdraw(timestamp: int, account_id: str, amount: int) -> bool`

- Withdraws the given `amount` at `timestamp`.
- Returns `False` if:
  - Account doesn’t exist
  - Insufficient balance

🧠 Consider:
- Multiple withdrawals at the same timestamp
- Withdrawals that reduce balance to exactly zero

---

### `schedule_payment(timestamp: int, account_id: str, amount: int, delay: int) -> str | None`

- Schedules a payment to be executed at `timestamp + delay`.
- Returns a unique ID like `"payment1"`, `"payment2"`, etc.
- Returns `None` if the account doesn't exist.

📋 Rules:
- Scheduled payments are executed before other transactions at that timestamp.
- If multiple scheduled payments exist for the same timestamp, execute in creation order (`payment1` before `payment2`).
- Skipped if insufficient balance at execution time.
- Successful payments are outgoing transactions and impact spender ranking.

🧠 Think about:
- Scheduling with `delay = 0`
- Duplicate schedules
- Back-to-back payments at same timestamp

---

### `cancel_payment(timestamp: int, account_id: str, payment_id: str) -> bool`

- Cancels a scheduled payment.
- Returns `True` if successfully canceled, `False` if:
  - Payment doesn’t exist
  - Belongs to another account
  - Already executed or canceled

📋 Scheduled payments must be executed before cancel operations at a given timestamp.

🧠 Consider:
- Canceling already executed payments
- Timing issues with same-timestamp execution and cancel

---

### `process(timestamp: int) -> None`

- Triggers:
  1. Scheduled payments execution
  2. Cancellation operations
  - In that order for the given timestamp.

🧠 Consider:
- Executing multiple scheduled payments and cancel requests
- Order of operations at the same timestamp
- How to update account balances and logs

---

### `get_account_summary(account_id: str) -> dict`

Returns a nested summary for the account.

**Output Format:**
```json
{
  "balance": 1300,
  "transactions": {
    "deposit": [{"timestamp": 1, "amount": 1000}],
    "withdrawal": [{"timestamp": 2, "amount": 200}]
  },
  "payments": {
    "pending": [{"id": "payment3", "scheduled_for": 10, "amount": 500}],
    "completed": [{"id": "payment1", "executed_at": 3, "amount": 300}],
    "skipped": [{"id": "payment2", "attempted_at": 5, "amount": 700}]
  }
}
