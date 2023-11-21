from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp # Display Pixels.
import matplotlib.pyplot as plt

thing = App.get_running_app()

plt.style.use('fivethirtyeight')

fig = plt.figure()
fig.patch.set_facecolor('#012148d9')

### On this one we update the graphic transforming the matplot plot an image because Kivy_garden.matplotlib doesn't support pie charts.
### If for whatever reason you want the Data Table to adapt to different sizes of screen on update the just add the same 'self.dpAssign = Window.size[0]/22' on the Update().

class Portfolio(Screen):
    changes = False # Boolean that tells us if the portfolio needs to run the Update function, changing to True if the user bought/sold stock.
    haveStocks = False # To check if it needs to plot a pie chart or not.
    dpAssign = 0 # Will hold the size needed to make the table fit whatever screen is being displayed in.
    table = None

    def __init__(self, **kw):
        """
        When innitiated it checks for stocks, if there are then it plots a new graph and makes a Datatable with the Data we have.
        If no stocks have been purchased then it display a stock photo of a graph with no Data.
        """
        super().__init__(**kw)
        thing.currentScreens['portfolio'] = True

        self.CheckStocks()
        
        if self.haveStocks == True:
            self.PlotPie()
            self.ids.graph.source = "images/piechart.png"

        self.dpAssign = Window.size[0]/22

        self.table = MDDataTable(
                        size_hint=(1, 1),
                        pos_hint= {'center_x': 0.5, 'center_y': 0.5},
                        rows_num= 6,
                        background_color_header= (0/255,128/255,0/255,1),
                        background_color_cell= (1/255,33/255,72/255,1),
                        background_color_selected_cell= (1/255,33/255,72/255,1),
                        column_data= [
                            ("[color=#D4D4D9]Stock[/color]", dp(self.dpAssign)),
                            ("[color=#D4D4D9]Amount[/color]", dp(self.dpAssign)),
                            ("[color=#D4D4D9]Total Payed[/color]", dp(self.dpAssign)),
                            ("[color=#D4D4D9]Total Value[/color]", dp(self.dpAssign))
                        ],
                        row_data= [
                            ("[color=#D4D4D9]AAPL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AAPL"] * thing.currentStockPrice["AAPL"], 2)}[/color]'),
                            ("[color=#D4D4D9]TSLA[/color]",f'[color=#D4D4D9]{thing.ownedStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["TSLA"] * thing.currentStockPrice["TSLA"], 2)}[/color]'),
                            ("[color=#D4D4D9]GOOGL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["GOOGL"] * thing.currentStockPrice["GOOGL"], 2)}[/color]'),
                            ("[color=#D4D4D9]AMZN[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AMZN"] * thing.currentStockPrice["AMZN"], 2)}[/color]'),
                            ("[color=#D4D4D9]^GSPC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^GSPC"] * thing.currentStockPrice["^GSPC"], 2)}[/color]'),
                            ("[color=#D4D4D9]^IXIC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^IXIC"] * thing.currentStockPrice["^IXIC"], 2)}[/color]')
                        ] 
                    )
        self.ids.table.add_widget(self.table)
    
    def CheckStocks(self):
        """
        Checks if the user has stocks and sets the value of self.haveStock accordingly.
        """
        for key in thing.ownedStocks:
            if thing.ownedStocks[key] > 0:
                self.haveStocks = True
                return
        self.haveStocks = False
        return     

    def Update(self):
        """
        When called the pie chart and the values of the stocks in the grid are updated IF self.changes is True.
        This function is called each time the portfolio screen is selected.
        """
        self.CheckStocks() # Checks if the user has stocks remaining.
        
        if self.haveStocks == False: # In case he doesn't then it changes the graph image to the base one.
            self.ids.graph.source = "images/piechartbase.png"
            self.ids.table.remove_widget(self.ids.table.children[0])
            self.table = MDDataTable(
                            size_hint=(1, 1),
                            pos_hint= {'center_x': 0.5, 'center_y': 0.5},
                            rows_num= 6,
                            background_color_header= (0/255,128/255,0/255,1),
                            background_color_cell= (1/255,33/255,72/255,1),
                            background_color_selected_cell= (1/255,33/255,72/255,1),
                            column_data= [
                                ("[color=#D4D4D9]Stock[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Amount[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Total Payed[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Total Value[/color]", dp(self.dpAssign))
                            ],
                            row_data= [
                                ("[color=#D4D4D9]AAPL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AAPL"] * thing.currentStockPrice["AAPL"], 2)}[/color]'),
                                ("[color=#D4D4D9]TSLA[/color]",f'[color=#D4D4D9]{thing.ownedStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["TSLA"] * thing.currentStockPrice["TSLA"], 2)}[/color]'),
                                ("[color=#D4D4D9]GOOGL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["GOOGL"] * thing.currentStockPrice["GOOGL"], 2)}[/color]'),
                                ("[color=#D4D4D9]AMZN[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AMZN"] * thing.currentStockPrice["AMZN"], 2)}[/color]'),
                                ("[color=#D4D4D9]^GSPC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^GSPC"] * thing.currentStockPrice["^GSPC"], 2)}[/color]'),
                                ("[color=#D4D4D9]^IXIC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^IXIC"] * thing.currentStockPrice["^IXIC"], 2)}[/color]')
                            ] 
                        )
            self.ids.table.add_widget(self.table)
            self.changes = False
            return
        
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
                            background_color_header= (0/255,128/255,0/255,1),
                            background_color_cell= (1/255,33/255,72/255,1),
                            background_color_selected_cell= (1/255,33/255,72/255,1),
                            column_data= [
                                ("[color=#D4D4D9]Stock[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Amount[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Total Payed[/color]", dp(self.dpAssign)),
                                ("[color=#D4D4D9]Total Value[/color]", dp(self.dpAssign))
                            ],
                            row_data= [
                                ("[color=#D4D4D9]AAPL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AAPL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AAPL"] * thing.currentStockPrice["AAPL"], 2)}[/color]'),
                                ("[color=#D4D4D9]TSLA[/color]",f'[color=#D4D4D9]{thing.ownedStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["TSLA"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["TSLA"] * thing.currentStockPrice["TSLA"], 2)}[/color]'),
                                ("[color=#D4D4D9]GOOGL[/color]",f'[color=#D4D4D9]{thing.ownedStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["GOOGL"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["GOOGL"] * thing.currentStockPrice["GOOGL"], 2)}[/color]'),
                                ("[color=#D4D4D9]AMZN[/color]",f'[color=#D4D4D9]{thing.ownedStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["AMZN"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["AMZN"] * thing.currentStockPrice["AMZN"], 2)}[/color]'),
                                ("[color=#D4D4D9]^GSPC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^GSPC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^GSPC"] * thing.currentStockPrice["^GSPC"], 2)}[/color]'),
                                ("[color=#D4D4D9]^IXIC[/color]",f'[color=#D4D4D9]{thing.ownedStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{thing.spentOnStocks["^IXIC"]}[/color]',f'[color=#D4D4D9]{round(thing.ownedStocks["^IXIC"] * thing.currentStockPrice["^IXIC"], 2)}[/color]')
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
        plt.title(f"Total value: {round(sum(slices), 2)}", color='white')
        plt.legend(loc="center", labels=labs)
        plt.tight_layout

        # Donut style:
        circle = plt.Circle(xy=(0,0), radius=0.75, facecolor= '#012148d9', alpha=1)
        plt.gca().add_artist(circle)

        plt.savefig("images/piechart.png", facecolor='#012148d9') # Saves the image so it can be used as a graph.

        return

    def GraphToggler(self):
        """
        Lazy way to deal with the GraphToggler from other screens.
        """
        return