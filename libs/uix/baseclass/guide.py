from kivy.app import App
from kivy.uix.screenmanager import Screen

class Guide(Screen):
    tutorialImages=['generalScreen.png', 'stocks.png', 'buyStocks.png', 'sellStocks.png', 'graphScreen.png', 'graphDrawer.png', 'profileScreen.png', 'portfolio.png']
    currentImage = 0

    def BackToMenu(self):
        """
        Resets the Image tutorial to the first one disables the 'Previous' button and enables the 'Next' button if needed.
        """
        self.currentImage = 0
        self.ids.tutorial_image.source = f"images/tutorial_images/{self.tutorialImages[self.currentImage]}"

        self.ids.previous.disabled = True
        self.ids.next.disabled = False
        App.get_running_app().root.set_current('main')
    
    def ImageChange(self, button):
        """
        Either changes the displayed image to the next one or to the previous one.
        """
        if button.text == 'Previous':
            self.currentImage -= 1
            self.ids.tutorial_image.source = f"images/tutorial_images/{self.tutorialImages[self.currentImage]}"
            
            if self.currentImage > 0:
                # Enables the next button to function.
                self.ids.next.disabled = False
            elif self.currentImage == 0:
                # When there is no more previous images it disables itself.
                button.disabled = True
        else:
            self.currentImage += 1
            self.ids.tutorial_image.source = f"images/tutorial_images/{self.tutorialImages[self.currentImage]}"
            
            if self.currentImage > 0 and self.currentImage != len(self.tutorialImages)-1:
                # Enables the previous button to function.
                self.ids.previous.disabled = False
            elif self.currentImage == len(self.tutorialImages)-1:
                # When there is no more next images it disables itself.
                button.disabled = True