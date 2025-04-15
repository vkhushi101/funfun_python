# JSON Parsing

**Prompt:**

You are given two inputs:

1. A **Python dictionary** representing a JSON object, structured like this:

```python
{
  "point1": {
    "d1": "hello",
    "d2": 10,
    "d3": {
      "ed1": 1,
      "ed2": "asjdlkajs"
    }
  },
  "point2": {
    "d1": "goodbye",
    "d2": 5,
    "d3": {
      "ed1": 1,
      "ed2": "asjhdas"
    }
  },
  ...
}
```

Each top-level key (e.g., `"point1"`, `"point2"`) maps to a dictionary containing arbitrary nested fields.

1. A **key path string**, representing the field you want to index the data by. This key path can be:
    - A top-level key (e.g., `"d1"`)
    - A nested key using dot notation (e.g., `"d3.ed1"`)

---

**Your task:**

Write a function with the following signature:

```python
def reorganize_by_key_path(data: dict, key_path: str) -> dict:
```

This function should:

- **Output a new dictionary** where:
    - Each key is a **value found at the specified key path** in one or more of the original objects.
    - Each value is the **original object** (i.e., the value associated with `"point1"`, `"point2"`, etc.).
    - If **multiple objects** share the same value at the key path, group them into a **list**.
    - If only **one object** has a given key path value, use the object directly (i.e., **do not wrap it in a list**).

---

**Edge Cases & Requirements:**

- If the key path is **not present** in an object, **skip that object**.
- You can assume the key path will only consist of **dot-separated keys** (e.g., `"a.b.c"`) and will **not contain list indexing**.
- The values at the key path are **hashable** and can be used as dictionary keys.

**Example:**

Given this input:

```python
data = {
  "point1": {
    "d1": "hello",
    "d2": 10,
    "d3": {
      "ed1": 1,
      "ed2": "asjdlkajs"
    }
  },
  "point2": {
    "d1": "goodbye",
    "d2": 5,
    "d3": {
      "ed1": 1,
      "ed2": "asjhdas"
    }
  },
  "point3": {
    "d2": 100,
    "d3": {
      "ed1": 2
    }
  }
}
key_path = "d3.ed1"
```

The output should be:

```python
{
  1: [
    {
      "d1": "hello",
      "d2": 10,
      "d3": {
        "ed1": 1,
        "ed2": "asjdlkajs"
      }
    },
    {
      "d1": "goodbye",
      "d2": 5,
      "d3": {
        "ed1": 1,
        "ed2": "asjhdas"
      }
    }
  ],
  2: {
    "d2": 100,
    "d3": {
      "ed1": 2
    }
  }
}
```