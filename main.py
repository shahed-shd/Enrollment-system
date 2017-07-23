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
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle


class StudentInfoInputLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(StudentInfoInputLayout, self).__init__(**kwargs)

        n = 14
        idx = n

        idx -= 1
        self.label_rollno = Label(text="Roll no:", italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0, 'y': 1/n*idx})
        self.text_input_rollno = TextInput(text='1437', hint_text='Enter roll no here.', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1/n), pos_hint={'x': 0.5, 'y': 1/n*idx})

        idx -= 1
        self.label_name = Label(text="Name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_firstname = TextInput(text='', hint_text='First name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_lastname = TextInput(text='', hint_text='last name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})

        idx -= 1
        self.label_fathersname = Label(text="Father's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_fathersname = TextInput(text='', hint_text='Enter here.', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})

        idx -= 1
        self.label_mothersname = Label(text="Mother's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_mothersname = TextInput(text='', hint_text='Enter here.', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})

        idx -= 1
        self.label_gender = Label(text="Gender:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_gender = Spinner(text='Male', values=('Male', 'Female', 'Other'), size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        self.label_bloodgroup = Label(text="Blood group:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})
        self.spinner_bloodgroup = Spinner(text='O+', values=('A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-'), size_hint=(0.25, 1 / n), pos_hint={'x': 0.75, 'y': 1 / n * idx})

        idx -= 1
        self.label_dob = Label(text="Date of birth:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_dob_day = TextInput(text='', hint_text='DD', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_dob_month = TextInput(text='', hint_text='MM', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})
        self.text_input_dob_year = TextInput(text='', hint_text='YYYY', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.25, 1 / n), pos_hint={'x': 0.75, 'y': 1 / n * idx})

        self.add_widget(self.label_rollno)
        self.add_widget(self.text_input_rollno)
        self.add_widget(self.label_name)
        self.add_widget(self.text_input_firstname)
        self.add_widget(self.text_input_lastname)
        self.add_widget(self.label_fathersname)
        self.add_widget(self.text_input_fathersname)
        self.add_widget(self.label_mothersname)
        self.add_widget(self.text_input_mothersname)
        self.add_widget(self.label_gender)
        self.add_widget(self.spinner_gender)
        self.add_widget(self.label_bloodgroup)
        self.add_widget(self.spinner_bloodgroup)
        self.add_widget(self.label_dob)
        self.add_widget(self.text_input_dob_day)
        self.add_widget(self.text_input_dob_month)
        self.add_widget(self.text_input_dob_year)


class HomeScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)

        self.add_widget(StudentInfoInputLayout())


class StartScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StartScreenLayout, self).__init__(**kwargs)

        # Canvas color.
        with self.canvas.before:
            Color(0.25, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda *a: setattr(self.rect, 'size', self.size), pos=lambda *a: setattr(self.rect, 'pos', self.pos))

        # adding widgets.
        self.add_widget(Image(source='images/IST_logo.png', allow_stretch=True, keep_ratio=False, color=(0.5, 0.5, 0.5, 1), size_hint=(0.5, 0.5), pos_hint={'x': 0.25, 'y': 0.45}))
        self.add_widget(Label(text='Admin password:', bold=True, italic=True, size_hint=(0.5, 0.075), pos_hint={'x': 0.25, 'y': .25}))
        self.text_input = TextInput(text='', hint_text='Enter password here.', password=True, multiline=False, write_tab=False, focus=False, size_hint=(0.5, 0.075), pos_hint={'x': 0.25, 'y': 0.175})
        self.add_widget(self.text_input)
        self.add_widget(Button(text='Submit', bold=True, italic=True, on_release=self.perform_submit, size_hint=(0.15, 0.075), pos_hint={'x': 0.35, 'y': 0.075}))
        self.add_widget(Button(text='Reset', bold=True, italic=True, on_release=lambda *a: setattr(self.text_input, 'text', ''), size_hint=(0.15, 0.075), pos_hint={'x': 0.5, 'y': 0.075}))


    def perform_submit(self, *a):
        if self.text_input.text == '12345':
            mngr = self.parent.manager
            mngr.transition.direction = 'left'
            mngr.current = 'home_screen'


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__(**kwargs)

        start_scr = Screen(name='start_screen')
        home_scr = Screen(name='home_screen')

        self.start_screen_layout = StartScreenLayout()
        self.home_screen_layout = HomeScreenLayout()

        start_scr.add_widget(self.start_screen_layout)
        home_scr.add_widget(self.home_screen_layout)

        self.add_widget(start_scr)
        self.add_widget(home_scr)

        # self.current = 'home_screen'


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