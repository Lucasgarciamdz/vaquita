from rich.console import Console
from rich.prompt import Prompt
from rich import print
from textual.app import App
from textual.widgets import Placeholder
from vaquita.statistics import StatisticsSvc
import plotext as plt

class StatisticsApp(App):
    async def on_mount(self):
        await self.view.dock(Placeholder(), edge="left", size=30)

    async def on_start(self):
        console = Console()
        statistics_service = StatisticsSvc()  # Aquí deberías pasar tu repositorio de estadísticas

        while True:
            command = Prompt.choices("Choose a command", choices=["pie_chart", "line_graph", "quit"])
            if command == 'quit':
                break
            else:
                if command == 'pie_chart':
                    data = statistics_service.get_pie_chart_data()
                    plt.pie(data)
                    plt.show()
                elif command == 'line_graph':
                    data = statistics_service.get_line_graph_data()
                    plt.plot(data)
                    plt.show()

StatisticsApp.run()