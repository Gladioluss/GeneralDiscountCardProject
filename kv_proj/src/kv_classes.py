from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.utils.fitimage import FitImage


class ContentNavigationDrawer(BoxLayout):
    pass


class WindowManager(ScreenManager):
    pass


class Authorization_or_registration_screen(Screen):
    pass


class Registration_screen(Screen):
    pass


class Home_screen(Screen):

    count = 0
    layouts = []

    def add(self):

        if not self.layouts:
            self.ids.box.clear_widgets()

        self.count += 1
        layout = MDGridLayout(cols=2, size_hint_y=None)
        layout.add_widget(FitImageButton(source='C:\\Users\\Danil\\Desktop\\12.jpg', radius=[10, 10, 10, 10, ]))
        self.ids.box.add_widget(layout)
        self.layouts.append(layout)





class StartScreen(BoxLayout):
    pass


class Login_screen(Screen):
    pass


class FitImageButton(ButtonBehavior, FitImage):
    def on_press(self):
        print('pressed')
