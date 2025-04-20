from datetime import date, datetime, timedelta
import re
import json

class CustomerProcessing():
    def validate_credit_card_number(self, card_number):
        inv_card_number = re.sub(r"[a-zA-Z- ]", "", card_number.strip())[::-1]  
        if len(inv_card_number) < 16: return False
             
        total = 0
        for i in range(1, len(inv_card_number)+1):
            val = int(inv_card_number[i-1])
            if i % 2 == 0:
                val *= 2
            if val > 9: val -= 9
            total += val
            
        print(f"Card number {card_number} is{" " if total % 10 == 0 else " not "}valid")
        return total % 10 == 0
    
    def get_transactions(self, filename="transactions.json"):
        transactions = {}
        with open(filename, 'r') as txn_file:
            for txn in json.load(txn_file):
                transactions[int(txn.pop("id"))] = txn
        return transactions
            
    def get_currency(self, currency):
        with open("conversion_rates.json", 'r') as conv_rates:
            rates = json.load(conv_rates)
            return rates.get(currency)
        
    def get_total_revenue(self):
        revenue = 0
        for txn in self.get_transactions().values():
            amount = txn.get("amount")
            if not amount or amount <= 0: continue
            
            currency = txn.get("currency")
            if not currency: continue
            
            currency_value = self.get_currency(currency)
            if not currency_value: continue
            
            revenue += amount / currency_value
            
        print(f"Total revenue found from all transactions is {revenue}")
        return revenue
    
    def get_invoices(self, filename="customers.json"):
        customers = {}
        with open(filename, 'r') as cust_file:
            for customer in json.load(cust_file):
                customers[customer.pop("customer_id")] = customer
        return customers
    
    def invoices_to_return(self, date: datetime = datetime.today().date()):
        customers_to_invoice = []
        for cid, invoice in self.get_invoices().items():
            last_invoice = datetime.strptime(invoice["last_invoiced"], "%Y-%m-%d").date()
            
            valid = False
            if invoice["frequency"] == "monthly":
                month = last_invoice.month
                day = last_invoice.day
                year = last_invoice.year
                if last_invoice.month == 12 and year == date.year - 1: 
                    month = 0
                    year = date.year
                if year == date.year and month + 1 == date.month and day == date.day:
                    valid = True
                elif last_invoice + timedelta(days=31) == date:
                    valid = True
                    
                if valid:
                    invoice["last_invoiced"] = date
                    customers_to_invoice.append(cid)
                    
            elif invoice["frequency"] == "weekly":
                print(f"Weekly invoice details: {last_invoice}, date: {date}")
                if last_invoice + timedelta(days=7) == date:
                    customers_to_invoice.append(cid)
                    
        print(f"Customers to invoice: {", ".join(customers_to_invoice)}")
        return customers_to_invoice

if __name__ == "__main__":
    customer_processing = CustomerProcessing()
    card_numbers = ["4012 8888 8888 1881", "4539-9767-4151-2043", "4111-1111-1111-1111", "0", "4539-a790-8831-6809", "49927398716", "2222 4000 7000 0005"]
    for card_number in card_numbers:
        customer_processing.validate_credit_card_number(card_number)

    customer_processing.get_transactions()
    customer_processing.get_total_revenue()
    customer_processing.invoices_to_return(date=date(2025,1,1))
    