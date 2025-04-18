# Device Health Checks

## Definitions:
- valid decice types: "sensor", "camera", and "thermostat"
- valid health status: "healthy": 100, "warning": 50, "critical": 0. otherwise "unknown": -1
- valid timestamp: ISO 8601
- valid metric data: numeric values for string keys

## Acceptance Criteria:
#### Validation/ Cleaning
- if invalid/ missing device type, set to unknown
- if invalid/ missing health status, set to unknown
- set timestamp to "YYYY-MM-DD" format

#### Transformation
- timestamp to UTC
- convert F degrees to C degrees
- normalize pressure values from Pa to hPa (val/100)
- normalize humidity to percentage
- set device health score
- new key "device full name" as concat of device name + device type

#### Aggregation
- new json structure for each device type with their transformed data

#### Sorting/ Filtering
- filter any -1 health scores
- sort devices by scores (desc)
- output of JSONs