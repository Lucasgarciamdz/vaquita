class StatisticsSvc:
    def __init__(self, statistics_repo):
        self.statistics_repo = statistics_repo

    def calculate_totals(self):
        stats = self.statistics_repo.get_all()
        totals = {
            'total_income': sum(stat.total_income for stat in stats),
            'total_expense': sum(stat.total_expense for stat in stats),
            # Add more totals as needed
        }
        return totals

    def calculate_averages(self):
        stats = self.statistics_repo.get_all()
        averages = {
            'average_transaction_value': sum(stat.average_transaction_value for stat in stats) / len(stats),
            'monthly_expense_average': sum(stat.monthly_expense_average for stat in stats) / len(stats),
            # Add more averages as needed
        }
        return averages

    def calculate_largest(self):
        stats = self.statistics_repo.get_all()
        largest = {
            'largest_expense': max(stat.largest_expense for stat in stats),
            'largest_income': max(stat.largest_income for stat in stats),
            # Add more largest values as needed
        }
        return largest

    def calculate_category_percentages(self):
        stats = self.statistics_repo.get_all()
        category_percentages = {
            'expense_category_percentage': self._calculate_percentage_for_each_category(stats, 'expense'),
            'income_category_percentage': self._calculate_percentage_for_each_category(stats, 'income'),
            # Add more category percentages as needed
        }
        return category_percentages

    def _calculate_percentage_for_each_category(self, stats, category):
        total = sum(getattr(stat, f'total_{category}') for stat in stats)
        percentages = {f'total_{category}': getattr(stat, f'total_{category}') / total * 100 for stat in stats}
        return percentages
