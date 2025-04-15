from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, date
from enum import Enum
import json
from collections import defaultdict
import csv

class Risk(Enum):
    HIGH="high"
    MEDIUM="medium"
    LOW="low"
    UNDETERMINED="undetermined"
    

class Report():
    def __init__(self):
        self.customer_details: Optional[List[Dict[str, str]]] = None
        self.subscription_details: Optional[Dict[str, Dict[str, str]]] = None

    def open_and_read_file(self, file_name: str) -> Optional[Dict[str, List[Dict[str, str]]]]:
        json_data = defaultdict(list)
        try:
            with open(file_name, 'r') as f:
                for entry in json.load(f):
                    cid = entry["customer_id"]
                    json_data[cid].append(entry)
            return json_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {file_name}: {e}")
            return None

    def get_customer_subscriptions(self) -> Dict[str, Dict[str, str]]:
        subscription_data = self.open_and_read_file("subscriptions.json")
        subscription_details = defaultdict(dict)

        for cid, subs in subscription_data.items():
            sorted_subs = sorted(subs, key=lambda s: datetime.strptime(s["start_date"], '%Y-%m-%d').date())
            subscription_details[cid]["subscription_start"] = sorted_subs[0]["start_date"]
            subscription_details[cid]["subscription_status"] = sorted_subs[-1]["status"]

        self.subscription_details = subscription_details
        return subscription_details

    def update_first_month_revenue(self, invoice: Dict[str, str]) -> Dict[str, str]:
        start_date_str = self.subscription_details[invoice["customer_id"]]["subscription_start"]
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        total_recurring_cost = sum(item["amount"] for item in invoice["items"]
                                   if item["type"] == "recurring" and item["amount"] is not None)

        days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
        days_sub_in_month = days_in_month - start_date.day + 1
        prorated_rev = round((total_recurring_cost / days_in_month) * days_sub_in_month, 2)

        for item in invoice["items"]:
            if item["type"] == "recurring":
                item["amount"] = prorated_rev
        return invoice

    def reduce_duplicates(self, invoices: List[Dict]) -> List[Dict]:
        unique_ids = set()
        unique_invoices = []
        for invoice in invoices:
            invoice_id = invoice["invoice_id"]
            if invoice_id not in unique_ids:
                unique_ids.add(invoice_id)
                unique_invoices.append(invoice)
        return unique_invoices

    def determine_risk_profile(self, invoice_dict: Dict[date, Dict[str, str]]) -> Risk:
        amounts = []
        for month in sorted(invoice_dict.keys())[-3:]:
            amounts.append(invoice_dict[month]["amount"])

        if None in amounts:
            return Risk.HIGH
        if min(amounts) == max(amounts):
            return Risk.MEDIUM
        if sorted(amounts) == amounts:
            return Risk.LOW
        return Risk.UNDETERMINED

    def get_customer_invoices(self) -> Dict[str, Dict[str, str]]:
        invoice_data = self.open_and_read_file("invoices.json")
        invoice_details = dict()

        for cid, invoices in invoice_data.items():
            details = dict()
            invoice_dict = {
                datetime.strptime(i["date"], '%Y-%m-%d').date(): i
                for i in self.reduce_duplicates(invoices)
            }
            if not invoice_dict:
                continue

            last_invoice = max(invoice_dict.keys())
            first_invoice = min(invoice_dict.keys())
            invoice_dict[first_invoice] = self.update_first_month_revenue(invoice_dict[first_invoice])

            all_items = {
                date: item
                for date, invoice in invoice_dict.items()
                if invoice["items"]
                for item in invoice["items"]
            }

            details["latest_invoice_date"] = last_invoice.strftime('%Y-%m-%d')
            details["invoice_count"] = len(all_items)
            details["monthly_revenue"] = sum(item["amount"] for item in all_items.values()
                                             if item["type"] == "recurring" and item["amount"] is not None)
            details["risk_rating"] = self.determine_risk_profile(all_items).value
            invoice_details[cid] = details
        return invoice_details

    def get_customer_details(self) -> List[Dict[str, str]]:
        customer_data = self.open_and_read_file("customers.json")
        subscription_data = self.get_customer_subscriptions()
        invoice_data = self.get_customer_invoices()

        all_customer_details = []
        for cid, c_details in customer_data.items():
            customer_details = dict()
            customer_details["customer_id"] = cid
            customer_details["company_name"] = c_details[0].get("company_name")

            customer_subs = subscription_data.get(cid, {})
            customer_details["subscription_start"] = customer_subs.get("subscription_start")
            customer_details["subscription_status"] = customer_subs.get("subscription_status")

            customer_invoices = invoice_data.get(cid, {})
            customer_details["monthly_revenue"] = customer_invoices.get("monthly_revenue")
            customer_details["latest_invoice_date"] = customer_invoices.get("latest_invoice_date")
            customer_details["invoice_count"] = customer_invoices.get("invoice_count")
            customer_details["risk_rating"] = customer_invoices.get("risk_rating")
            all_customer_details.append(customer_details)

        print(json.dumps(all_customer_details, indent=2))
        self.customer_details = all_customer_details
        return all_customer_details

    def parse_to_csv(self):
        field_names = [
            "customer_id", "company_name", "subscription_start",
            "subscription_status", "monthly_revenue",
            "latest_invoice_date", "invoice_count", "risk_rating"
        ]
        try:
            with open('customer_report.csv', 'w', newline='') as final_report:
                writer = csv.DictWriter(final_report, fieldnames=field_names)
                writer.writeheader()
                for customer in self.customer_details or []:
                    writer.writerow(customer)
        except IOError as e:
            print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    report = Report()
    report.get_customer_details()
    report.parse_to_csv()