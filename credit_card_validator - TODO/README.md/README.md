# Credit Card Validator & Revenue Aggregator with Recurring Invoice Tracker

## Prompt:

You are building a financial application that handles customer transactions and invoice processing. You need to implement the following functionality:

1. **Validate a Credit Card Number** using the Luhn algorithm.
2. **Aggregate Transaction Revenue** from multiple customers, ensuring you handle non-digit characters (like spaces and dashes) in credit card numbers.
3. **Track Recurring Invoices** by checking whether customers need to be invoiced today, based on the frequency of their billing cycle.

---

## Steps:

### 1. Credit Card Validator

**Task:**

Write a function that takes a string representing a credit card number and returns `True` if it’s valid according to the **Luhn algorithm**, and `False` otherwise. 

**Requirements:**

- Handle non-digit characters gracefully (e.g., spaces, dashes) by stripping them before validation.

#### Example Input:
```python
"4539-9767-4151-2043"
```
#### Example Output:
`True`

**Luhn Algorithm:**
- Reverse the string of digits.
- Double every second digit from the right, and if the result is greater than 9, subtract 9 from it.
- Sum all the digits.
- The number is valid if the total sum modulo 10 is 0.



### 2. Revenue Aggregator

**Task:**

You are given a list of transaction records, each represented by a dictionary containing the following fields:

id: The transaction ID
amount: The transaction amount (in dollars)
currency: The currency of the transaction

Write a function that returns the total revenue in cents across all transactions.

### Example Input:
```python
[
  {"id": 1, "amount": 1000, "currency": "USD"},
  {"id": 2, "amount": 500, "currency": "USD"},
  {"id": 3, "amount": 1500, "currency": "EUR"}
]
```

### Example Output:
```python
300000  # (1000 + 500 + 1500) * 100 = 300000 cents
```

## 3. Recurring Invoice Tracker

**Task:**

Given a list of customers with their last invoice date and the frequency of their billing cycle (either "monthly" or "weekly"), write a function that returns a list of customers who need to be invoiced today.

Assume today's date is "2025-01-01".

### Example Input:
```python
[
  {"customer_id": "cus_1", "last_invoiced": "2024-12-01", "frequency": "monthly"},
  {"customer_id": "cus_2", "last_invoiced": "2024-12-25", "frequency": "weekly"},
  {"customer_id": "cus_3", "last_invoiced": "2025-01-01", "frequency": "monthly"}
]
```
## Example Output:

```python
["cus_2", "cus_3"]
```

**Requirements:**

- Weekly invoices need to be generated every 7 days from the last invoice date.
- Monthly invoices should be generated on the same day of the month, but ensure you handle edge cases (e.g., for February or months with fewer days).
- Use datetime to manipulate the dates appropriately.

**Additional Notes:**

- Ensure you handle edge cases correctly, such as:
- Non-digit characters in credit card numbers.
- Different lengths of months (e.g., February, months with 30 vs 31 days).
- Missing or malformed transaction records.
- Provide clear function signatures for each of the tasks.
- Use unit tests to validate the correctness of your solutions