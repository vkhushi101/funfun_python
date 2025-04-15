import re
from fastapi.exceptions import ValidationException
from pydantic import BaseModel, constr, model_validator, PrivateAttr
from typing import Optional, TypeAlias, Dict
import csv, json

VALID_STR: TypeAlias = constr(min_length=2, max_length=36)
VALID_ADDR: TypeAlias = constr(min_length=9, max_length=380)
VALID_ZIP: TypeAlias = constr(pattern="\\d{5}")
VALID_DATE: TypeAlias = constr(pattern="\\d{4}-\\d{2}-\\d{2}")
FIELD_NAMES = ["id", "name", "email", "age", "full_address", 'is_email_invalid', "registration_date", "is_adult"]



class RegistrationInfo(BaseModel):
    
    registration_date: VALID_DATE = "1900-01-01"
    registration_age: int = 0
    is_adult: bool = False
    _is_reg_date_invalid=(bool, PrivateAttr(default=False))
    _is_reg_age_invalid=(bool, PrivateAttr(default=False))
    
    @model_validator(mode="before")
    def check_validity(cls, values):
        registration_date: str = values.get("registration_date")
        registration_age = values.get("registration_age")
        
        if registration_date:
            regex = "(\\d{4}-\\d{2}-\\d{2})"
            match_res = re.fullmatch(regex, registration_date)
            if match_res: 
                values["registration_date"] = match_res[0]
            else:
                values["registration_date"] = "1900-01-01"
                values["_is_reg_date_invalid"] = True
        else:
            values["_is_reg_date_invalid"] = True
            
        if not registration_age or not registration_age.isdigit() or not (1 <= int(registration_age) < 150):
            values["registration_age"] = 0
            values["_is_reg_age_invalid"] = True
        else:
            values["registration_age"] = int(values["registration_age"])
            values["is_adult"] = True
        return values

    
class Address(BaseModel):
    street: VALID_STR = None
    city: VALID_STR = None
    state: VALID_STR = None
    zipcode: VALID_ZIP = "00000"
    _is_valid: bool = (bool, PrivateAttr(default=True))
    
    @model_validator(mode="before")
    def check_validity(cls, values):
        street = values["street"]
        city = values["city"]
        state = values["state"]
        zipcode = values["zipcode"]
        
        if not street or not city or not state or not zipcode:
            values["_is_valid"] = False
        if zipcode:
            if not bool(re.fullmatch(r"^\d{5}$", zipcode)): 
                values["zipcode"] = '00000'
                values["_is_valid"] = False
        return values
    
    def create_full_address(self):
        if self._is_valid: 
            return f"{self.street}, {self.city}, {self.state}, {self.zipcode}"
        return None
    
    
class User(BaseModel):
    id: int
    name: VALID_STR = None
    email: VALID_STR = None
    age: int = 0
    full_address: Optional[str] = None
    registration_info: RegistrationInfo
    is_email_invalid: bool = False
    
    @model_validator(mode="before")
    def check_validity(cls, values):
        email = values["email"]
            
        if not email or '@' not in email:
            values["email"] = None
            values["is_email_invalid"] = True
        return values
    
    def get_csv_output(self):
        res = self.model_dump().copy()
        res["registration_date"] = self.registration_info.registration_date
        res["is_adult"] = self.registration_info.is_adult
        del res["registration_info"]
        return res



class DataManager():
    def __init__(self):
        self.users_with_invalid_address = []
        self.users_with_invalid_registration = []
        self.users_with_invalid_emails = []
        self.users_with_registration_fraud = []

    def _validate_and_transform(self, data):
        user_id = data["id"]
        
        try:
            full_address = Address(**data["address"]).create_full_address() if isinstance(data["address"], dict) else None
        except ValidationException as e:
            print(f"Error caught when formatting the address for user {user_id}: {e}")
            full_address = None
        if not full_address: self.users_with_invalid_address.append(user_id)
        
        try:
            reg_info = RegistrationInfo(registration_age=data["age"], registration_date=data["registration_date"]) 
        except ValidationException as e:
            print(f"Error caught when formatting the registration information for user {user_id}: {e}")
            reg_info = RegistrationInfo(_is_reg_age_invalid=True, _is_reg_date_invalid=True)
        if reg_info._is_reg_age_invalid: self.users_with_registration_fraud.append(user_id)
        if reg_info._is_reg_date_invalid: self.users_with_invalid_registration.append(user_id)
        
        data["age"] = reg_info.registration_age
        del data["address"]
        data["full_address"] = full_address
        data["registration_info"] = reg_info
        return User(**data).get_csv_output()

    def _write_to_json(self, rows):
        try:
            with open("output.csv", 'w') as output_file:
                writer = csv.DictWriter(output_file, FIELD_NAMES)
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
        except Exception as e:
            print(f"Error writing to output.csv file: {e}")
                
    def load_and_write_csv(self, filename: str):
        rows = []
        try:
            with open(filename, 'r') as csv_file:
                for row in csv.DictReader(csv_file):
                    rows.append(self._validate_and_transform(row))
            self._write_to_json(rows)
        except Exception as e:
            print(f"failure reading from json file {filename} and writing to output.csv")
    
    def load_and_write_json(self, filename: str):
        rows = []
        try:
            with open(filename, 'r') as json_file:
                for row in json.load(json_file):
                    res = self._validate_and_transform(row)
                    rows.append(res)
            self._write_to_json(rows)
        except Exception as e:
            print(f"failure reading from json file {filename} and writing to output.csv")


if __name__ == "__main__":
    data_manager = DataManager()
    data_manager.load_and_write_json("sample_jsons.json")
    