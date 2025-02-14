import datetime

class MoneyCalculations:
    def __init__(self, object_list):
        self.object_list = object_list

    def calculate_expenditure_of_day(self):
        """
        Calculate the total expenditure of the day.
        """
        total_expenditure = 0
        for transaction in self.object_list.filter(date__day=datetime.date.today().day, date__month = datetime.date.today().month, date__year = datetime.date.today().year):
            if transaction.transaction_type == 'Expense':
                total_expenditure += transaction.amount
            elif transaction.transaction_type == 'Income':
                total_expenditure -= transaction.amount
        return total_expenditure
    
    def calculate_expenditure_of_month(self):
        """
        Calculate the total expenditure of the month.
        """
        total_expenditure = 0
        for transaction in self.object_list.filter(date__month=datetime.date.today().month, date__year=datetime.date.today().year):
            if transaction.transaction_type == 'Expense':
                total_expenditure += transaction.amount
            elif transaction.transaction_type == 'Income':
                total_expenditure -= transaction.amount
        return total_expenditure
    
    def calculate_expenditure_of_year(self):
        """
        Calculate the total expenditure of the year.
        """
        total_expenditure = 0
        for transaction in self.object_list.filter(date__year=datetime.date.today().year):
            if transaction.transaction_type == 'Expense':
                total_expenditure += transaction.amount
            elif transaction.transaction_type == 'Income':
                total_expenditure -= transaction.amount
        return total_expenditure