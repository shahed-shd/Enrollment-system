import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.cache import Cache
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle

from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

# SQL part ..................................................

engine = create_engine('mysql+pymysql://root:abcd1234@localhost/enrollment_system', echo=True)
Base = declarative_base()

class Student(Base):
    __table__ = Table('students', Base.metadata,
                      Column('dept', String(5), primary_key=True),
                      Column('roll_no', Integer, primary_key=True),
                      Column('first_name', String(25)),
                      Column('last_name', String(25)),
                      Column('fathers_name', String(50)),
                      Column('mothers_name', String(50)),
                      Column('gender', String(10)),
                      Column('blood_group', String(5)),
                      Column('date_of_birth', Date),
                      Column('address', String(200)),
                      Column('nationality', String(25)),
                      Column('email_address', String(100)),
                      Column('phone_no', String(25)),
                      Column('ssc_roll_no', Integer),
                      Column('ssc_reg_no', Integer),
                      Column('ssc_gpa', Float),
                      Column('ssc_year', Integer),
                      Column('ssc_board', String(25)),
                      Column('hsc_roll_no', Integer),
                      Column('hsc_reg_no', Integer),
                      Column('hsc_gpa', Float),
                      Column('hsc_year', Integer),
                      Column('hsc_board', String(25)),
                      Column('photo_path', String(150)))

    def __repr__(self):
        return "<Student(roll_no={}, dept={}, name={} {},)>".format(self.roll_no, self.dept, self.first_name, self.last_name)


Base.metadata.create_all(engine)

# UI part ..................................................


class StudentInfoInputLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(StudentInfoInputLayout, self).__init__(**kwargs)

        n = 14
        idx = n

        idx -= 1
        self.label_name = Label(text="Name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_firstname = TextInput(text='', hint_text='First name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.37, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_lastname = TextInput(text='', hint_text='last name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.37, 1 / n), pos_hint={'x': 0.62, 'y': 1 / n * idx})

        idx -= 1
        self.label_fathersname = Label(text="Father's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_fathersname = TextInput(text='', hint_text="Father's name", password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_mothersname = Label(text="Mother's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_mothersname = TextInput(text='', hint_text="Mother's name", password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_gender = Label(text="Gender:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_gender = Spinner(text='Male', values=('Male', 'Female', 'Other'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_bloodgroup = Label(text="Blood group:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_bloodgroup = Spinner(text='O+', values=('A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_dob = Label(text="Date of birth:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_dob_day = TextInput(text='', hint_text='DD', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.12, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_dob_month = TextInput(text='', hint_text='MM', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.12, 1 / n), pos_hint={'x': 0.37, 'y': 1 / n * idx})
        self.text_input_dob_year = TextInput(text='', hint_text='YYYY', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1 / n), pos_hint={'x': 0.49, 'y': 1 / n * idx})

        idx -= 1
        self.label_address = Label(text="Address:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_address = TextInput(text='', hint_text='Address', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_nationality = Label(text="Nationality:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_nationality = TextInput(text='', hint_text='Nationality', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_email_address = Label(text="Email address:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_email_address = TextInput(text='', hint_text='Email address', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_phone_no = Label(text="Phone no.:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_phone_no = TextInput(text='', hint_text='Phone no.', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_ssc = Label(text='SSC:', italic=True, size_hint=(0.16, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_ssc_roll = TextInput(text='', hint_text='Roll no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.16, 'y': 1 / n * idx})
        self.text_input_ssc_reg = TextInput(text='', hint_text='Reg no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.32, 'y': 1 / n * idx})
        self.text_input_ssc_gpa = TextInput(text='', hint_text='GPA', password=False, multiline=False, write_tab=False, focus=False, input_filter='float', size_hint=(0.16, 1 / n), pos_hint={'x': 0.48, 'y': 1 / n * idx})
        self.text_input_ssc_year = TextInput(text='', hint_text='Year', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.64, 'y': 1 / n * idx})
        self.spinner_ssc_board = Spinner(text='Dhaka', values=('Dhaka', 'Rajshahi', 'Comilla', 'Jessore', 'Chittagong', 'Barisal', 'Sylhet', 'Dinajpur', 'Madrasah'), size_hint=(0.16, 1 / n), pos_hint={'x': 0.80, 'y': 1 / n * idx})

        idx -= 1
        self.label_hsc = Label(text='HSC:', italic=True, size_hint=(0.16, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_hsc_roll = TextInput(text='', hint_text='Roll no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.16, 'y': 1 / n * idx})
        self.text_input_hsc_reg = TextInput(text='', hint_text='Reg no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.32, 'y': 1 / n * idx})
        self.text_input_hsc_gpa = TextInput(text='', hint_text='GPA', password=False, multiline=False, write_tab=False, focus=False, input_filter='float', size_hint=(0.16, 1 / n), pos_hint={'x': 0.48, 'y': 1 / n * idx})
        self.text_input_hsc_year = TextInput(text='', hint_text='Year', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.64, 'y': 1 / n * idx})
        self.spinner_hsc_board = Spinner(text='Dhaka', values=('Dhaka', 'Rajshahi', 'Comilla', 'Jessore', 'Chittagong', 'Barisal', 'Sylhet', 'Dinajpur', 'Madrasah'), size_hint=(0.16, 1 / n), pos_hint={'x': 0.80, 'y': 1 / n * idx})

        idx -= 1
        self.label_dept = Label(text='Department:', italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_dept = Spinner(text='CSE', values=('CSE', 'ECE', 'BBA'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_rollno = Label(text="Roll no:", italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0, 'y': 1/n*idx})
        self.text_input_rollno = TextInput(text='', hint_text='Roll no.', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})

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
        self.add_widget(self.label_address)
        self.add_widget(self.text_input_address)
        self.add_widget(self.label_nationality)
        self.add_widget(self.text_input_nationality)
        self.add_widget(self.label_email_address)
        self.add_widget(self.text_input_email_address)
        self.add_widget(self.label_phone_no)
        self.add_widget(self.text_input_phone_no)
        self.add_widget(self.label_ssc)
        self.add_widget(self.text_input_ssc_roll)
        self.add_widget(self.text_input_ssc_reg)
        self.add_widget(self.text_input_ssc_gpa)
        self.add_widget(self.text_input_ssc_year)
        self.add_widget(self.spinner_ssc_board)
        self.add_widget(self.label_hsc)
        self.add_widget(self.text_input_hsc_roll)
        self.add_widget(self.text_input_hsc_reg)
        self.add_widget(self.text_input_hsc_gpa)
        self.add_widget(self.text_input_hsc_year)
        self.add_widget(self.spinner_hsc_board)
        self.add_widget(self.label_dept)
        self.add_widget(self.spinner_dept)
        self.add_widget(self.label_rollno)
        self.add_widget(self.text_input_rollno)


    def reset_fields(self, *a):
        self.text_input_rollno.text = ''
        self.text_input_firstname.text = ''
        self.text_input_lastname.text = ''
        self.text_input_fathersname.text = ''
        self.text_input_mothersname.text = ''
        self.spinner_gender.text = 'Male'
        self.spinner_bloodgroup.text = 'O+'
        self.text_input_dob_day.text = ''
        self.text_input_dob_month.text = ''
        self.text_input_dob_year.text = ''
        self.text_input_address.text = ''
        self.text_input_nationality.text = ''
        self.text_input_email_address.text = ''
        self.text_input_phone_no.text = ''
        self.text_input_ssc_roll.text = ''
        self.text_input_ssc_reg.text = ''
        self.text_input_ssc_gpa.text = ''
        self.text_input_ssc_year.text = ''
        self.spinner_ssc_board.text = 'Dhaka'
        self.text_input_hsc_roll.text = ''
        self.text_input_hsc_reg.text = ''
        self.text_input_hsc_gpa.text = ''
        self.text_input_hsc_year.text = ''
        self.spinner_hsc_board.text = 'Dhaka'
        self.spinner_dept.text = 'CSE'


class FileChooserPopup(Popup):
    def __init__(self, **kwargs):
        super(FileChooserPopup, self).__init__(**kwargs)

        self.title = 'Select photo (.jpg, .jpeg, .png)'

        layout = RelativeLayout()

        file_chooser_list_view = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'], size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0.2})
        file_chooser_list_view.bind(selection=self.file_chooser_selection_do)
        self.text_input = TextInput(text='', readonly=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.1})

        layout.add_widget(file_chooser_list_view)
        layout.add_widget(self.text_input)
        layout.add_widget(Button(text='Select', italic=True, on_release=self.dismiss, size_hint=(0.25, 0.1), pos_hint={'x': 0.25, 'y': 0}))
        layout.add_widget(Button(text='Cancel', italic=True, on_release=self.cancel_btn_do, size_hint=(0.25, 0.1), pos_hint={'x': 0.5, 'y': 0}))

        self.content = layout


    def file_chooser_selection_do(self, fc, selection, *a):
        self.text_input.text = selection[0] if selection else ''


    def cancel_btn_do(self, *a):
        self.text_input.text = ''
        self.dismiss()


class AddNewTabLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(AddNewTabLayout, self).__init__(**kwargs)

        self.student_info_input_layout = StudentInfoInputLayout(size_hint=(1, 0.75), pos_hint={'x': 0, 'y': 0.25})
        self.text_input_file_choose = TextInput(text='', hint_text='No file selected', readonly=True, size_hint=(0.6, 0.057), pos_hint={'x': 0.25, 'y': 0.17})
        self.file_chooser_popup = FileChooserPopup(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.file_chooser_popup.bind( on_dismiss=lambda popup_instance, *a: setattr(self.text_input_file_choose, 'text', popup_instance.text_input.text))

        self.add_widget(self.student_info_input_layout)

        self.add_widget(Label(text='Photo:', italic=True, size_hint=(0.25, 0.057), pos_hint={'x': 0, 'y': 0.17}))
        self.add_widget(self.text_input_file_choose)
        self.add_widget(Button(text='Choose', italic=True, on_release=self.file_chooser_popup.open, size_hint=(0.14, 0.057), pos_hint={'x': 0.85, 'y': 0.17}))

        self.add_widget(Button(text='Add', italic=True, size_hint=(0.45, 0.075), pos_hint={'x': 0.05, 'y': 0.03}))
        self.add_widget(Button(text='Reset', italic=True, on_release=self.reset_btn_do, size_hint=(0.45, 0.075), pos_hint={'x': 0.5, 'y': 0.03}))


    def reset_btn_do(self, *a):
        self.student_info_input_layout.reset_fields()
        self.text_input_file_choose.text = ''


class FindTabLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(FindTabLayout, self).__init__(**kwargs)

        self.student_info_input_layout = StudentInfoInputLayout(size_hint=(0.50, 0.85), pos_hint={'x': 0, 'y': 0.15})

        self.add_widget(self.student_info_input_layout)
        self.add_widget(Button(text='Find', italic=True, size_hint=(0.20, 0.075), pos_hint={'x': 0.05, 'y': 0.03}))
        self.add_widget(Button(text='Reset', italic=True, on_release=self.student_info_input_layout.reset_fields, size_hint=(0.20, 0.075), pos_hint={'x': 0.25, 'y': 0.03}))


class HomeScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)

        tp = TabbedPanel(do_default_tab=False)

        self.th_home = TabbedPanelHeader(text='Home')
        self.th_add_new = TabbedPanelHeader(text='Add new', content=AddNewTabLayout())
        self.th_find = TabbedPanelHeader(text='Find', content=FindTabLayout())

        # self.th_add_new.content = layout

        tp.add_widget(self.th_home)
        tp.add_widget(self.th_add_new)
        tp.add_widget(self.th_find)

        self.add_widget(tp)


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

        self.current = 'home_screen'


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