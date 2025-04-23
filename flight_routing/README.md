# Flight Route and URL Optimization System

## Problem Statement

You are building a travel application that requires efficient handling of flight routes, URL transformations, input cleaning, and HTTP request parsing. Implement a class-based solution to address the following requirements:

1.  **Flight Route Management System:** Given a string representing direct flights, implement functions to find the cost of a direct flight and the cheapest indirect flight route.
2.  **URL Compression with Minor Parts:** Implement a function to compress URL-like strings by shortening minor parts within major segments.
3.  **Stop Words Removal:** Implement a function to remove a list of stop words from an input string.
4.  **Sorting Strings with Alphanumeric Components:** Implement a function to sort a list of strings based on their alphabetical and numerical components.
5.  **HTTP Request Parsing:** Implement a function to parse HTTP request strings with two parameters and extract their values.

Your solution should be robust, handle edge cases gracefully, and provide clear function signatures.

---

## 1. Flight Route Management System

**Input Format:** A string of direct flights, e.g., `"UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8"`. Each entry is in the format `source:destination:airline:cost`.

**Tasks:**

* **Direct Flight Cost:** Write a function `direct_flight_cost(source: str, destination: str)` that returns the cost of the direct flight between the `source` and `destination`. If no direct flight exists, return `None`.

* **Cheapest Flight Route:** Write a function `cheapest_flight_route(source: str, destination: str)` that:
    * Returns the cheapest route between two cities as a list: `[source, intermediate1, intermediate2, destination]`.
    * The cost should be the sum of the flight costs for each leg of the journey.
    * If no route exists, return `None`.
    * Assume multiple indirect routes are possible, but only direct flights are provided as input.

## 2. URL Compression with Minor Parts**

**Task:**

* **URL Compression** Implement a function `compress_url(url: str, minor_parts: int)` that compresses a URL-like string based on the `minor_parts` parameter:
    * Split the input url into major parts separated by /.
    * For each major part, further split it into minor parts separated by ..
    * Compress each minor part by replacing the middle characters with the count of those characters. For example:
    ```
    "john" becomes "j2n"
    "doe" becomes "d1e"
    ```
    * Reconstruct the string with the compressed parts, keeping the major parts intact.

## 3. Stop Words Removal

**Task:**
* **Stripe stopwords**: Implement a function `stopwords_stripped(input_string: str, stop_words: List[str])` that removes stop words from an input string:
    * Convert the `input_string` to lowercase.
    * Remove all words present in the stop_words list from the lowercase string.
    * Return the cleaned string without the stop words.

## 4. Sorting Strings with Alphanumeric Components

**Task:**

* **Sort strings**: Write a function `sort_strings_with_components(strings: List[str])` that sorts a list of strings based on their alphabetical and numerical components:
    * Sort the list by the alphabetical component (letters) in ascending order.
    * Then, sort by the numerical component in descending order.
    * Assume each string follows the format `<letters><number>`.


## 5. HTTP Request Parsing

**Task:**

* **Parse HTTP Request**: Implement a function `parse_http_request(request: str)` that parses an HTTP request string with two parameters.
    * Extract the values of `param1` and `param2` from the input request string.
    * Return the extracted values as a dictionary with keys `"param1"` and `"param2"`.
    * Handle cases where the parameters are missing or the string is malformed (i.e., missing `&` or `=`).



```python
flights_data = "UK:US:FedEx:4,UK:FR:Jet1:2,US:UK:RyanAir:8,CA:UK:CanadaAir:8"
print(f"Cost UK to US: {direct_flight_cost(flights_data, 'UK', 'US')}")     # Expected: 4
print(f"Cost US to FR: {direct_flight_cost(flights_data, 'US', 'FR')}")     # Expected: None
print(f"Cost CA to UK: {direct_flight_cost(flights_data, 'CA', 'UK')}")     # Expected: 8
print(f"Cost UK to UK: {direct_flight_cost(flights_data, 'UK', 'UK')}")     # Expected: None
print(f"Cost NonExistent to US: {direct_flight_cost(flights_data, 'NonExistent', 'US')}") # Expected: None
```

```python
flights_data = "UK:US:FedEx:4,UK:FR:Jet1:2,FR:DE:EasyFly:3,DE:US:Luft:5,CA:UK:CanadaAir:8"
print(f"Cheapest CA to US: {cheapest_flight_route(flights_data, 'CA', 'US')}")   # Expected (example): ['CA', 'UK', 'US'] (cost 12)
print(f"Cheapest UK to DE: {cheapest_flight_route(flights_data, 'UK', 'DE')}")   # Expected (example): ['UK', 'FR', 'DE'] (cost 5)
print(f"Cheapest US to CA: {cheapest_flight_route(flights_data, 'US', 'CA')}")   # Expected: None (no route back)
print(f"Cheapest UK to UK: {cheapest_flight_route(flights_data, 'UK', 'UK')}")   # Expected: ['UK'] (cost 0, direct route of length 1)
print(f"Cheapest FR to US: {cheapest_flight_route(flights_data, 'FR', 'US')}")   # Expected (example): ['FR', 'DE', 'US'] (cost 8)
print(f"Cheapest CA to NonExistent: {cheapest_flight_route(flights_data, 'CA', 'NonExistent')}") # Expected: None
```

