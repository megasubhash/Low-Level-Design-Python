from enum import Enum

class PaymentType(Enum):
    """Enum for payment types."""
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    CASH = "CASH"
    MOBILE_PAYMENT = "MOBILE_PAYMENT"
