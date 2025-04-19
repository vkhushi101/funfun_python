
from enum import Enum
import json, csv
from collections import defaultdict
import cmd


class BillingDiscrepancySystem():
    def __init__(self):
        self.customer_usage = defaultdict(list)
        self.customer_invoices = {}
        self.pricing = {}
    
    def get_customer_usages(self, file='usage.csv'):
        with open(file, 'r') as usage_file:
            for i in csv.DictReader(usage_file):
                self.customer_usage[i["customer_id"]].append(i)
    
    def get_customer_invoices(self, file='invoices.csv'):
        with open(file, 'r') as invoice_file:
            for i in csv.DictReader(invoice_file):
                self.customer_invoices[i["customer_id"]] = i
    
    def get_pricing(self, file='pricing.json'):
        with open(file, 'r') as pricing_file:
            self.pricing = json.load(pricing_file)
    
    def compute_charges(self, usage) -> float:
        service = usage["service_type"]
        price = self.pricing.get(service)
        if not price:
            print(f"No pricing recorded for service {service}")
            return None
        
        units_used = int(usage["units_used"])
        return round(float(price) * units_used, 5)
    
    def compare_expected_against_billed_charges(self, customer_id: str, billed_amount: float) -> bool:
        expected_charges = 0
        for usage in self.customer_usage[customer_id]:
            charges_for_service = self.compute_charges(usage)
            if not charges_for_service: continue
            
            print(f"Expecting {charges_for_service} charged for service {usage["service_type"]} for account {customer_id} with {usage["units_used"]} units used")
            expected_charges += charges_for_service
        
        return {"expected_amount": expected_charges, "amount_billed": billed_amount, "difference": expected_charges-billed_amount}
    
    def list_discrepancies(self):
        header = ["customer_id","date","expected_amount","amount_billed","difference"]
        with open("discrepencies.csv", 'w') as disc_file:
            disc_results = csv.DictWriter(disc_file, header)
            disc_results.writeheader()
            
            for cid, invoice in self.customer_invoices.items():
                billed_amount = round(float(invoice["amount_billed"]), 5)
                result = self.compare_expected_against_billed_charges(cid, billed_amount)
                difference_found = result["difference"]
                
                if abs(difference_found) <= 0.01:
                    print(f"No discrepencies found for customer {cid} with billed amount {billed_amount} differing by {difference_found} from expected\n")
                    continue
                
                result["date"] = invoice["date"]
                result["customer_id"] = cid
                print(f"Discrepencies found for customer {cid} with billed amount {billed_amount} differing by {difference_found} from expected\n")
                disc_results.writerow(result)
                    

class CLI(cmd.Cmd):
    prompt = 'billy > '
    intro = "Welcome to the Billing Discrepancy Detector CLI. Type 'help' for available commands."

    def __init__(self):
        super().__init__()
        self.system = BillingDiscrepancySystem()
        self.system.get_customer_usages()
        self.system.get_customer_invoices()
        self.system.get_pricing()

    def do_list(self, arg):
        self.system.list_discrepancies()

    def do_exit(self, arg):
        print("Goodbye!")
        return True
    
    
if __name__ == "__main__":
    CLI().cmdloop()