```python
print(f"Compress 2: {compress_url('stripe.com/payments/checkout/customer.john.doe', 2)}")       # Expected: stripe.c3m/payments/checkout/customer.j2n.d1e
print(f"Compress 1: {compress_url('stripe.com/payments/checkout/customer.john.doe', 1)}")       # Expected: s4m/p7s/c6t/c7r.j3n.d2e
print(f"Compress 0: {compress_url('stripe.com/payments/checkout/customer.john.doe', 0)}")       # Expected: s5m/p8s/c8t/c8r.j4n.d3e
print(f"Compress 3: {compress_url('example.longdomainname/path/item.verylongitemname', 3)}") # Expected: exa...ame/pat/ite.ver...ame
print(f"Compress 10: {compress_url('short.part/another.short', 10)}")                     # Expected: short.part/another.short (no compression)
print(f"Compress 2: {compress_url('singlepart', 2)}")                                    # Expected: s6t
print(f"Compress 2: {compress_url('part.with.empty..segment', 2)}")                     # Expected: p2t.w2h.e0y.s4t
```

```python
stop_words_list = ["is", "a", "to", "the", "and"]
print(f"Remove 1: {stopwords_stripped('This is a test sentence to remove stop words', stop_words_list)}") # Expected: this  test sentence  remove stop words
print(f"Remove 2: {stopwords_stripped('The quick brown fox jumps over the lazy dog', stop_words_list)}") # Expected:  quick brown fox jumps over  lazy dog
print(f"Remove 3: {stopwords_stripped('No stop words here', stop_words_list)}")                     # Expected: no stop words here
print(f"Remove 4: {stopwords_stripped('IS A TO THE AND', stop_words_list)}")                     # Expected: None
print(f"Remove 5: {stopwords_stripped('Mixed Case Is A Test', stop_words_list)}")                 # Expected: mixed case  test
print(f"Remove 6: {stopwords_stripped('', stop_words_list)}")                                     # Expected: None
```

```python
strings_list1 = ["a1", "b32", "caba522", "b21"]
print(f"Sort 1: {sort_strings_with_components(strings_list1)}")       # Expected: ['a1', 'b32', 'b21', 'caba522']
strings_list2 = ["z9", "a10", "a2", "b5", "a1"]
print(f"Sort 2: {sort_strings_with_components(strings_list2)}")       # Expected: ['a10', 'a2', 'a1', 'b5', 'z9']
strings_list3 = ["x1", "x10", "y5", "y1"]
print(f"Sort 3: {sort_strings_with_components(strings_list3)}")       # Expected: ['x10', 'x1', 'y5', 'y1']
strings_list4 = ["abc10", "ab10", "abc20", "ab5"]
print(f"Sort 4: {sort_strings_with_components(strings_list4)}")       # Expected: ['ab10', 'ab5', 'abc20', 'abc10']
strings_list5 = []
print(f"Sort 5: {sort_strings_with_components(strings_list5)}")       # Expected: []
```

```python
print(f"Parse 1: {parse_http_request('param1=123&param2=abc')}")       # Expected: {'param1': '123', 'param2': 'abc'}
print(f"Parse 2: {parse_http_request('param1=hello&param2=world')}")   # Expected: {'param1': 'hello', 'param2': 'world'}
print(f"Parse 3: {parse_http_request('param1=one&param2=two=extra')}") # Expected: {'param1': 'one', 'param2': 'two=extra'}
print(f"Parse 4: {parse_http_request('param1=&param2=')}")              # Expected: {'param1': '', 'param2': ''}
print(f"Parse 5: {parse_http_request('param1=value1')}")               # Expected: {'param1': 'value1', 'param2': None}
print(f"Parse 6: {parse_http_request('param2=value2')}")               # Expected: {'param1': None, 'param2': 'value2'}
print(f"Parse 7: {parse_http_request('=value1&param2=value2')}")       # Expected: {'param1': None, 'param2': 'value2'}
print(f"Parse 8: {parse_http_request('param1=value1&')}")              # Expected: {'param1': 'value1', 'param2': None}
print(f"Parse 9: {parse_http_request('param1value1param2value2')}")     # Expected: {'param1': 'value1param2value2', 'param2': None} (handling missing '=')
print(f"Parse 10: {parse_http_request('')}")                             # Expected: {'param1': None, 'param2': None}
print(f"Parse 11: {parse_http_request('param1=')}")                            # Expected: {'param1': '', 'param2': None}
print(f"Parse 12: {parse_http_request('&param2=value2')}")                   # Expected: {'param1': None, 'param2': 'value2'}
```

