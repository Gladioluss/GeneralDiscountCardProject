from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemeManager
from kivymd.uix.screen import MDScreen

Config.set('graphics', 'position', 'custom')
Window.size = (300, 500)


class AlphaBankProject(MDApp):
    def build(self):
        Window.borderless = False
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        return Builder.load_file('templates/authorization_or_registration_screen.kv')

    def logger(self):
        self.root.ids.welcome_label.text = f'Sup{self.root.ids.user.text}'


if __name__ == '__main__':
    AlphaBankProject().run()
