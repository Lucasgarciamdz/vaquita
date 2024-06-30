import plotext as plt
from rich.console import Console
from rich.prompt import Prompt
from textual.app import App
from textual.widgets import Placeholder

from vaquita.statistics import StatisticsSvc


class StatisticsApp(App):
    async def on_mount(self):
        await self.view.dock(Placeholder(), edge="left", size=30)

    async def on_start(self):
        console = Console()
        statistics_service = StatisticsSvc()  # Aquí deberías pasar tu repositorio de estadísticas

        while True:
            command = Prompt.choices
            if command == 'quit':
                break
            else:
                if command == 'pie_chart':
                    categories = [
                        "total_food",
                        "total_rent",
                        "total_services",
                        "total_transportation",
                        "total_utilities",
                        "total_health",
                        "total_insurance",
                        "total_personal",
                        "total_entertainment",
                        "total_education",
                        "total_savings",
                        "total_salary"
                    ]
                    data = [statistics_service.get_metric_data(category) for category in categories]
                    plt.pie(data, labels=categories)
                    plt.show()
                elif command == 'line_graph':
                    data = statistics_service.get_line_graph_data()
                    plt.plot(data)
                    plt.show()


StatisticsApp.run()
