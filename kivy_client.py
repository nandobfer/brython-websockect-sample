from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NumericProperty
from kivy.uix.floatlayout import FloatLayout

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    id: menuscreen
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'assets/background.jpg'
    FloatLayout:
        Button:
        # PLAY BUTTON
            text: "PLAY"
            font_size: '50sp'
            font_name: 'assets/cthulus_calling.ttf'
            pos: (self.parent.width / 2) - (self.width / 2), -self.height/4
            size_hint: None, None
            size: menuscreen.button_width, menuscreen.button_height
            background_normal: 'assets/buttons/button.png'
            background_down: 'assets/buttons/button_down.png'
            on_release: print(self.size)
        Button:
        # OPTIONS BUTTON
            text: "OPTIONS"
            font_size: '50sp'
            font_name: 'assets/cthulus_calling.ttf'
            pos: self.parent.width - self.width, -self.height/4
            size_hint: None, None
            size: menuscreen.button_width, menuscreen.button_height
            background_normal: 'assets/buttons/button.png'
            background_down: 'assets/buttons/button_down.png'
            on_release: root.manager.current = 'settings'
        Button:
        # QUIT BUTTON
            text: "QUIT"
            font_size: '50sp'
            font_name: 'assets/cthulus_calling.ttf'
            pos: 0, -self.height/4
            size_hint: None, None
            size: menuscreen.button_width, menuscreen.button_height
            background_normal: 'assets/buttons/button.png'
            background_down: 'assets/buttons/button_down.png'
            on_press: print(menuscreen.button_width, menuscreen.button_height)
        Label:
            text: 'TITLE'
            pos: 0, self.height / 3
            font_size: '70sp'
            font_name: 'assets/cthulus_calling.ttf'



<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_release: root.manager.current = 'menu'
""")


class MenuScreen(Screen):
    button_width = NumericProperty(250)
    button_height = NumericProperty(180)


class SettingsScreen(Screen):
    pass


sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))


class TestApp(App):
    def build(self):
        return sm

    def on_app_press(self):
        print('foi')


if __name__ == '__main__':
    TestApp().run()
