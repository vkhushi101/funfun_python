from collections import defaultdict
from typing import Dict, Optional
import csv, json
from report_model import Account, Metadata, Payment, Status, Transaction, Type

class BillingSystem():
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.metadata: Metadata = Metadata()
        self.outgoing_spenders: Dict[str, float] = defaultdict(float)
    
    
    def _get_account_details(self, account_id: str) -> Optional[Account]:
        account = self.accounts.get(account_id)
        if not account: 
            print(f"Account {account_id} does not exist in our system")
            raise RuntimeError(f"Account {account_id} not found")
        return account
        
    
    def add_account(self, account_id: str, initial_balance: str):
        print(f"Creating account {account_id} with initial balance {initial_balance}")
        
        if not self.accounts.get(account_id): 
            self.accounts[account_id] = Account(account_id=account_id, final_balance=float(initial_balance))
        

    def record_transaction(self, timestamp: int, account_id: str, amount: float):
        print(f"Recording transaction for {account_id} with amount {amount} at {timestamp}")
        
        self.process_scheduled_payment(timestamp, account_id)
        if amount == 0: print(f"No valid amount to deposit or withdraw for account {account_id}")
            
        txn_type = Type.WITHDRAW if amount < 0 else Type.DEPOSIT
        
        try:
            cur_account = self._get_account_details(account_id)
            
            if txn_type == Type.WITHDRAW:
                if cur_account.final_balance < abs(amount):
                    self.metadata.total_failed_withdrawals += 1
                    print(f"Insufficient funds to withdraw {amount} from account {account_id} at {timestamp}")
                    return
                self.outgoing_spenders[account_id] -= amount
            
            cur_account.final_balance += amount
            transaction = Transaction(type=txn_type.value, amount=amount, timestamp=timestamp)
            cur_account.transactions.append(transaction)
            
            self.metadata.timestamp_last_processed = timestamp
            print(f"Transaction recorded for account {account_id} with amount {amount} at time {timestamp}")
        except RuntimeError as e:
            self.metadata.total_failed_withdrawals += 1
            print(f"Failure when recording transaction at {timestamp} for account {account_id} with amount {amount}, {e}")
    

    def schedule_payment(self, timestamp: int, account_id: str, amount: float, delay: int):
        print(f"Attempting scheduling transaction for {account_id} with amount {amount} at time {timestamp + delay}")
        
        self.process_scheduled_payment(timestamp, account_id)
        try:
            cur_account = self._get_account_details(account_id)

            payment_count = max(cur_account.payments.keys(), default=0) + 1
            new_payment_id = f"payment{payment_count}"
            new_payment = Payment(id=new_payment_id, status=Status.PENDING, scheduled_at=timestamp+delay, amount=amount)
            cur_account.payments[payment_count] = new_payment
            print(f"Scheduled transaction for {account_id} with amount {amount} at time {timestamp + delay} with id {new_payment_id}")
        except RuntimeError as e:
            print(f"Failure when scheduling payment at {timestamp+delay} for account {account_id} with amount {amount}, {e}")
        
        
    def cancel_payment(self, timestamp: int, account_id: str, payment_id: str):
        print(f"Attempting cancelling transaction for {account_id} with payment id {payment_id} for timestamp {timestamp}")
       
        try:
            cur_account = self._get_account_details(account_id)
            
            id_num = int(payment_id.strip("payment"))
            payment = cur_account.payments.get(id_num)
            if not payment:
                print(f"No scheduled payment found for account {account_id} with payment id {payment_id}")
                return
            
            self.process_scheduled_payment(timestamp, account_id)
            if payment.status != Status.PENDING:
                print(f"Payment {payment_id} for account {account_id} is in {payment.status} state, unable to cancel payment")
                return
            
            if payment.scheduled_at == timestamp:
                print(f"Cannot cancel payment {payment_id} for account {account_id}, as it has just been executed at time {timestamp}")
                return
            
            del cur_account.payments[id_num]
            self.metadata.timestamp_last_processed = timestamp
            print(f"Cancelled payment for account {account_id} with payment id {payment_id} at time {timestamp}")
        except RuntimeError as e:
            print(f"Failure when cancelling payment at {timestamp} for account {account_id}, {e}")


    def process_scheduled_payment(self, timestamp: int, account_id: str):
        print(f"Processing transaction for account {account_id} at timestamp {timestamp}")
        
        try:
            account_details = self._get_account_details(account_id)
            cur_funds = account_details.final_balance
            for payment_details in account_details.payments.values():
                pending_payment_value = payment_details.amount
                if payment_details.status != Status.PENDING:
                    continue
                if payment_details.scheduled_at > timestamp:
                    continue
                if pending_payment_value > cur_funds:
                    payment_details.status = Status.SKIPPED
                    continue
                payment_details.executed_at = timestamp
                payment_details.status = Status.EXECUTED
                
                self.metadata.total_payments_executed += 1
                self.metadata.timestamp_last_processed = timestamp

                account_details.final_balance -= pending_payment_value
                self.outgoing_spenders[account_id] += pending_payment_value
            print(f"Executed payments for account {account_id} at time {timestamp}")
        except RuntimeError as e:
            self.metadata.total_payments_failed += 1
            print(f"Failure processing scheduled transactions for account {account_id}, {e}")
        

    def get_top_spenders(self, timestamp: int, k: int):
        print(f"Getting top {k} spending accounts")
        
        self.process_scheduled_payment(timestamp, account_id)
        result = sorted(self.outgoing_spenders.items(), key=lambda x: (-x[1], x[0]))[:k]
        return result
    
    
    def get_account_summary(self, timestamp: int, account_id: str):
        print(f"Getting account {account_id} summary")
        
        self.process_scheduled_payment(timestamp, account_id)
        try:
            account = self._get_account_details(account_id).to_dict()
            
            result = {}
            result["id"] = account_id
            result["balance"] = account["final_balance"]
            result["outgoing"] = self.outgoing_spenders.get(account_id, 0)
            
            if account["transactions"]:
                transactions_by_type = defaultdict(list)
                for transaction in account["transactions"]:
                    type = transaction.pop("type")
                    transactions_by_type[type].append(transaction)
                result["transactions"] = transactions_by_type
            
            if account["payments"]:
                payments_by_type = defaultdict(list)
                for payment in account["payments"].values():
                    status = payment.pop("status")
                    payments_by_type[status].append(payment)
                result["payment_status"] = payments_by_type 
                
            return result
        except RuntimeError as e:
            print(f"Failure getting the account summary for account {account_id} at timestamp {timestamp}")


    def get_structured_report(self, timestamp: int):
        print(f"Printing structured report at timestamp {timestamp}")
        
        self.process_scheduled_payment(timestamp, account_id)
        result = {}
        result["accounts"] = [self.get_account_summary(timestamp, i) for i in self.accounts.keys()]
        result["top_spenders"] = self.get_top_spenders(timestamp, 2)
        result["meta"] = self.metadata.to_dict()
        return result
    
    
