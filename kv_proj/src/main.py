from typing import Any

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
from kivy.metrics import dp
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

# Нужен для работы kv файлов
import kv_proj.src.kv_classes


import hash_password
# from kv_proj.src.hash_password import hash_password, check_password


Config.set('graphics', 'position', 'custom')
Window.size = (300, 500)


class AlphaBankProject(MDApp):
    box = ObjectProperty(None)

    db: Database = None

    def build_config(self, config):
        config.setdefaults('login', {'username': '', 'password': ''})

    def build(self):

        Window.borderless = False
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        self.db = Database().connect()
        if self._check_config():
            login = self.config.get('login', 'username')
            password = self.config.get('login', 'password')
            res = Database().check_user_exists(login=login)
            if res is not None and password == res['password']:
                return Builder.load_file('templates_new/main_without_config.kv')
        else:
            self.config.setdefaults('login', {'username': '', 'password': ''})
            return Builder.load_file('templates_new/main_with_config.kv')


    def _check_config(self) -> bool:
        if self.config.get('login', 'username') != ''\
                and self.config.get('login', 'password') != '':
            return True
        return False

    def change_screen(self, filename) -> None:
        self.root.current = filename

    def register_account(self, login, password) -> None:
        if len(login) > 4 and len(password) > 4:
            new_password = hash_password.hash_password(password)
            Database().add_new_user(login=login, password=new_password)
            self.config.set('login', 'username', login)
            self.config.set('login', 'password', new_password)
            self.config.write()
            username = self.config.get('login', 'username')
            print(username)
            self.change_screen('home_screen')
        else:
            dialog = MDDialog(text='Длина логина должна быть больше 4')
            dialog.open()

    def login_account(self, login, password) -> None:
        res = Database().check_user_exists(login=login)

        if res is not None and hash_password.check_password(res['password'], password):
            self.config.set('login', 'username', login)
            self.config.set('login', 'password', res['password'])
            self.config.write()
            self.change_screen('home_screen')
        else:
            dialog = MDDialog(text='Неверный логин или пароль')
            dialog.open()

    def get_width(self) -> Any:
        return Window.size[0]

    def get_height(self) -> Any:
        return Window.size[1]

    def clear(self) -> None:
            self.box.add_widget(kv_proj.src.kv_classes.ImageButton(Image='C:\\Users\\Danil\\Desktop\\12.jpg'), index=2)

    # def on_gps_location(**kwargs):
    #     print('lat: {lat}, lon: {lon}'.format(**kwargs))
    #
    # def on_start(self):
    #     gps.configure(on_location=self.on_gps_location)
    #     gps.start()
    #     gps.stop()


if __name__ == '__main__':
    AlphaBankProject().run()
