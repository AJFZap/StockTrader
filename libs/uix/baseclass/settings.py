from kivy.app import App
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
import os

class Settings(Screen):
    wipeDialog = None
    extraConfirmDialog = None
    
    def Selection(self, button):
        """
        It will change the currency and the language of the app depending on wich spinner was changed.
        """
        print(button.text)
    
    def WipeDialog(self):
        """
        Opens the Wipe saved data dialog.
        """
        if not self.wipeDialog:
            self.dialog = MDDialog(
                text="Are you sure you want to wipe all saved data and start over?",
                md_bg_color=(1/255,33/255,72/255,1),
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
                text="ARE YOU ABSOLUTELY CERTAIN THAT YOU WANT THIS? (The app will close too.)",
                md_bg_color=(1/255,33/255,72/255,1),
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
        if os.path.exists("./Save_Data/user_data.json"):
            os.remove("./Save_Data/user_data.json")
            App.get_running_app().stop()

        else:
            self.dialog.dismiss()
            toast("There is no saved data to wipe.")