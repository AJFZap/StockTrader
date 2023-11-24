from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from random import randint
# from kivy.utils import platform
from kivymd.toast import toast
from kivy.properties import NumericProperty
from libs.uix.root import Root
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.app import App
import pandas as pd
import datetime
import json

# TODO Minor bug: Sometimes the plots in graphs are created zoomed, it has something to do with the scalable property
# wich in normal circurmstances is set to "normal", but when the widget gets smaller in size it changes to "scalable".
# TODO Minor bug: Sometimes the portfolio label background color won't load on the image for some reason so it will be hard to read until the app is restarted.

### Improvements that could work: 
# -1) New Data table column with the payed for each stock showing the median paid.
# -2) On the "Sell" show how much did you paid for that stock and maybe show the current stock price with either green or red 
#     depending if it's higher or lower than the paid amount.

# if platform == "android":
#     from android.permissions import request_permissions, Permission
#     request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

aapl = pd.read_csv('stocksDB/aapl.csv')
tsla = pd.read_csv('stocksDB/tsla.csv')
googl = pd.read_csv('stocksDB/googl.csv')
amzn = pd.read_csv('stocksDB/amzn.csv')
gspc = pd.read_csv('stocksDB/gspc.csv')
ixic = pd.read_csv('stocksDB/ixic.csv')

