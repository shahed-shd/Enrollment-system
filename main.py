import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.cache import Cache
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle


class HomeScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)

        # Canvas color
        with self.canvas.before:
            Color(0.25, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda *a: setattr(self.rect, 'size', self.size), pos=lambda *a: setattr(self.rect, 'pos', self.pos))

        # Popup feature.
        self.popup_create_new_system = Popup(title='Create new system', title_color=(0, 1, 1, 1), separator_height=2, title_align='center', size_hint=(0.9, 0.5), auto_dismiss=False)

        layout = RelativeLayout()
        text_input = TextInput(text='', hint_text="Enter system name here", focus=False, multiline=False, write_tab=False, size_hint=(0.75, 0.2), pos_hint={'x': 0.125, 'y': 0.65})
        text_input.bind(text=self.space_to_underscore)
        btn_create = Button(text='Create', on_release=self.create_new_system, size_hint=(0.25, 0.2), pos_hint={'x': 0.25, 'y': 0.25})
        btn_cancel = Button(text='Cancel', on_release=self.popup_create_new_system.dismiss, size_hint=(0.25, 0.2), pos_hint={'x': 0.5, 'y': 0.25})

        layout.add_widget(text_input)
        layout.add_widget(btn_create)
        layout.add_widget(btn_cancel)

        self.popup_create_new_system.content = layout
        self.popup_text_input = text_input

        # Adding widgets.
        self.add_widget(Label(text='Systems:', italic=True, bold=True, font_size=30, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.9}))
        self.add_widget(Button(text='Create new system', on_release=self.popup_create_new_system.open, size_hint=(0.5, 0.1), pos_hint={'x': 0.25, 'y': 0.8}))


    def space_to_underscore(self, *a):
        if len(self.popup_text_input.text) > 0 and self.popup_text_input.text[-1] == ' ':
            self.popup_text_input.text = self.popup_text_input.text[:-1] + '_'


    def create_new_system(self, *a):
        if len(self.popup_text_input.text) > 0:
            print("New system name:", self.popup_text_input.text)
            self.popup_text_input.text = ''
            self.popup_create_new_system.dismiss()
            # sql task here


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

        home_scr = Screen(name='home_screen')

        self.home_screen_layout = HomeScreenLayout()

        home_scr.add_widget(self.home_screen_layout)

        self.add_widget(home_scr)


class EnrollmentSystem(App):
    def __init__(self, **kwargs):
        super(EnrollmentSystem, self).__init__(**kwargs)


    def build(self):
        return MainScreenManager()


def main():
    app = EnrollmentSystem()
    app.run()


if __name__ == '__main__':
    main()