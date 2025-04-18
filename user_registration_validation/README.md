# User Registration Validation

## Prompt:
Transform JSON dataset into a clean CSV after validating & manipulating the data

### Definitions:
##### User
```
- id
- name
- email
- age
- address
```

##### Address
```
- street
- city
- state
- zipcode
```

##### Registration Info
```
- registration date
```


### Acceptance Criteria
- Use Pydantic to define data models for User, Address, RegistrationInfo
- If age missing/ invalid, set to 0
- If email missing/ invalid, market the user as email_invalid = True and set email to None. Log the invalid email for future review
- If address missing, populate with None
- If registration date missing or invalid, set to default "1900-01-01"
- If zipcode invalid, set to "00000" default and log invalid zipcode

- Transform registration date to YYYY-MM-DD (datetime lib)
- Add a field "is_adult" which is True if age is > 18
- Add a field "full_address" that's user friendly (123 Main St, Springfield, IL, 62701)

- Handle validation, missing/ invalid field, formatting errors 
- Capture all invalid data
- Create CSV with columns:
*ID, Name, Email, Age, Registration Date, Full Address, Email Invalid, Is Adult*
