import os.path

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.factory import Factory
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, BaseListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen
from plyer import gps

from kv_proj.src.data_base import Database

from os.path import join

Config.set('graphics', 'position', 'custom')
Window.size = (300, 500)


class AlphaBankProject(MDApp):
    class ContentNavigationDrawer(BoxLayout):
        pass

    class WindowManager(ScreenManager):
        pass

    class Authorization_or_registration_screen(Screen):
        pass

    class Registration_screen(Screen):
        pass

    class Home_screen(Screen):
        pass

    class StartScreen(BoxLayout):
        pass

    class Login_screen(Screen):
        pass

    db: Database = None

    def build(self):

        Window.borderless = False
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        self.db = Database().connect()
        if self.check_config():
            login = self.config.get('login', 'username')
            password = self.config.get('login', 'password')
            res = Database().check_user_exists(login=login)
            if res is not None and password == res['password']:
                print("MAIN")
                return Builder.load_file('templates_new/main_without_config.kv')
        else:
            print("GUI")
            self.config.setdefaults('login', {'username': '', 'password': ''})
            return Builder.load_file('templates_new/main_with_config.kv')

    def check_config(self):
        if self.config.get('login', 'username') != ''\
                and self.config.get('login', 'password') != '':
            return True
        return False

    def build_config(self, config):
        config.setdefaults('login', {'username': '', 'password': ''})

    def change_screen(self, filename):
        self.root.current = filename

    def register_account(self, login, password):
        if len(login) > 4 and len(password) > 4:
            # Database().add_new_user(login=login, password=password)
            # self.config.add_section('default_section')
            self.config.set('login', 'username', login)
            self.config.set('login', 'password', password)
            self.config.write()
            username = self.config.get('login', 'username')
            print(username)
            # self.change_screen('main_screen')
            self.change_screen('home_screen')
        else:
            dialog = MDDialog(text='Длина логина должна быть больше 4')
            dialog.open()

    def login_account(self, login, password):
        res = Database().check_user_exists(login=login)

        if res is not None and password == res['password']:
            # self.change_screen('main_screen')
            self.change_screen('home_screen')
        else:
            dialog = MDDialog(text='Неверный логин или пароль')
            dialog.open()

    # def on_gps_location(**kwargs):
    #     print('lat: {lat}, lon: {lon}'.format(**kwargs))
    #
    # def on_start(self):
    #     gps.configure(on_location=self.on_gps_location)
    #     gps.start()
    #     gps.stop()


if __name__ == '__main__':
    AlphaBankProject().run()