class StockApp(MDApp):
    randomRow = randint(0, aapl.shape[0]) # selects a random number that represents the position on the dataframe.

    openPrice = {"AAPL": round(float(aapl.iloc[randomRow]['Open']),2), "TSLA": round(float(tsla.iloc[randomRow]['Open']),2), "GOOGL": round(float(googl.iloc[randomRow]['Open']),2), "AMZN": round(float(amzn.iloc[randomRow]['Open']),2), "^GSPC": round(float(gspc.iloc[randomRow]['Open']),2), "^IXIC": round(float(ixic.iloc[randomRow]['Open']),2)}
    pastStockValuesDict = {"AAPL": openPrice["AAPL"], "TSLA": openPrice["TSLA"], "GOOGL": openPrice["GOOGL"], "AMZN": openPrice["AMZN"], "^GSPC": openPrice["^GSPC"], "^IXIC": openPrice["^IXIC"]}
    currentStockPrice = {"AAPL": openPrice["AAPL"], "TSLA": openPrice["TSLA"], "GOOGL": openPrice["GOOGL"], "AMZN": openPrice["AMZN"], "^GSPC": openPrice["^GSPC"], "^IXIC": openPrice["^IXIC"]}
    stockDiffDict = {"AAPL": "", "TSLA": "", "GOOGL": "", "AMZN": "", "^GSPC": "", "^IXIC": ""}
    ownedStocks = {"AAPL": 0, "TSLA": 0, "GOOGL": 0, "AMZN": 0, "^GSPC": 0, "^IXIC": 0}
    currentScreens = {"AAPL": False, "TSLA": False, "GOOGL": False, "AMZN": False, "^GSPC": False, "^IXIC": False, "portfolio": False}
    screenNames = {"AAPL": 'first', "TSLA": 'second', "GOOGL": 'third', "AMZN": 'fourth', "^GSPC": 'fifth', "^IXIC": 'sixth', "portfolio": 'portfolio'}
    spentOnStocks = {"AAPL": 0.00, "TSLA": 0.00, "GOOGL": 0.00, "AMZN": 0.00, "^GSPC": 0.00, "^IXIC": 0.00}
    cont = '' # Holds the name of the stock the Dialog Content will display.
    stockHistory= [] # Holds all the transactions made by the user.
    userMoney = NumericProperty(10000.00)
    
    # Content Dialogs.
    dialogBuy = None
    dialogSell = None
    dialogHistory = None

    # Storage.
    store = JsonStore('user_data.json')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "Stock App"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        # Don't change self.root to self.some_other_name
        # refer https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.root
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Green'
        self.icon = ""
        self.root = Root()
        self.root.set_current("main")

    def on_start(self):
        """
        On start it checks if there is a saved game, if there is then it loads the progress
        and switches the screen to the market.
        Then checks the rank of the user and schedules the updating of the stocks and the rank checking.
        """
        if self.store.exists('user'):
            self.LoadProgress()
            Clock.schedule_once(self.Switch, 3)

        self.CheckRank()
        Clock.schedule_interval(self.updateStocks, 2)
        Clock.schedule_interval(self.CheckRank, 5)
        # print(self.root.get_screen("main").ids)
    
    def Switch(self, *args):
        """
        Switches the screen to the Market one.
        """
        self.root.get_screen("main").ids.bottom_nav.switch_tab('screen 2')
        return
    
    def SaveProgress(self):
        """
        Saves the progress of the user by saving the amount of stocks from each company that they have and their cash on hand.
        """
        self.store.put("user", money= round(self.userMoney, 2), stocks= self.ownedStocks, spent= self.spentOnStocks, history= self.stockHistory)
        return
    
    def LoadProgress(self):
        """
        If the user has saved data then it will load it.
        """
        with open("user_data.json", 'r') as json_file:
            data = json.loads(json_file.read())

            self.userMoney = data['user']['money']
            self.ownedStocks = data['user']['stocks']
            self.spentOnStocks = data['user']['spent']
            self.stockHistory = data['user']['history']
        
        return
    
    def CheckRank(self, *args):
        """
        Checks the total value of the user portfolio and cash to provide an according title.
        """
        RankAlias = self.root.get_screen("main").ids.rank
        TotalValue = self.userMoney

        for key in self.ownedStocks:
            if self.ownedStocks[key]:
                TotalValue += (self.ownedStocks[key] * self.currentStockPrice[key])
        
        if TotalValue < 10000:
            RankAlias.text = "Deadbeat"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/deadbeat.png'
        elif TotalValue == 10000:
            RankAlias.text = "Newcomer"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/newcomer.png'
        elif TotalValue > 10000 and TotalValue < 25000:
            RankAlias.text = "Apprentice"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/apprentice.png'
        elif TotalValue >= 25000 and TotalValue < 50000:
            RankAlias.text = "Money Wise"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/moneywise.png'
        elif TotalValue >= 50000 and TotalValue < 100000:
            RankAlias.text = "Prodigy"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/prodigy.png'
        elif TotalValue >= 100000 and TotalValue < 250000:
            RankAlias.text = "Market Guru"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/marketguru.png'
        elif TotalValue >= 250000 and TotalValue < 500000:
            RankAlias.text = "Smart Investor"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/smartinvestor.png'
        elif TotalValue >= 500000 and TotalValue < 1000000:
            RankAlias.text = "Genius Investor"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/geniusinvestor.png'
        else:
            RankAlias.text = "Warren Buffett's Advisor"
            self.root.get_screen("main").ids.bottom_nav.imageSource = 'images/warrenbuffetsadvisor.png'
    
    def ToGraph(self, button):
        """
        Changes the screen to the one the button needs and checks if the screen was already created so it can start updating the graph again or not.
        """
        # Way to deal with the portfolio screen.
        if button.text == "Portfolio" and self.currentScreens['portfolio']:
            self.root.get_screen('portfolio').Update()
            self.root.set_current('portfolio')
            return
        elif button.text == "Portfolio":
            self.root.set_current('portfolio')
            return

        if self.currentScreens[button.parent.name]:
            self.root.get_screen(self.screenNames[button.parent.name]).isActive = True # To indicate the screen is active
            self.root.get_screen(self.screenNames[button.parent.name]).graphUpdating = True # To indicate the graph must be updated
            Clock.schedule_interval(self.root.get_screen(self.screenNames[button.parent.name]).UpdateGraph, 2) # To set the clock to update the graph again
            self.root.set_current(self.screenNames[button.parent.name])
        else:
            self.root.set_current(self.screenNames[button.parent.name])

    def GetPrice(self, *args):
        """
        Receives an argument 'ticker' string listed in the yahoo finance base and returns the current price for that stock.
        Example GetPrice('AAPL') will return a float value with the current price of the Apple stock.
        """
        name = args[0].parent.name

        if args[0].parent.posDF >= aapl.shape[0]:
            args[0].parent.posDF = (randint(0, aapl.shape[0]) - 1) # To ensure the we never go above the DF max amount of rows.

        match name:
            case '^GSPC':
                price = gspc.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['^GSPC'] = round(price, 2)
            case '^IXIC':
                price = ixic.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['^IXIC'] = round(price, 2)
            case 'AAPL':
                price = aapl.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['AAPL'] = round(price, 2)
            case 'TSLA':
                price = tsla.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['TSLA'] = round(price, 2)
            case 'GOOGL':
                price = googl.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['GOOGL'] = round(price, 2)
            case 'AMZN':
                price = amzn.iloc[args[0].parent.posDF]['Low']
                args[0].parent.posDF += 1
                self.currentStockPrice['AMZN'] = round(price, 2)

        return str(round(price, 2))

    def GetDifference(self, stock):
        """
        Takes two arguments ticker = string with the company ticker and price = The value at the moment of calling the function.
        Returns a string with the price difference between the past value and the current one.
        """
        pastValue = self.pastStockValuesDict[stock.parent.name]
        diff = pastValue - self.currentStockPrice[stock.parent.name]
        diffPercent = (diff / pastValue) * 100
        self.pastStockValuesDict[stock.parent.name] =  self.currentStockPrice[stock.parent.name]

        if pastValue > self.currentStockPrice[stock.parent.name]:
            return f'Diff: [b][color=be3228]-{"{:,.2f}$".format(diff)} (-{"{:,.2f}%".format(diffPercent)})[/color][/b]' # Setting colors and Bold text on the labels.
        elif pastValue < self.currentStockPrice[stock.parent.name]:
            return f'Diff: [b][color=4CAE51]+{"{:,.2f}$".format(-diff)} (+{"{:,.2f}%".format(-diffPercent)})[/color][/b]'
        else:
            return "Diff: +/- 0 (+-0)$"

    def updateStocks(self, time):
        """
        Updates the data on the stock cards on the market tab.
        """
        cards = self.root.get_screen("main")

        cards.ids.stock_price_o.text = self.GetPrice(cards.ids.stock_price_o)
        cards.ids.stock_price_t.text = self.GetPrice(cards.ids.stock_price_t)
        cards.ids.stock_price_th.text = self.GetPrice(cards.ids.stock_price_th)
        cards.ids.stock_price_fo.text = self.GetPrice(cards.ids.stock_price_fo)
        cards.ids.stock_price_fi.text = self.GetPrice(cards.ids.stock_price_fi)
        cards.ids.stock_price_six.text = self.GetPrice(cards.ids.stock_price_six)

        cards.ids.stock_diff_o.text = self.GetDifference(cards.ids.stock_price_o)
        cards.ids.stock_diff_t.text = self.GetDifference(cards.ids.stock_price_t)
        cards.ids.stock_diff_th.text = self.GetDifference(cards.ids.stock_price_th)
        cards.ids.stock_diff_fo.text = self.GetDifference(cards.ids.stock_price_fo)
        cards.ids.stock_diff_fi.text = self.GetDifference(cards.ids.stock_price_fi)
        cards.ids.stock_diff_six.text = self.GetDifference(cards.ids.stock_price_six)
    
    def BuyStock(self, stockName):
        """
        Stops the stocks and graphs from updating while the Buy Dialog is open.
        Then it opens a Buy Dialog with the BuyContent class.
        """
        self.cont = stockName # To know wich Dialog Content Stock to Open.

        Clock.unschedule(self.updateStocks) # To stay at the price of the stock when clicked.
        for key in self.currentScreens: # Stops updating the graphis of the loaded screens.
            if self.currentScreens[key] == True:
                self.root.get_screen(self.screenNames[key]).GraphToggler()

        if not self.dialogBuy:
            self.dialog = MDDialog(
                title=f"Buy Stocks - {stockName}",
                md_bg_color=(1/255,33/255,72/255,1),
                on_dismiss= self.RunClock,
                type="custom",
                content_cls=BuyContent(),
                buttons=[
                    MDFlatButton(
                        text="Buy",
                        font_name='fonts/SF-Pro-Display-Regular.ttf',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release= self.Buy,
                    ),
                    MDFlatButton(
                        text="Cancel",
                        font_name='fonts/SF-Pro-Display-Regular.ttf',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.CloseDialog,
                    ),
                ],
            )
        self.dialog.open()

    def SellStock(self, stockName):
        """
        Stops the stocks and graphs from updating while the Sell Dialog is open.
        Then it opens a Sell Dialog with the SellContent class.
        """
        self.cont = stockName # To know wich Dialog Content Stock to Open.

        Clock.unschedule(self.updateStocks) # To stay at the price of the stock when clicked.
        for key in self.currentScreens: # Stops updating the graphis of the loaded screens.
            if self.currentScreens[key] == True:
                self.root.get_screen(self.screenNames[key]).GraphToggler()

        if not self.dialogSell:
            self.dialog = MDDialog(
                title=f"Sell Stocks - {stockName}",
                md_bg_color=(1/255,33/255,72/255,1),
                on_dismiss= self.RunClock,
                type= "custom",
                content_cls=SellContent(),
                buttons=[
                    MDFlatButton(
                        text="Sell",
                        font_name='fonts/SF-Pro-Display-Regular.ttf',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.Sell,
                    ),
                    MDFlatButton(
                        text="Cancel",
                        font_name='fonts/SF-Pro-Display-Regular.ttf',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.CloseDialog,
                    ),
                ],
            )
        self.dialog.open()

    def RunClock(self, *args):
        """
        When the buy or sell dialogs is dismissed starts updating the stock values again.
        """
        Clock.schedule_interval(self.updateStocks, 2) # Start updating the stock prices again.
        for key in self.currentScreens: # Starts updating the graphs of the required screens again.
            if self.currentScreens[key] == True:
                self.root.get_screen(self.screenNames[key]).GraphToggler()

    def CloseDialog(self, *args):
        """
        Closes the Buy and Sell dialogs.
        """
        self.dialog.dismiss()

    def Buy(self, *args):
        """
        It updates the amount of money and stocks the user has. Then it updates the amount of money the user spent on stocks,
        prepares the graphs and portfolio to update, updates the recent trades and stores the transaction in the stockHistory
        and finally calls the SaveProgress function.
        """
        aka = self.dialog.content_cls

        if int(aka.ids.text_input.text) == 0:
            self.dialog.dismiss()
            return

        if int(aka.ids.text_input.text) > aka.ids.buy_slider.max:
            aka.ids.text_input.text = str(int(aka.ids.buy_slider.max))

        self.ownedStocks[aka.stockName] += int(aka.ids.text_input.text)
        self.userMoney -= round((int(aka.ids.text_input.text) * float(self.pastStockValuesDict[aka.stockName])), 2)
        self.spentOnStocks[aka.stockName] = round((self.spentOnStocks[aka.stockName] + (int(aka.ids.text_input.text) * float(self.pastStockValuesDict[aka.stockName]))), 2)

        ### Update the values from the stock screen drawer (Like the stocks owned and cash on hand).
        if self.currentScreens[aka.stockName]:
            self.root.get_screen(self.screenNames[aka.stockName]).ids.stocks_owned.text = f"Stocks Owned: {self.ownedStocks[aka.stockName]}"
            self.root.get_screen(self.screenNames[aka.stockName]).ids.cash_hand.text = f"Cash on hand: ${round(self.userMoney, 2)}"
        
        #################### SCREEN 3 CHANGES ####################

        day = datetime.datetime.today()

        ### Add the transaction to the recent trades and the full history trades. If recent trades has 10 childen then it deletes the last one.
        recentTradesLabels = self.root.get_screen("main").ids['recent_trades'].children
        
        if recentTradesLabels[0].text == "No recent trades to show.": # Removes the "No recent trades label.
            self.root.get_screen("main").ids['recent_trades'].remove_widget(recentTradesLabels[0])

        if len(recentTradesLabels) > 10:
            self.root.get_screen("main").ids['recent_trades'].remove_widget(recentTradesLabels[-1]) 
        
        recent = MDLabel(text=f"· {day.time().hour}:{day.strftime('%M')} -- Bought: {int(aka.ids.text_input.text)} of {aka.stockName}",
                         font_name='fonts/SF-Pro-Display-Regular.ttf', font_size= self.root.get_screen("main").ids['recent_trades'].parent.parent.fontSize,
                         outline_width= 1, outline_colour= (0, 0, 0, 1))
        
        self.root.get_screen("main").ids['recent_trades'].add_widget(recent)

        self.stockHistory.append(f"· {day.date()} {day.time().hour}:{day.strftime('%M')} -- Bought: {int(aka.ids.text_input.text)} of {aka.stockName}")

        ### Portolio screen changes (update values and graph.)
        if self.currentScreens['portfolio']:
            self.root.get_screen("portfolio").changes = True
        
        ### Save transaction
        self.SaveProgress()

        self.dialog.dismiss()

    def Sell(self, *args):
        """
        It updates the amount of money and stocks the user has. Then it updates the amount of money the user spent on stocks,
        prepares the graphs and portfolio to update, updates the recent trades, stores the transaction in the stockHistory
        and finally calls the SaveProgress function.
        """
        aka = self.dialog.content_cls

        if int(aka.ids.text_input.text) == 0:
            self.dialog.dismiss()
            return

        if int(aka.ids.text_input.text) > aka.ids.sell_slider.max:
            aka.ids.text_input.text = str(int(aka.ids.sell_slider.max))

        self.spentOnStocks[aka.stockName] = round((self.spentOnStocks[aka.stockName] - (int(aka.ids.text_input.text) * (self.spentOnStocks[aka.stockName] / self.ownedStocks[aka.stockName]))), 2) # Just a fake relationship between the spent price and the amount of stocks that the user have, to avoid having the error of money spent over 0 when the user has no more stocks.
        self.ownedStocks[aka.stockName] -= int(aka.ids.text_input.text)
        self.userMoney += round((int(aka.ids.text_input.text) * float(self.pastStockValuesDict[aka.stockName])), 2)

        ### Update the values from the stock screen drawer (Like the stocks owned and cash on hand).
        if self.currentScreens[aka.stockName]:
            self.root.get_screen(self.screenNames[aka.stockName]).ids.stocks_owned.text = f"Stocks Owned: {self.ownedStocks[aka.stockName]}"
            self.root.get_screen(self.screenNames[aka.stockName]).ids.cash_hand.text = f"Cash on hand: ${round(self.userMoney, 2)}"

        #################### SCREEN 3 CHANGES ####################

        day = datetime.datetime.today()

        ### Add the transaction to the recent trades and the full history trades. If recent trades has 10 childen then it deletes the last one.
        recentTradesLabels = self.root.get_screen("main").ids['recent_trades'].children
        
        if recentTradesLabels[0].text == "No recent trades to show.": #  Removes the "No recent trades label.
            self.root.get_screen("main").ids['recent_trades'].remove_widget(recentTradesLabels[0])

        if len(recentTradesLabels) > 10:
            self.root.get_screen("main").ids['recent_trades'].remove_widget(recentTradesLabels[-1]) 
        
        recent = MDLabel(text=f"· {day.time().hour}:{day.strftime('%M')} -- Sold: {int(aka.ids.text_input.text)} of {aka.stockName}",
                         font_name='fonts/SF-Pro-Display-Regular.ttf', font_size=  self.root.get_screen("main").ids['recent_trades'].parent.parent.fontSize,
                         outline_width= 1, outline_colour= (0, 0, 0, 1))
        
        self.root.get_screen("main").ids['recent_trades'].add_widget(recent)

        self.stockHistory.append(f"· {day.date()} {day.time().hour}:{day.strftime('%M')} -- Sold: {int(aka.ids.text_input.text)} of {aka.stockName}")
        
        ### Portolio screen changes (update values and graph.)
        if self.currentScreens['portfolio']:
            self.root.get_screen("portfolio").changes = True
        
        ### Save transaction
        self.SaveProgress()
        
        self.dialog.dismiss()
    
    def History(self, *args):
        """
        Opens the whole history dialog box.
        Containing dates and time of the trades made by the user.
        """
        if len(self.stockHistory) == 0:
            toast("No trades have been made yet.")
            return
        
        if not self.dialogHistory:
            self.dialog = MDDialog(
                title="Trade History",
                md_bg_color=(1/255,33/255,72/255,1),
                type= "custom",
                content_cls=HistoryContent(),
                buttons=[
                    MDFlatButton(
                        text="Close",
                        font_name='fonts/SF-Pro-Display-Regular.ttf',
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.CloseDialog,
                        pos_hint={'center_x': .5}
                    ),
                ],
            )
        self.dialog.open()

