# Project: Data Transformation Engine (T Layer Challenge)
```
Duration: ~1 hour (Part 1)
Difficulty: Intermediate to Advanced
Domain: Fintech (Recurring Revenue, Investor Reporting)
Focus: Advanced JSON transformation, list comprehensions, nested data normalization, and algorithmic logic
```

## 📄 Background
You’ve been provided with raw JSON exports from various billing and customer platforms. Your job is to build the Transformation Layer (T of ETL) that normalizes and enriches this data for reporting purposes.

## 📦 Provided Files
raw_data/customers.json: Raw customer data from CRM

raw_data/invoices.json: Raw invoice data (including items, amounts, and timestamps)

raw_data/subscriptions.json: Subscription metadata per customer

The basic I/O logic and file reading is already provided. You're focusing entirely on transforming the raw JSON structures into analytics-ready formats.


**✅ Part 1 — Normalize & Join**
Transform the raw JSON into a flattened table structure with the following schema:

```
{
  "customer_id": "cus_123",
  "company_name": "Stripe, Inc.",
  "subscription_start": "2023-01-01",
  "subscription_status": "active",
  "monthly_revenue": 1500.0,
  "latest_invoice_date": "2024-04-01",
  "invoice_count": 14
}
```

*Details:*

- monthly_revenue is calculated by summing up recurring items from the invoices (use only items tagged "type": "recurring").
- Assume subscription start dates come from subscriptions.json.
- Skip customers who don’t have active subscriptions or invoices.

**⚠️ Edge Cases to Handle**
- Missing or null values in nested invoice items
- Duplicate invoices for the same month
- Customers with multiple active subscriptions (only take the earliest start date)
- Invoices in foreign currencies (convert to USD using a dummy conversion dict)
- Incomplete months (e.g., customer started mid-month — prorate revenue)

*🧩 Part 2 — Risk Rating Algorithm (Uncovered During Interview)*

Add a risk_rating to each customer, based on:
- "High" risk: more than 1 missed invoice or revenue drop in last 3 months
- "Medium" risk: no growth in last 3 months
- "Low" risk: steady or increasing monthly revenue
- You may need to build a revenue_trend list for last 3 months first

🛠 Suggested Tools
```
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
import json
from decimal import Decimal
```

**💡 Stretch Goals**
- Export your final transformed output to a CSV
- Add memoization or caching if customer volume is high
- Include a CLI layer or minimal FastAPI endpoint to trigger transformation

