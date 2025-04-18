# 🧾 Billing Discrepancy Detector

## Overview

Middesk processes large volumes of invoices from its partners. Occasionally, discrepancies occur between the **amount billed** and the **actual usage** of services recorded in internal logs. This project is a tool to detect those discrepancies.

You are provided with three data files:

- `usage.csv` — Logs of customer service usage.
- `invoices.csv` — Records of invoiced amounts to customers.
- `pricing.json` — Unit pricing for each service type.

Your task is to identify billing discrepancies that exceed **$0.01** and output a clean, sorted report.

---

## 📂 Input Files

##### `usage.csv`
| customer_id | date       | service_type      | units_used |
|-------------|------------|-------------------|-------------|
| C123        | 2024-06-01 | email_validation  | 100         |
| C123        | 2024-06-01 | business_lookup   | 20          |

##### `invoices.csv`
| customer_id | date       | amount_billed |
|-------------|------------|----------------|
| C123        | 2024-06-01 | 12.00          |

##### `pricing.json`
```json
{
  "email_validation": 0.02,
  "business_lookup": 0.10,
  "monitoring": 0.05
}
```


## Objective

Write a program that:
1. Parses the input files.
2. Computes the expected charges by multiplying units_used with the appropriate unit_price.
3. Compares this computed total against the amount_billed.
4. Outputs a list of discrepancies greater than $0.01.

### Output Format
Output a CSV-formatted report to stdout or a file with the following headers:

```bash
customer_id,date,expected_amount,amount_billed,difference
```

### Example Output:
```bash
C123,2024-06-01,12.30,12.00,0.30
C456,2024-06-01,3.10,3.15,-0.05
```

* **Only include rows where |expected_amount - amount_billed| > 0.01**
* **Sort by customer_id, then date**


## Bonus
- Add CLI flags:
```
--overbilled → Show only rows where expected < billed
--underbilled → Show only rows where expected > billed
```
- Include basic unit tests for core logic.