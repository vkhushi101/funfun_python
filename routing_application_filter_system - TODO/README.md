# Logistics Routing & Application Filter System

## Overview

You are working on a logistics platform that routes packages through a network of international shipping lanes. Each shipping lane includes routing information and an associated **application ID** that authorizes the shipment.

Your task is to:

1. Parse a raw shipping lane string.
2. Filter the parsed data using a whitelist of valid application IDs.
3. Calculate shipping costs (both direct and indirect) between countries.

This challenge combines **string parsing**, **graph traversal**, and **filtering logic** — core skills in practical software engineering interviews.

---

## Input Format

### Shipping Lane String

You are given a single string that encodes one or more shipping lanes in the following format:

`[lengthOfAppId][APP_ID][Origin][Destination][Carrier][Cost]...[0]`

```md
- `lengthOfAppId` — a positive integer (1–2 digits)
- `APP_ID` — alphanumeric string of the given length
- `Origin` and `Destination` — 2-letter country codes (e.g., US, UK)
- `Carrier` — variable-length string with no digits (e.g., FedEx, UPS)
- `Cost` — integer (1–3 digits)
- Ends with a single character `0`
```

### Whitelist of Application IDs

You are also given a list of authorized (whitelisted) application IDs, e.g.:

```python
["A134141242"]

Example Input
"10A134141242USUKUPS520B12456435643456743USCAFedEx30CAUKDHL70"
Whitelist: ["A134141242"]
```

Your Tasks
### Part 1: Parse the Shipping Lanes

Write a function to parse the input string and return a list of structured lane dictionaries:

```python
[
  {"app_id": "A134141242", "from": "US", "to": "UK", "carrier": "UPS", "cost": 5},
  {"app_id": "B12456435643456743", "from": "US", "to": "CA", "carrier": "FedEx", "cost": 3},
  {"app_id": None, "from": "CA", "to": "UK", "carrier": "DHL", "cost": 7}
]
```
If there’s no application ID prefix before a shipping lane, set app_id: None.


### Part 2: Filter by Whitelist
Filter the shipping lanes to keep only those that:

- Have an app_id that exists in the whitelist, OR
- Have app_id set to None (i.e., unauthenticated lanes that are still allowed)

Expected output for the example above and whitelist ["A134141242"]:

```python
[
  {"app_id": "A134141242", "from": "US", "to": "UK", "carrier": "UPS", "cost": 5},
  {"app_id": None, "from": "CA", "to": "UK", "carrier": "DHL", "cost": 7}
]
```


### Part 3: Compute Shipping Cost
Write a function:

```python
def get_shipping_cost(lanes: List[dict], from_country: str, to_country: str) -> int
```
It should return the lowest total shipping cost from from_country to to_country, using one or more lanes.


Example usage:

```python
def get_shipping_cost(lanes, from_country="US", to_country="UK")  # → 5

Direct route: US → UK = 5
Indirect route: US → CA → UK = 3 + 7 = 10
Return the cheaper one (5)
```

Use Dijkstra's algorithm or a similar graph-based approach.

## Bonus
1. Add support for cost in multiple currencies: {"amount": 5, "currency": "USD"}

2. Build a CLI tool with flags:
--whitelist for loading whitelist
--from and --to to specify countries
--indirect to allow multi-hop routes only

