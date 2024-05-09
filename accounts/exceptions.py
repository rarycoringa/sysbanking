from django.core.exceptions import ValidationError

class InsufficientBalance(ValidationError):
    ...

class NegativeTransaction(ValidationError):
    ...