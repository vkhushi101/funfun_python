Overview

We track compliance filings for businesses across all 50 U.S. states. Each state has its own **filing cadence** (e.g., annually, quarterly), and businesses can be **incorporated on any date**. Your task is to determine the **next due date** for each business's upcoming compliance filing, given its incorporation date, filing cadence, and today’s date.

This exercise tests your understanding of:
- Python’s `datetime` module
- Data modeling and manipulation
- Handling real-world scheduling logic

---

## Prompt

Write a function:

```python
def calculate_next_filing_dates(businesses: List[Dict[str, Any]], today: str) -> Dict[str, str]:
    ...
```
```bash
Parameters:
businesses: A list of dictionaries. Each dictionary represents a business and contains:

    business_id: A unique string
    incorporation_date: A string in "YYYY-MM-DD" format
    filing_cadence: One of "ANNUAL", "QUARTERLY", "SEMIANNUAL"
    state: A two-letter U.S. state abbreviation (e.g., "CA", "TX")
    today: A string representing the current date in "YYYY-MM-DD" format


Return
A dictionary mapping each business_id to the next filing due date as a "YYYY-MM-DD" string.
```

Example Input
```python
businesses = [
    {
        "business_id": "abc123",
        "incorporation_date": "2022-05-17",
        "filing_cadence": "ANNUAL",
        "state": "CA"
    },
    {
        "business_id": "xyz456",
        "incorporation_date": "2023-02-01",
        "filing_cadence": "QUARTERLY",
        "state": "TX"
    }
]
today = "2025-04-20"
```

Output
```python
{
  "abc123": "2025-05-17",
  "xyz456": "2025-05-01"
}
```

## Cadence Rules
```bash
ANNUAL: Filing is due every year on the incorporation anniversary.
QUARTERLY: Filing is due every 3 months from the incorporation date.
SEMIANNUAL: Filing is due every 6 months from incorporation.

If today is the same as a due date, return today's date.
Due dates must be in the future or today (never return a past date).
```