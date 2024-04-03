from models.base_mdl import BaseMdl
from sqlalchemy import Column, Integer, Numeric, JSON


class StatisticsMdl(BaseMdl):
    """statistics."""

    __tablename__ = 'Statistics'

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
        return f'CheckingAccountStats(id={self.id}, balance={self.balance}, total_income={self.total_income}, total_expense={self.total_expense}, checking_account_id={self.checking_account_id})'
