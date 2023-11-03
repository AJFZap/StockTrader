from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp # Display Pixels.
import matplotlib.pyplot as plt

thing = App.get_running_app()

# plt.style.use('seaborn-v0_8-darkgrid')
plt.style.use('fivethirtyeight')

### On this one we update the graphic transforming the matplot plot an image because Kivy_garden.matplotlib doesn't support pie charts.

class Portfolio(Screen):
    changes = False # Boolean that tells us if the portfolio needs to run the Update function, changing to True if the user bought/sold stock.
    haveStocks = False # To check if it needs to plot a pie chart or not.
    table = None

    def __init__(self, **kw):
        """
        When innitiated it checks for stocks, if there are then it plots a new graph and makes a Datatable with the Data we have.
        If no stocks have been purchased then it display a stock photo of a graph with no Data.
        """
        super().__init__(**kw)
        thing.currentScreens['portfolio'] = True

        for key in thing.ownedStocks:
            if thing.ownedStocks[key] > 0:
                self.haveStocks = True
        
        if self.haveStocks == True:
            self.PlotPie()
            self.ids.graph.source = "images/piechart.png"

        self.table = MDDataTable(
                        size_hint=(1, 1),
                        pos_hint= {'center_x': 0.5, 'center_y': 0.5},
                        rows_num= 6,
                        background_color_header= (76/255,174/255,81/255,1),
                        column_data= [
                            ("Stock", dp(17)),
                            ("Amount", dp(17)),
                            ("Total Payed", dp(17)),
                            ("Total Value", dp(17))
                        ],
                        row_data= [
                            ("AAPL",thing.ownedStocks["AAPL"],thing.spentOnStocks["AAPL"],round(thing.ownedStocks["AAPL"] * thing.currentStockPrice["AAPL"], 2)),
                            ("TSLA",thing.ownedStocks["TSLA"],thing.spentOnStocks["TSLA"],round(thing.ownedStocks["TSLA"] * thing.currentStockPrice["TSLA"], 2)),
                            ("GOOGL",thing.ownedStocks["GOOGL"],thing.spentOnStocks["GOOGL"],round(thing.ownedStocks["GOOGL"] * thing.currentStockPrice["GOOGL"], 2)),
                            ("AMZN",thing.ownedStocks["AMZN"],thing.spentOnStocks["AMZN"],round(thing.ownedStocks["AMZN"] * thing.currentStockPrice["AMZN"], 2)),
                            ("^GSPC",thing.ownedStocks["^GSPC"],thing.spentOnStocks["^GSPC"],round(thing.ownedStocks["^GSPC"] * thing.currentStockPrice["^GSPC"], 2)),
                            ("^IXIC",thing.ownedStocks["^IXIC"],thing.spentOnStocks["^IXIC"],round(thing.ownedStocks["^IXIC"] * thing.currentStockPrice["^IXIC"], 2))
                        ] 
                    )
        self.ids.table.add_widget(self.table)
    
    def Update(self):
        """
        When called the pie chart and the values of the stocks in the grid are updated IF self.changes is True.
        This function is called each time the portfolio screen selected.
        """
        if self.changes == True:
            self.ids.graph.source = "images/piechart.png" # To change the piechartbase image to the new location and be able to update it.
            self.PlotPie()
            self.ids.graph.reload() # Reloads changed image.

            # Lazy way to handle changes in the Data table, just remove the previous one and add the new one with the changes.
            self.ids.table.remove_widget(self.ids.table.children[0])

            self.table = MDDataTable(
                            size_hint=(1, 1),
                            pos_hint= {'center_x': 0.5, 'center_y': 0.5},
                            rows_num= 6,
                            background_color_header= (76/255,174/255,81/255,1),
                            column_data= [
                                ("Stock", dp(17)),
                                ("Amount", dp(17)),
                                ("Total Payed", dp(17)),
                                ("Total Value", dp(17))
                            ],
                            row_data= [
                                ("AAPL",thing.ownedStocks["AAPL"],thing.spentOnStocks["AAPL"],round(thing.ownedStocks["AAPL"] * thing.currentStockPrice["AAPL"], 2)),
                                ("TSLA",thing.ownedStocks["TSLA"],thing.spentOnStocks["TSLA"],round(thing.ownedStocks["TSLA"] * thing.currentStockPrice["TSLA"], 2)),
                                ("GOOGL",thing.ownedStocks["GOOGL"],thing.spentOnStocks["GOOGL"],round(thing.ownedStocks["GOOGL"] * thing.currentStockPrice["GOOGL"], 2)),
                                ("AMZN",thing.ownedStocks["AMZN"],thing.spentOnStocks["AMZN"],round(thing.ownedStocks["AMZN"] * thing.currentStockPrice["AMZN"], 2)),
                                ("^GSPC",thing.ownedStocks["^GSPC"],thing.spentOnStocks["^GSPC"],round(thing.ownedStocks["^GSPC"] * thing.currentStockPrice["^GSPC"], 2)),
                                ("^IXIC",thing.ownedStocks["^IXIC"],thing.spentOnStocks["^IXIC"],round(thing.ownedStocks["^IXIC"] * thing.currentStockPrice["^IXIC"], 2))
                            ] 
                        )
            
            self.ids.table.add_widget(self.table)
            self.changes = False

        return
    
    def PlotPie(self):
        """
        It will plot the pie chart each time it is called.
        """
        slices = []
        labs = []
        
        for key in thing.ownedStocks:
            if thing.ownedStocks[key] > 0:
                labs.append(f"{key}: {round(thing.ownedStocks[key] * thing.currentStockPrice[key], 2)}")
                slices.append(thing.ownedStocks[key] * thing.currentStockPrice[key])
        
        plt.cla()
        plt.pie(slices, labels=None, wedgeprops={'edgecolor': 'black'}, startangle=90)
        plt.axis('equal')
        plt.title(f"Total value: {round(sum(slices), 2)}")
        plt.legend(loc="center", labels=labs)
        plt.tight_layout

        # Donut style:
        circle = plt.Circle(xy=(0,0), radius=0.75, facecolor= 'white')
        plt.gca().add_artist(circle)

        plt.savefig("images/piechart.png") # Saves the image so it can be used as a graph.

        return

    def GraphToggler(self):
        """
        Lazy way to deal with the GraphToggler from other screens.
        """
        return