class BuyContent(MDBoxLayout):
    Builder.load_file("buycontent.kv")

    sliderValue = NumericProperty()

    def Increment(self):
        """
        Increments the value of the slider and the text input in the Buy Content dialog box.
        """
        currentValue = int(self.ids.text_input.text)
        if currentValue < self.ids.buy_slider.max:
            currentValue += 1
            self.ids.text_input.text = str(currentValue)
            self.ids.buy_slider.value = currentValue
        return

    def Decrease(self):
        """
        Decreases the value of the slider and the text input in the Buy Content dialog box.
        """
        currentValue = int(self.ids.text_input.text)
        if currentValue > 0:
            currentValue -= 1
            self.ids.text_input.text = str(currentValue)
            self.ids.buy_slider.value = currentValue
        return

    def Validation(self, *args):
        """
        Checks that the input value in the text input field is correct.
        Example if buying 100 stocks is possible with the amount of cash and if not it defaults to max.
        """
        if int(args[0]) > int(self.ids.buy_slider.max):
            self.ids.text_input.text = str(int(self.ids.buy_slider.max))
            self.ids.buy_slider.value = int(self.ids.text_input.text)
        else:
            self.ids.text_input.text = args[0]
            self.ids.buy_slider.value = int(args[0])

class SellContent(MDBoxLayout):
    Builder.load_file("sellcontent.kv")

    sliderValue = NumericProperty()

    def Increment(self):
        """
        Increments the value of the slider and the text input in the Sell Content dialog box.
        """
        currentValue = int(self.ids.text_input.text)
        if currentValue < self.ids.sell_slider.max:
            currentValue += 1
            self.ids.text_input.text = str(currentValue)
            self.ids.sell_slider.value = currentValue
        return

    def Decrease(self):
        """
        Decreases the value of the slider and the text input in the Sell Content dialog box.
        """
        currentValue = int(self.ids.text_input.text)
        if currentValue > 0:
            currentValue -= 1
            self.ids.text_input.text = str(currentValue)
            self.ids.sell_slider.value = currentValue
        return

    def Validation(self, *args):
        """
        Checks that the input value in the text input field is correct.
        Example if selling 100 stocks with the amount the user has.
        """
        if int(args[0]) > int(self.ids.sell_slider.max):
            self.ids.text_input.text = str(int(self.ids.sell_slider.max))
            self.ids.sell_slider.value = int(self.ids.text_input.text)
        else:
            self.ids.text_input.text = args[0]
            self.ids.sell_slider.value = int(args[0])

class HistoryContent(MDBoxLayout):
    Builder.load_file("historycontent.kv")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loads all the transactions as labels to show them.
        for label in App.get_running_app().stockHistory:
            newLabel = MDLabel(text=label, font_name='fonts/SF-Pro-Display-Regular.ttf',font_size=  self.ids.all_trades.fontSize)
            self.ids.all_trades.add_widget(newLabel)

if __name__ == "__main__":
    StockApp().run()