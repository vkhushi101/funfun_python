from collections import defaultdict
from enum import Enum
import json
from typing import Dict, List, Optional, Tuple


class Type(Enum):
    DEPOSIT='deposit'
    WITHDRAW='withdraw'
    SCHEDULE="schedule_payment"
    CANCEL="cancel_payment"
    
    
class Transaction:
    def __init__(self, type=None, amount=0, timestamp=None, payment_id=None, scheduled_at=None, executed_at=None, status=None):
        self.type: Optional[Type] = type
        self.amount: Optional[float] = amount
        self.timestamp: Optional[int] = timestamp
    
    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }
        

class Status(Enum):
    PENDING="pending"
    EXECUTED="executed"
    SKIPPED="skipped"
    FAILED="failed"
    CANCELLED="cancelled"
    CANCEL_FAILED="cancel_failed"
    
    
class Payment:
    def __init__(self, id=None, status=None, scheduled_at=None, executed_at=None, amount=0):
        self.id: str = id
        self.status: Status = status
        self.scheduled_at: int = scheduled_at
        self.executed_at: int = executed_at
        self.amount: float = amount

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status.value if self.status else None,
            "scheduled_at": self.scheduled_at,
            "executed_at": self.executed_at,
            "amount": self.amount
        }
        

class Account:
    def __init__(self, account_id=None, final_balance=0, outgoing_total=0, transactions=None, payments=None):
        self.account_id: str = account_id
        self.final_balance: float = final_balance
        self.transactions: List[Transaction] = transactions or []
        self.payments: Dict[int, Payment] = payments or {}

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "final_balance": self.final_balance,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "payments": {k: p.to_dict() for k, p in self.payments.items()}
        }
        
        
class Metadata():
    def __init__(self, total_payments_executed=0, total_payments_failed=0, total_failed_withdrawals=0, timestamp_last_processed=None):
        self.total_payments_executed: float = total_payments_executed
        self.total_payments_failed: int = total_payments_failed
        self.total_failed_withdrawals: int = total_failed_withdrawals
        self.timestamp_last_processed: int = timestamp_last_processed
    
    def to_dict(self):
        return {
            "total_payments_executed": self.total_payments_executed,
            "total_payments_failed": self.total_payments_failed,
            "total_failed_withdrawals": self.total_failed_withdrawals,
            "timestamp_last_processed": self.timestamp_last_processed
        }
    
