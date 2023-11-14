from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton, MDRaisedButton

class Settings(Screen):
    wipeDialog = None
    extraConfirmDialog = None
    
    def Selection(self, button):
        """
        It will change the currence and the language of the app depending on wich spinner was changed.
        """
        print(button.text)
    
    def WipeDialog(self):
        """
        Opens the Wipe saved data dialog.
        """
        if not self.wipeDialog:
            self.dialog = MDDialog(
                text="Are you sure you want to wipe all saved data and start over?",
                buttons=[
                    MDRaisedButton(
                        text="Wipe",
                        on_release=self.ExtraConfirmation,
                    ),
                    MDFlatButton(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.primary_color,
                        on_release=self.CloseDialog,
                    ),
                ],
            )
        self.dialog.open()
    
    def ExtraConfirmation(self, *args):
        """
        Extra step dialog to wipe the saved data just to be sure.
        """
        self.dialog.dismiss() # Closes the first dialog.

        if not self.extraConfirmDialog:
            self.dialog = MDDialog(
                text="ARE YOU ABSOLUTELY CERTAIN THAT YOU WANT THIS?",
                buttons=[
                    MDRaisedButton(
                        text="Yes, wipe my data",
                        on_release=self.WipeData,
                    ),
                    MDFlatButton(
                        text="No, keep my data",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.primary_color,
                        on_release=self.CloseDialog,
                    ),
                ],
            )
        self.dialog.open()
    
    def CloseDialog(self, *args):
        """
        closes the wipe dialog.
        """
        self.dialog.dismiss()
    
    def WipeData(self, *args):
        """
        When clicked it will clear all the saved data from the user, so they can start over if they want.
        """
        self.dialog.dismiss()