if __name__ == "__main__":
    accounts = {}
    field_names = ["account_id", "initial_balance"]
    with open('accounts.csv', 'r') as accounts_file:
        for i in csv.DictReader(accounts_file):
            accounts[i["account_id"]] = i
        
    billingSystem = BillingSystem()
    with open('events.json', 'r') as events_file:
        for event in json.load(events_file):
            event_type = event.pop("operation")
            timestamp = int(event["timestamp"])
            result = None
            
            match (event_type):
                case "create_account":
                    account_id = event["account_id"]
                    billingSystem.add_account(**accounts[account_id])
                
                case "deposit":
                    account_id = event["account_id"]
                    amount = event["amount"] 
                    billingSystem.record_transaction(timestamp, account_id, float(amount))
                
                case "withdraw":
                    account_id = event["account_id"]
                    amount = -event["amount"] 
                    billingSystem.record_transaction(timestamp, account_id, float(amount))      
                
                case "schedule_payment":
                    account_id = event["account_id"]
                    amount = event["amount"]
                    delay = event["delay"]
                    billingSystem.schedule_payment(timestamp, account_id, float(amount), int(delay))
                
                case "cancel_payment":
                    account_id = event["account_id"]
                    payment_id = event["payment_id"]
                    billingSystem.cancel_payment(timestamp, account_id, payment_id)
                
                case "get_top_spenders":
                    k = event["k"]
                    result = billingSystem.get_top_spenders(timestamp, k)
                
                case "get_account_summary":
                    account_id = event["account_id"]
                    result = billingSystem.get_account_summary(timestamp, account_id)
                
                case "generate_report":
                    result = billingSystem.get_structured_report(timestamp)
            
            if result: print(json.dumps(result, indent=1))
            print()