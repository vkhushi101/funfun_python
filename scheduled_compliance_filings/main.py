
from datetime import datetime
from enum import Enum
from typing import Dict, List
import json
from dateutil.relativedelta import relativedelta


class Cadence(Enum):
    QUARTERLY=3
    SEMIANNUAL=6
    ANNUAL=12
    
    @classmethod
    def get_cadence(cls, cadence):
        return cls.__getitem__(cadence).value

class ComplianceManager():
    def __init__(self):
        pass
    
    def get_filing_dates(self, start_date: datetime, cur_date: datetime, monthly_cadence: int) -> List[str]:
        while start_date <= cur_date:
            start_date += relativedelta(months=monthly_cadence) 
        return str(start_date.date())
        
    def calculate_next_filing_dates(self, businesses: List[Dict[str, str]], todays_date: str) -> Dict[str, datetime]:
        filing_schedule = {}
        todays_date = datetime.strptime(todays_date, "%Y-%m-%d")
        
        for business in businesses:
            id = business["business_id"]
            start_date = datetime.strptime(business["incorporation_date"], "%Y-%m-%d")
            cadence = business["filing_cadence"]
            
            delta = Cadence.get_cadence(cadence)
            filing_schedule[id] = self.get_filing_dates(start_date, todays_date, delta)
         
        return filing_schedule


if __name__ == "__main__":
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
        },
        {
            "business_id": "lmn789",
            "incorporation_date": "2024-08-20",
            "filing_cadence": "SEMIANNUAL",
            "state": "NY"
        },
        {
            "business_id": "ghi321",
            "incorporation_date": "2023-04-20",
            "filing_cadence": "ANNUAL",
            "state": "WA"
        },
        {
            "business_id": "uvw987",
            "incorporation_date": "2020-01-31",
            "filing_cadence": "QUARTERLY",
            "state": "FL"
        },
        {
            "business_id": "rst654",
            "incorporation_date": "2021-12-15",
            "filing_cadence": "SEMIANNUAL",
            "state": "IL"
        },
        {
            "business_id": "nop000",
            "incorporation_date": "2025-04-20",
            "filing_cadence": "ANNUAL",
            "state": "OR"
        },
        {
            "business_id": "hello0",
            "incorporation_date": "2024-11-30",
            "filing_cadence": "QUARTERLY",
            "state": "OR"
        }
    ]

    today = "2025-01-20"
    
    complianceManager = ComplianceManager()
    filing_schedule = complianceManager.calculate_next_filing_dates(businesses, today)
    print(json.dumps(filing_schedule, indent=1))