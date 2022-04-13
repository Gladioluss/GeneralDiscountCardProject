from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.factory import Factory
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemeManager
from kivymd.uix.screen import MDScreen
import plyer

from kv_proj.src.data_base import Database


Config.set('graphics', 'position', 'custom')
Window.size = (300, 500)


class AlphaBankProject(MDApp):
    db: Database = None

    def build(self):

        Window.borderless = False
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        GUI = Builder.load_file('templates/authorization_or_registration_screen.kv')
        self.db = Database().connect()
        return GUI

    def change_screen(self, filename):
        self.root.current = filename

    def register_account(self, login, password):
        if len(login) > 4 and len(password) > 4:
            Database().add_new_user(login=login, password=password)
            self.change_screen('main_screen')
        else:
            dialog = MDDialog(text='Длина логина должна быть больше 4')
            dialog.open()

    def login_in_account(self, login, password):
        res = Database().check_user_exists(login=login)
        if res is not None and password == res['password']:
            self.change_screen('main_screen')
        else:
            dialog = MDDialog(text='Неверный логин или пароль')
            dialog.open()


if __name__ == '__main__':
    AlphaBankProject().run()
