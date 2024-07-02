from sqlalchemy import Column, Integer, Numeric, JSON

from backend.models.base_mdl import BaseMdl


class StatisticsMdl(BaseMdl):
    """statistics."""

    __tablename__ = "Statistics"

    id = Column(Integer, primary_key=True)
    balance = Column(Numeric)
    total_income = Column(Numeric)
    total_expense = Column(Numeric)
    total_food = Column(Numeric)
    total_rent = Column(Numeric)
    total_services = Column(Numeric)
    total_transportation = Column(Numeric)
    total_utilities = Column(Numeric)
    total_health = Column(Numeric)
    total_insurance = Column(Numeric)
    total_personal = Column(Numeric)
    total_entertainment = Column(Numeric)
    total_education = Column(Numeric)
    total_savings = Column(Numeric)
    total_salary = Column(Numeric)
    average_transaction_value = Column(Numeric)
    largest_expense = Column(Numeric)
    largest_income = Column(Numeric)
    total_transactions = Column(Integer)
    total_expenses_transactions = Column(Integer)
    total_income_transactions = Column(Integer)
    monthly_expense_average = Column(Numeric)
    monthly_income_average = Column(Numeric)
    daily_expense_average = Column(Numeric)
    daily_income_average = Column(Numeric)
    expense_category_percentage = Column(JSON)
    income_category_percentage = Column(JSON)
    transaction_frequency = Column(JSON)
    income_vs_expense = Column(Numeric)

    checking_account_id = Column(Integer)

    def __repr__(self):
        return f"CheckingAccountStats(id={self.id}, balance={self.balance}, total_income={self.total_income}, total_expense={self.total_expense}, checking_account_id={self.checking_account_id})"

    def to_dict(self, depth=1):
        if depth < 0:
            return self.id
        return {
            "id": self.id,
            "balance": float(self.balance),
            "total_income": float(self.total_income),
            "total_expense": float(self.total_expense),
            "total_food": float(self.total_food),
            "total_rent": float(self.total_rent),
            "total_services": float(self.total_services),
            "total_transportation": float(self.total_transportation),
            "total_utilities": float(self.total_utilities),
            "total_health": float(self.total_health),
            "total_insurance": float(self.total_insurance),
            "total_personal": float(self.total_personal),
            "total_entertainment": float(self.total_entertainment),
            "total_education": float(self.total_education),
            "total_savings": float(self.total_savings),
            "total_salary": float(self.total_salary),
            "average_transaction_value": float(self.average_transaction_value),
            "largest_expense": float(self.largest_expense),
            "largest_income": float(self.largest_income),
            "total_transactions": self.total_transactions,
            "total_expenses_transactions": self.total_expenses_transactions,
            "total_income_transactions": self.total_income_transactions,
            "monthly_expense_average": float(self.monthly_expense_average),
            "monthly_income_average": float(self.monthly_income_average),
            "daily_expense_average": float(self.daily_expense_average),
            "daily_income_average": float(self.daily_income_average),
            "expense_category_percentage": self.expense_category_percentage,
            "income_category_percentage": self.income_category_percentage,
            "transaction_frequency": self.transaction_frequency,
            "income_vs_expense": float(self.income_vs_expense),
            "checking_account_id": self.checking_account_id,
        }
