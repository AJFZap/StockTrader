from kivy.app import App
from kivy.uix.screenmanager import Screen
from garden_matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np
from kivy.clock import Clock

plt.style.use('seaborn-darkgrid')

thing = App.get_running_app()

openPrice = [thing.openPrice['TSLA']]
times = [0]
stockPrice = [thing.currentStockPrice['TSLA']]

fig,ax = plt.subplots()

ax.plot(times, stockPrice, label= f'Price: ${stockPrice[-1]}', marker='o')
ax.plot(times, openPrice, label= f'Open Price: {openPrice[0]}', linestyle='--')

ax.legend(ncol= 2,bbox_to_anchor = (0.5,1.15),loc='upper center', labelcolor='white', prop={'weight':'bold', 'size': 10})
ax.set_facecolor('black')
fig.set_facecolor((1/255,33/255,72/255,1))
ax.tick_params(axis='y', colors='white')

frame = plt.gca()

frame.get_xaxis().set_visible(False)
frame.yaxis.tick_right()

plt.yticks(np.arange(min(stockPrice), max(stockPrice)+1, 1.0))
plt.grid(visible=True)

class SecondStock(Screen):
    graphUpdating = True
    isActive = True
    
    def __init__(self, **kw):
        """
        Indicates to the App that the screen has been created and exists 
        then it plots the graph and schedules its constant update.
        """
        super().__init__(**kw)
        thing.currentScreens[self.ids.nav_drawer.name] = True
        self.ids.graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        Clock.schedule_interval(self.UpdateGraph, 2)
    
    
    def UpdateGraph(self, time):
      """
      The only way to make a pseudo animation with matplotlib in Kivy.
      """
      if len(stockPrice) >= 5:
         times.pop(0)
         stockPrice.pop(0)
         openPrice.pop(0)

      times.append(times[-1] + 1)
      stockPrice.append(thing.currentStockPrice['TSLA'])
      openPrice.append(openPrice[0])
      ax.cla()
      ax.plot(times, stockPrice, label= f'Price: ${stockPrice[-1]}', marker='o')
      ax.plot(times, openPrice, label= f'Open Price: {openPrice[0]}', linestyle='--')

      ax.fill_between(times, stockPrice, openPrice,where=np.asarray(stockPrice) > np.asarray(openPrice), interpolate=True, color='green', alpha=0.25)
      ax.fill_between(times, stockPrice, openPrice, where=np.asarray(stockPrice) < np.asarray(openPrice), interpolate=True, color='red', alpha=0.25)
      
      ax.legend(ncol= 2,bbox_to_anchor = (0.5,1.15),loc='upper center', labelcolor='white', prop={'weight':'bold', 'size': 10})
    #   ax.text(times[-1] - 0.1, stockPrice[-1] + 0.4, s=str(stockPrice[-1]), ha='center', va='center')
      
      self.ids.graph.children[0].draw()

      self.ids.current_price.text = f"Current Price: ${stockPrice[-1]}"
    
    def GraphToggler(self):
       """
       Checks if the graph is updating or not in case it is then it stops it.
       If it is not it makes it update again.
       """
       if self.graphUpdating == False and self.isActive == True:
          self.graphUpdating = True
          Clock.schedule_interval(self.UpdateGraph, 2)
          return
       elif self.graphUpdating == True and self.isActive == True:
         Clock.unschedule(self.UpdateGraph)
         self.graphUpdating = False
         return
       else:
          return
    
    def BackToMenu(self):
       """
       When the back arrow is pressed it stops the graph from updating and changes the value that indicates if the grap screen is active or not.
       This is done to improve performance.
       """
       self.isActive = False
       self.graphUpdating = False
       Clock.unschedule(self.UpdateGraph)
       App.get_running_app().root.set_current('main')
 