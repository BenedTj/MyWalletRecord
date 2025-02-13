from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    TransactionType = [('Expense', 'Expense'), ('Income', 'Income')]
    transaction_type = models.CharField(max_length=10, default='Expense', blank=False, null=False,
                              choices=TransactionType)
    CurrencyType = [('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('JPY', 'JPY'), ('CNY', 'CNY'), ('SGD', 'SGD'), ('MYR', 'MYR'), ('IDR', 'IDR')]
    currency = models.CharField(max_length=3, default='SGD', blank=False, null=False, choices=CurrencyType)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False, default=0)
    date = models.DateField(default=timezone.now, blank=False, null=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    ExpenseCategory = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Other', 'Other')
    ]
    IncomeCategory = [
        ('Salary', 'Salary'),
        ('Bonus', 'Bonus'),
        ('Allowance', 'Allowance'),
        ('Other', 'Other')
    ]
    category = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.title