import kivy
kivy.require('1.10.0')

import time
import datetime
import os
import re
import shutil
from enum import Enum, unique

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
from kivy.storage.jsonstore import JsonStore
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
Session = sessionmaker(bind=engine)
session = Session()


def find_next_roll_to_have(L, start):
    if not L:
        return start

    if L[0] != start:
        return start

    len_L = len(L)

    if len_L > 1:
        for i in range(1, len_L):
            if not L[i-1]+1 == L[i]:
                return L[i-1] + 1

    return L[-1] + 1


def is_valid_date(y, m, d):
    try:
        datetime.date(year=y, month=m, day=d)
    except:
        return False

    return True


def is_valid_emaid(email):
    return  bool(re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

# UI part ..................................................


class StudentInfoInputLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(StudentInfoInputLayout, self).__init__(**kwargs)

        n = 14
        idx = n

        idx -= 1
        label_name = Label(text="Name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_firstname = TextInput(text='', hint_text='First name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.37, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_lastname = TextInput(text='', hint_text='last name', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.37, 1 / n), pos_hint={'x': 0.62, 'y': 1 / n * idx})

        idx -= 1
        label_fathersname = Label(text="Father's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_fathersname = TextInput(text='', hint_text="Father's name", password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_mothersname = Label(text="Mother's name:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_mothersname = TextInput(text='', hint_text="Mother's name", password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_gender = Label(text="Gender:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_gender = Spinner(text='Male', values=('Male', 'Female', 'Other'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_bloodgroup = Label(text="Blood group:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_bloodgroup = Spinner(text='O+', values=('A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_dob = Label(text="Date of birth:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_dob_day = TextInput(text='', hint_text='DD', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.12, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.text_input_dob_month = TextInput(text='', hint_text='MM', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.12, 1 / n), pos_hint={'x': 0.37, 'y': 1 / n * idx})
        self.text_input_dob_year = TextInput(text='', hint_text='YYYY', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1 / n), pos_hint={'x': 0.49, 'y': 1 / n * idx})

        idx -= 1
        label_address = Label(text="Address:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_address = TextInput(text='', hint_text='Address', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_nationality = Label(text="Nationality:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_nationality = TextInput(text='', hint_text='Nationality', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_email_address = Label(text="Email address:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_email_address = TextInput(text='', hint_text='Email address', password=False, multiline=False, write_tab=False, focus=False, size_hint=(0.74, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_phone_no = Label(text="Phone no.:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_phone_no = TextInput(text='', hint_text='Phone no.', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_ssc = Label(text='SSC:', italic=True, size_hint=(0.16, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_ssc_roll = TextInput(text='', hint_text='Roll no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.16, 'y': 1 / n * idx})
        self.text_input_ssc_reg = TextInput(text='', hint_text='Reg no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.32, 'y': 1 / n * idx})
        self.text_input_ssc_gpa = TextInput(text='', hint_text='GPA', password=False, multiline=False, write_tab=False, focus=False, input_filter='float', size_hint=(0.16, 1 / n), pos_hint={'x': 0.48, 'y': 1 / n * idx})
        self.text_input_ssc_year = TextInput(text='', hint_text='Year', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.64, 'y': 1 / n * idx})
        self.spinner_ssc_board = Spinner(text='Dhaka', values=('Dhaka', 'Rajshahi', 'Comilla', 'Jessore', 'Chittagong', 'Barisal', 'Sylhet', 'Dinajpur', 'Madrasah'), size_hint=(0.16, 1 / n), pos_hint={'x': 0.80, 'y': 1 / n * idx})

        idx -= 1
        label_hsc = Label(text='HSC:', italic=True, size_hint=(0.16, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_hsc_roll = TextInput(text='', hint_text='Roll no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.16, 'y': 1 / n * idx})
        self.text_input_hsc_reg = TextInput(text='', hint_text='Reg no', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.32, 'y': 1 / n * idx})
        self.text_input_hsc_gpa = TextInput(text='', hint_text='GPA', password=False, multiline=False, write_tab=False, focus=False, input_filter='float', size_hint=(0.16, 1 / n), pos_hint={'x': 0.48, 'y': 1 / n * idx})
        self.text_input_hsc_year = TextInput(text='', hint_text='Year', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.16, 1 / n), pos_hint={'x': 0.64, 'y': 1 / n * idx})
        self.spinner_hsc_board = Spinner(text='Dhaka', values=('Dhaka', 'Rajshahi', 'Comilla', 'Jessore', 'Chittagong', 'Barisal', 'Sylhet', 'Dinajpur', 'Madrasah'), size_hint=(0.16, 1 / n), pos_hint={'x': 0.80, 'y': 1 / n * idx})

        idx -= 1
        label_dept = Label(text='Department:', italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.spinner_dept = Spinner(text='CSE', values=('CSE', 'ECE', 'BBA'), size_hint=(0.5, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        label_rollno = Label(text="Roll no:", italic=True, size_hint=(0.25, 1/n), pos_hint={'x': 0, 'y': 1/n*idx})
        self.text_input_rollno = TextInput(text='', hint_text='Roll no.', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1/n), pos_hint={'x': 0.25, 'y': 1/n*idx})

        self.add_widget(label_name)
        self.add_widget(self.text_input_firstname)
        self.add_widget(self.text_input_lastname)
        self.add_widget(label_fathersname)
        self.add_widget(self.text_input_fathersname)
        self.add_widget(label_mothersname)
        self.add_widget(self.text_input_mothersname)
        self.add_widget(label_gender)
        self.add_widget(self.spinner_gender)
        self.add_widget(label_bloodgroup)
        self.add_widget(self.spinner_bloodgroup)
        self.add_widget(label_dob)
        self.add_widget(self.text_input_dob_day)
        self.add_widget(self.text_input_dob_month)
        self.add_widget(self.text_input_dob_year)
        self.add_widget(label_address)
        self.add_widget(self.text_input_address)
        self.add_widget(label_nationality)
        self.add_widget(self.text_input_nationality)
        self.add_widget(label_email_address)
        self.add_widget(self.text_input_email_address)
        self.add_widget(label_phone_no)
        self.add_widget(self.text_input_phone_no)
        self.add_widget(label_ssc)
        self.add_widget(self.text_input_ssc_roll)
        self.add_widget(self.text_input_ssc_reg)
        self.add_widget(self.text_input_ssc_gpa)
        self.add_widget(self.text_input_ssc_year)
        self.add_widget(self.spinner_ssc_board)
        self.add_widget(label_hsc)
        self.add_widget(self.text_input_hsc_roll)
        self.add_widget(self.text_input_hsc_reg)
        self.add_widget(self.text_input_hsc_gpa)
        self.add_widget(self.text_input_hsc_year)
        self.add_widget(self.spinner_hsc_board)
        self.add_widget(label_dept)
        self.add_widget(self.spinner_dept)
        self.add_widget(label_rollno)
        self.add_widget(self.text_input_rollno)


    def reset_fields(self, *a):
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
        self.text_input_rollno.text = ''


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


class StudentProfileLayout(RelativeLayout, kivy.uix.widget.Widget):
    def __init__(self, **kwargs):
        super(StudentProfileLayout, self).__init__(**kwargs)

        self.student = None     # Will be assigned in attach_student()
        self.any_change = False

        self.profile_pic = Image(allow_stretch=True, keep_ratio=False, size_hint=(0.20, 0.40), pos_hint={'x': 0.025, 'y': 0.55})    # source will be add in attach_student()
        self.student_info_input_layout = StudentInfoInputLayout(size_hint=(0.75, 0.75), pos_hint={'x': 0.25, 'y': 0.25})
        self.student_info_input_layout.spinner_dept.bind(text=self.student_info_input_dept_bind)
        self.student_info_input_layout.text_input_rollno.readonly = True

        self.btn_cancel = Button(text='Cancel', italic=True, on_release=self.btn_cancel_do, size_hint=(0.2, 0.06), pos_hint={'x': 0.75, 'y': 0.08})
        self.btn_ok_update = Button(text='OK', italic=True, on_release=self.btn_ok_update_do, size_hint=(0.2, 0.06), pos_hint={'x': 0.55, 'y': 0.08})
        self.btn_undo_changes = Button(text='Undo changes', italic=True, on_release=self.assign_student_info, opacity=0.25, size_hint=(0.2, 0.06), pos_hint={'x': 0.35, 'y': 0.08})
        self.label_dialogue = Label(text='', italic=True, size_hint=(1, 0.06), pos_hint={'x': 0, 'y': 0.01})

        self.text_input_file_choose = TextInput(text='', hint_text='No file selected', readonly=True, size_hint=(0.6, 0.057), pos_hint={'x': 0.25, 'y': 0.18})
        self.text_input_file_choose.bind(text=lambda *a: setattr(self.profile_pic, 'source', self.text_input_file_choose.text))
        self.file_chooser_popup = FileChooserPopup(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.file_chooser_popup.bind(on_dismiss=lambda popup_instance, *a: setattr(self.text_input_file_choose, 'text', popup_instance.text_input.text))

        self.add_widget(self.profile_pic)
        self.add_widget(self.student_info_input_layout)

        self.add_widget(Label(text='Photo:', italic=True, size_hint=(0.25, 0.057), pos_hint={'x': 0, 'y': 0.18}))
        self.add_widget(self.text_input_file_choose)
        self.add_widget(Button(text='Choose', italic=True, on_release=self.file_chooser_popup.open, size_hint=(0.14, 0.057), pos_hint={'x': 0.85, 'y': 0.18}))

        self.add_widget(self.btn_cancel)
        self.add_widget(self.btn_ok_update)
        self.add_widget(self.btn_undo_changes)
        self.add_widget(self.label_dialogue)

        for ch in self.student_info_input_layout.children:
            if type(ch) != Label:
                ch.bind(text=self.any_change_do)

        self.text_input_file_choose.bind(text=self.any_change_do)


    def student_info_input_dept_bind(self, *a):
        '''Set the roll according to dept.'''

        dept = self.student_info_input_layout.spinner_dept.text

        if dept == self.student.dept:
            self.student_info_input_layout.text_input_rollno.text = str(self.student.roll_no)
            return

        res = session.query(Student.roll_no).filter(Student.dept == dept).order_by(Student.roll_no)
        L = [x[0] for x in res]

        store = Cache.get('global_data', 'records_store')
        start = int(store.get(dept)['start'])

        next_roll = find_next_roll_to_have(L, start)
        self.student_info_input_layout.text_input_rollno.text = str(next_roll)


    # def text_input_file_choose_bind(self, *a):
    #     self.profile_pic.source = self.text_input_file_choose.text


    def check_any_change(self, *a):
        inp = self.student_info_input_layout
        student = self.student

        if inp.text_input_firstname.text != student.first_name:
            return True

        if inp.text_input_lastname.text != student.last_name:
            return True

        if inp.text_input_fathersname.text != student.fathers_name:
            return True

        if inp.text_input_mothersname.text != student.mothers_name:
            return True

        if inp.spinner_gender.text != student.gender:
            return True

        if inp.spinner_bloodgroup.text != student.blood_group:
            return True

        if inp.text_input_dob_day.text != str(student.date_of_birth.day):
            return True

        if inp.text_input_dob_month.text != str(student.date_of_birth.month):
            return True

        if inp.text_input_dob_year.text != str(student.date_of_birth.year):
            return True

        if inp.text_input_address.text != student.address:
            return True

        if inp.text_input_nationality.text != student.nationality:
            return True

        if inp.text_input_email_address.text != student.email_address:
            return True

        if inp.text_input_phone_no.text != student.phone_no:
            return True

        if inp.text_input_ssc_roll.text != str(student.ssc_roll_no):
            return True

        if inp.text_input_ssc_reg.text != str(student.ssc_reg_no):
            return True

        if inp.text_input_ssc_gpa.text != str(student.ssc_gpa):
            return True

        if inp.text_input_ssc_year.text != str(student.ssc_year):
            return True

        if inp.spinner_ssc_board.text != student.ssc_board:
            return True

        if inp.text_input_hsc_roll.text != str(student.hsc_roll_no):
            return True

        if inp.text_input_hsc_reg.text != str(student.hsc_reg_no):
            return True

        if inp.text_input_hsc_gpa.text != str(student.hsc_gpa):
            return True

        if inp.text_input_hsc_year.text != str(student.hsc_year):
            return True

        if inp.spinner_hsc_board.text != student.hsc_board:
            return True

        if inp.spinner_dept.text != student.dept:
            return True

        if inp.text_input_rollno.text != str(student.roll_no):
            return True

        if self.text_input_file_choose.text != student.photo_path:
            return True

        return False


    def any_change_do(self, *a):
        if self.student == None:
            return

        self.any_change = self.check_any_change()

        if self.any_change:
            self.btn_undo_changes.opacity = 1
            self.btn_ok_update.text = 'Update'
        else:
            self.btn_undo_changes.opacity = 0.25
            self.btn_ok_update.text = 'OK'


    def btn_ok_update_do(self, *a):
        if self.any_change:
            self.label_dialogue.text = ''
            inp = self.student_info_input_layout
            student = self.student

            def input_to_obj(input_attr, obj_attr, meta=''):
                value = getattr(inp, input_attr).text
                if value:
                    if value != str(getattr(student, obj_attr)):
                        setattr(student, obj_attr, value)
                    return True
                else:
                    self.label_dialogue.text = meta + " needs to be filled up !"
                    return False

            if not input_to_obj('text_input_firstname', 'first_name', 'First name'): return
            if not input_to_obj('text_input_lastname', 'last_name', 'Last name'): return
            if not input_to_obj('text_input_fathersname', 'fathers_name', "Father's name"): return
            if not input_to_obj('text_input_mothersname', 'mothers_name', "Mother's name"): return
            if not input_to_obj('spinner_gender', 'gender'): return
            if not input_to_obj('spinner_bloodgroup', 'blood_group'): return

            if inp.text_input_dob_day.text != '' and inp.text_input_dob_month.text != '' and inp.text_input_dob_year.text != '':
                d = int(inp.text_input_dob_day.text)
                m = int(inp.text_input_dob_month.text)
                y = int(inp.text_input_dob_year.text)

                if d != student.date_of_birth.day or m != student.date_of_birth.month or y != student.date_of_birth.year:
                    if is_valid_date(y, m, d):
                        student.date_of_birth = datetime.date(year=y, month=m, day=d)
                    else:
                        self.label_dialogue.text = "Invalid date of birth !"
                        return
            else:
                self.label_dialogue.text = "Date of birth needs to be filled up !"
                return

            if not input_to_obj('text_input_address', 'address', 'Address'): return
            if not input_to_obj('text_input_nationality', 'nationality', 'Nationality'): return

            email = inp.text_input_email_address.text
            if email != student.email_address:
                if email:
                    if is_valid_emaid(email):
                        input_to_obj('text_input_email_address', 'email_address')
                    else:
                        self.label_dialogue.text = "Invalid email address !"
                        return
                else:
                    self.label_dialogue.text = "Email address needs to be filled up !"
                    return

            if not input_to_obj('text_input_phone_no', 'phone_no', 'Phone no.'): return
            if not input_to_obj('text_input_ssc_roll', 'ssc_roll_no', 'SSC roll no. '): return
            if not input_to_obj('text_input_ssc_reg', 'ssc_reg_no', 'SSC reg. no.'): return
            if not input_to_obj('text_input_ssc_gpa', 'ssc_gpa', 'SSC GPA'): return
            if not input_to_obj('text_input_ssc_year', 'ssc_year', 'SSC passing year'): return
            if not input_to_obj('spinner_ssc_board', 'ssc_board'): return
            if not input_to_obj('text_input_hsc_roll', 'hsc_roll_no', 'HSC roll no.'): return
            if not input_to_obj('text_input_hsc_reg', 'hsc_reg_no', 'HSC reg. no.'): return
            if not input_to_obj('text_input_hsc_gpa', 'hsc_gpa', 'HSC GPA'): return
            if not input_to_obj('text_input_hsc_year', 'hsc_year', 'HSC passing year'): return
            if not input_to_obj('spinner_hsc_board', 'hsc_board'): return

            if self.text_input_file_choose.text != student.photo_path:
                photo_path_from = self.text_input_file_choose.text if self.text_input_file_choose.text != '' else 'images/blank_profile_pic.jpg'
                photo_path_to = 'images/profile_pics/' + inp.spinner_dept.text + '-' + inp.text_input_rollno.text + os.path.splitext(photo_path_from)[1]
                shutil.copyfile(photo_path_from, photo_path_to)
                student.photo_path = photo_path_to

            if not input_to_obj('spinner_dept', 'dept'): return
            if not input_to_obj('text_input_rollno', 'roll_no'): return

            session.commit()
            self.label_dialogue.text = 'Student info Updated'

        self.btn_cancel_do()


    def btn_cancel_do(self, *a):
        self.parent.parent.parent.dismiss()


    def assign_student_info(self, *a):
        inp = self.student_info_input_layout
        student = self.student

        inp.spinner_dept.text = student.dept
        inp.text_input_rollno.text = str(student.roll_no)
        inp.text_input_firstname.text = student.first_name
        inp.text_input_lastname.text = student.last_name
        inp.text_input_fathersname.text = student.fathers_name
        inp.text_input_mothersname.text = student.mothers_name
        inp.spinner_gender.text = student.gender
        inp.spinner_bloodgroup.text = student.blood_group
        inp.text_input_dob_day.text = str(student.date_of_birth.day)
        inp.text_input_dob_month.text = str(student.date_of_birth.month)
        inp.text_input_dob_year.text = str(student.date_of_birth.year)
        inp.text_input_address.text = student.address
        inp.text_input_nationality.text = student.nationality
        inp.text_input_email_address.text = student.email_address
        inp.text_input_phone_no.text = student.phone_no
        inp.text_input_ssc_roll.text = str(student.ssc_roll_no)
        inp.text_input_ssc_reg.text = str(student.ssc_reg_no)
        inp.text_input_ssc_gpa.text = str(student.ssc_gpa)
        inp.text_input_ssc_year.text = str(student.ssc_year)
        inp.spinner_ssc_board.text = student.ssc_board
        inp.text_input_hsc_roll.text = str(student.hsc_roll_no)
        inp.text_input_hsc_reg.text = str(student.hsc_reg_no)
        inp.text_input_hsc_gpa.text = str(student.hsc_gpa)
        inp.text_input_hsc_year.text = str(student.hsc_year)
        inp.spinner_hsc_board.text = student.hsc_board
        self.text_input_file_choose.text = student.photo_path
        self.profile_pic.source = student.photo_path


    def attach_student(self, *a, student):
        self.student = student
        self.assign_student_info()


class RecycleViewListLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(RecycleViewListLayout, self).__init__(**kwargs)

        self.student = None
        self.popup_student_profile = Popup(title='Profile', title_align='center', content=StudentProfileLayout(), auto_dismiss=False, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.popup_student_profile.bind(on_dismiss=self.popup_student_profile_dismiss_bind)

        n = 5
        idx = n

        idx -= 3
        self.label_dept_roll = Label(text='', italic=True, size_hint=(1, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})

        idx -= 1
        self.label_name = Label(text='', italic=True, size_hint=(1, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})

        idx -= 1
        self.btn_profile = Button(text='Profile', italic=True, on_release=self.btn_profile_do, size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})
        self.btn_delete = Button(text='Delete', italic=True, on_release=self.btn_delete_do, size_hint=(0.25, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx})

        self.add_widget(self.label_dept_roll)
        self.add_widget(self.label_name)
        self.add_widget(self.btn_profile)
        self.add_widget(self.btn_delete)

        Clock.schedule_once(self.assing_student_info, 0)


    def assing_student_info(self, *a):
        self.label_dept_roll.text=self.student.dept + ' - ' + str(self.student.roll_no)
        self.label_name.text=self.student.first_name + ' ' + self.student.last_name


    def btn_profile_do(self, *a):
        # res = session.query(Student).filter(Student.roll_no == 2017001).one()
        self.popup_student_profile.content.attach_student(student=self.student)
        self.popup_student_profile.open()


    def btn_delete_do(self, *a):
        session.delete(self.student)
        session.commit()
        self.parent.parent.parent.find_btn_do()


    def popup_student_profile_dismiss_bind(self, *a):
        if self.popup_student_profile.content.any_change:
            self.assing_student_info()


class RBL(RecycleBoxLayout):
    def __init__(self, **kwargs):
        super(RBL, self).__init__(**kwargs)

        self.default_size_hint = (1, None)
        self.default_size = (None, 100)
        self.size_hint_y = None
        self.bind(minimum_height=lambda a, b: setattr(self, 'height', b))
        self.orientation = 'vertical'


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        self.add_widget(RBL())
        self.viewclass = 'RecycleViewListLayout'
        self.data = []


    def set_data(self, *a, student_list):
        self.data = [{'student': stu} for stu in student_list]


class HomeTabLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(HomeTabLayout, self).__init__(**kwargs)

        # Get start value
        store = Cache.get('global_data', 'records_store')

        if store.exists('CSE'):
            cse_start = store.get('CSE')['start']
        else:
            curr_year = time.localtime(time.time()).tm_year
            cse_start = str(curr_year * 1000 + 1)
            store.put('CSE', start=cse_start)

        if store.exists('ECE'):
            ece_start = store.get('ECE')['start']
        else:
            curr_year = time.localtime(time.time()).tm_year
            ece_start = str(curr_year * 1000 + 1)
            store.put('ECE', start=ece_start)

        if store.exists('BBA'):
            bba_start = store.get('BBA')['start']
        else:
            curr_year = time.localtime(time.time()).tm_year
            bba_start = str(curr_year * 1000 + 1)
            store.put('BBA', start=bba_start)

        # Password change popup
        layout = RelativeLayout()
        self.popup_change_password = Popup(title='Change password', title_align='center', content=layout, size_hint=(0.6, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.popup_change_password.bind(on_open=lambda *a: setattr(layout.text_input_curr_pw, 'text', ''))
        self.popup_change_password.bind(on_open=lambda *a: setattr(layout.text_input_new_pw, 'text', ''))
        self.popup_change_password.bind(on_open=lambda *a: setattr(layout.text_input_re_new_pw, 'text', ''))
        n = 7
        idx = n

        idx -= 1
        layout.add_widget(Label(text='Current password:', italic=True, size_hint=(0.4, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx}))
        layout.text_input_curr_pw = TextInput(text='', hint_text='Current password', password=True, multiline=False, write_tab=False, focus=False, size_hint=(0.6, 1 / n), pos_hint={'x': 0.4, 'y': 1 / n * idx})
        layout.add_widget(layout.text_input_curr_pw)

        idx -= 1
        layout.add_widget(Label(text='New password:', italic=True, size_hint=(0.4, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx}))
        layout.text_input_new_pw = TextInput(text='', hint_text='New password', password=True, multiline=False, write_tab=False, focus=False, size_hint=(0.6, 1 / n), pos_hint={'x': 0.4, 'y': 1 / n * idx})
        layout.add_widget(layout.text_input_new_pw)

        idx -= 1
        layout.add_widget(Label(text='New password:', italic=True, size_hint=(0.4, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx}))
        layout.text_input_re_new_pw = TextInput(text='', hint_text='Re-enter new password', password=True, multiline=False, write_tab=False, focus=False, size_hint=(0.6, 1 / n), pos_hint={'x': 0.4, 'y': 1 / n * idx})
        layout.add_widget(layout.text_input_re_new_pw)

        idx -= 2
        layout.add_widget(Button(text='Change', italic=True, on_release=self.password_change_validation, size_hint=(0.3, 1 / n), pos_hint={'x': 0.2, 'y': 1 / n * idx}))
        layout.add_widget(Button(text='Cancel', italic=True, on_release=self.popup_change_password.dismiss, size_hint=(0.3, 1 / n), pos_hint={'x': 0.5, 'y': 1 / n * idx}))

        idx -= 2
        layout.label_dialogue = Label(text='', italic=True, size_hint=(1, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        layout.add_widget(layout.label_dialogue)

        # Adding widgets to the tab content
        n = 17
        idx = n

        idx -= 1
        self.label_cse_start_roll = Label(text="CSE dept. start roll:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_cse_start_roll = TextInput(text=cse_start, hint_text='CSE dept. start roll', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_ece_start_roll = Label(text="ECE dept. start roll:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_ece_start_roll = TextInput(text=ece_start, hint_text='ECE dept. start roll', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 1
        self.label_bba_start_roll = Label(text="BBA dept. start roll:", italic=True, size_hint=(0.25, 1 / n), pos_hint={'x': 0, 'y': 1 / n * idx})
        self.text_input_bba_start_roll = TextInput(text=bba_start, hint_text='BBA dept. start roll', password=False, multiline=False, write_tab=False, focus=False, input_filter='int', size_hint=(0.25, 1 / n), pos_hint={'x': 0.25, 'y': 1 / n * idx})

        idx -= 2
        self.btn_save_start_rolls = Button(text='Save start rolls', italic=True, on_release=self.save_start_roll_changes, size_hint=(0.4, 1 / n), pos_hint={'x': 0.05, 'y': 1 / n * idx})

        idx -= 3
        self.btn_change_password = Button(text='Change password', italic=True, on_release=self.popup_change_password.open, size_hint=(0.4, 1 / n), pos_hint={'x': 0.05, 'y': 1 / n * idx})

        idx -= 3
        self.btn_log_out = Button(text='Log out', italic=True, on_release=self.log_out, size_hint=(0.4, 1 / n), pos_hint={'x': 0.05, 'y': 1 / n * idx})

        self.add_widget(self.label_cse_start_roll)
        self.add_widget(self.text_input_cse_start_roll)
        self.add_widget(self.label_ece_start_roll)
        self.add_widget(self.text_input_ece_start_roll)
        self.add_widget(self.label_bba_start_roll)
        self.add_widget(self.text_input_bba_start_roll)
        self.add_widget(self.btn_save_start_rolls)

        self.add_widget(self.btn_change_password)
        self.add_widget(self.btn_log_out)


    def log_out(self, *a):
        mngr = self.parent.parent.parent.parent.manager
        mngr.transition.direction = 'right'
        mngr.current = 'start_screen'


    def save_start_roll_changes(self, *a):
        store = Cache.get('global_data', 'records_store')

        def check_and_go(dept):
            if session.query(Student.roll_no).filter(Student.dept == dept).count() == 0:
                store.put(dept, start=getattr(getattr(self, 'text_input_' + dept.lower() + '_start_roll'), 'text'))
            else:
                setattr(getattr(self, 'text_input_' + dept.lower() + '_start_roll'), 'text', store.get('CSE')['start'])

        check_and_go('CSE')
        check_and_go('ECE')
        check_and_go('BBA')


    def password_change_validation(self, *a):
        content = self.popup_change_password.content
        store = Cache.get('global_data', 'records_store')
        curr_pw = store.get('password')['value'] if store.exists('password') else '1234'

        content.label_dialogue.text = ''

        if content.text_input_curr_pw.text != curr_pw:
            content.label_dialogue.text = "Current password doesn't match !"
        elif content.text_input_new_pw.text != content.text_input_re_new_pw.text:
            content.label_dialogue.text = "Re-entering new password doesn't match !"
        else:
            store.put('password', value=content.text_input_new_pw.text)
            self.popup_change_password.dismiss()


class AddNewTabLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(AddNewTabLayout, self).__init__(**kwargs)

        self.student_info_input_layout = StudentInfoInputLayout(size_hint=(1, 0.75), pos_hint={'x': 0, 'y': 0.25})
        self.student_info_input_dept_bind()     # first fill the roll.
        self.student_info_input_layout.spinner_dept.bind(text=self.student_info_input_dept_bind)
        self.student_info_input_layout.text_input_rollno.readonly = True
        self.text_input_file_choose = TextInput(text='', hint_text='No file selected', readonly=True, size_hint=(0.6, 0.057), pos_hint={'x': 0.25, 'y': 0.17})
        self.file_chooser_popup = FileChooserPopup(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.file_chooser_popup.bind( on_dismiss=lambda popup_instance, *a: setattr(self.text_input_file_choose, 'text', popup_instance.text_input.text))

        self.add_widget(self.student_info_input_layout)

        self.add_widget(Label(text='Photo:', italic=True, size_hint=(0.25, 0.057), pos_hint={'x': 0, 'y': 0.17}))
        self.add_widget(self.text_input_file_choose)
        self.add_widget(Button(text='Choose', italic=True, on_release=self.file_chooser_popup.open, size_hint=(0.14, 0.057), pos_hint={'x': 0.85, 'y': 0.17}))

        self.add_widget(Button(text='Add', italic=True, on_release=self.add_new_student, size_hint=(0.45, 0.05), pos_hint={'x': 0.05, 'y': 0.075}))
        self.add_widget(Button(text='Reset', italic=True, on_release=self.reset_btn_do, size_hint=(0.45, 0.05), pos_hint={'x': 0.5, 'y': 0.075}))
        self.label_dialogue = Label(text='', italic=True, size_hint=(1, 0.075), pos_hint={'x': 0, 'y': 0})
        self.add_widget(self.label_dialogue)


    def student_info_input_dept_bind(self, *a):
        '''Set the roll according to dept.'''
        dept = self.student_info_input_layout.spinner_dept.text
        res = session.query(Student.roll_no).filter(Student.dept == dept).order_by(Student.roll_no)
        L = [x[0] for x in res]

        store = Cache.get('global_data', 'records_store')
        start = int(store.get(dept)['start'])

        next_roll = find_next_roll_to_have(L, start)
        self.student_info_input_layout.text_input_rollno.text = str(next_roll)


    def reset_btn_do(self, *a):
        self.student_info_input_layout.reset_fields()
        self.text_input_file_choose.text = ''
        self.student_info_input_dept_bind()
        self.label_dialogue.text = ''


    def add_new_student(self, *a):
        self.label_dialogue.text = ''
        inp = self.student_info_input_layout
        new_student = Student()

        def input_to_obj(input_attr, obj_attr, meta=''):
            value = getattr(inp, input_attr).text
            if value:
                setattr(new_student, obj_attr, value)
                return True
            else:
                self.label_dialogue.text = meta + " needs to be filled up !"
                return False

        if not input_to_obj('text_input_firstname', 'first_name', 'First name'): return
        if not input_to_obj('text_input_lastname', 'last_name', 'Last name'): return
        if not input_to_obj('text_input_fathersname', 'fathers_name', "Father's name"): return
        if not input_to_obj('text_input_mothersname', 'mothers_name', "Mother's name"): return
        if not input_to_obj('spinner_gender', 'gender'): return
        if not input_to_obj('spinner_bloodgroup', 'blood_group'): return

        if inp.text_input_dob_day.text != '' and inp.text_input_dob_month.text != '' and inp.text_input_dob_year.text != '':
            d = int(inp.text_input_dob_day.text)
            m = int(inp.text_input_dob_month.text)
            y = int(inp.text_input_dob_year.text)

            if is_valid_date(y, m, d):
                new_student.date_of_birth = datetime.date(year=y, month=m, day=d)
            else:
                self.label_dialogue.text = "Invalid date of birth !"
                return
        else:
            self.label_dialogue.text = "Date of birth needs to be filled up !"
            return

        if not input_to_obj('text_input_address', 'address', 'Address'): return
        if not input_to_obj('text_input_nationality', 'nationality', 'Nationality'): return

        email = inp.text_input_email_address.text
        if email:
            if is_valid_emaid(email):
                input_to_obj('text_input_email_address', 'email_address')
            else:
                self.label_dialogue.text = "Invalid email address !"
                return
        else:
            self.label_dialogue.text = "Email address needs to be filled up !"
            return

        if not input_to_obj('text_input_phone_no', 'phone_no', 'Phone no.'): return
        if not input_to_obj('text_input_ssc_roll', 'ssc_roll_no', 'SSC roll no. '): return
        if not input_to_obj('text_input_ssc_reg', 'ssc_reg_no', 'SSC reg. no.'): return
        if not input_to_obj('text_input_ssc_gpa', 'ssc_gpa', 'SSC GPA'): return
        if not input_to_obj('text_input_ssc_year', 'ssc_year', 'SSC passing year'): return
        if not input_to_obj('spinner_ssc_board', 'ssc_board'): return
        if not input_to_obj('text_input_hsc_roll', 'hsc_roll_no', 'HSC roll no.'): return
        if not input_to_obj('text_input_hsc_reg', 'hsc_reg_no', 'HSC reg. no.'): return
        if not input_to_obj('text_input_hsc_gpa', 'hsc_gpa', 'HSC GPA'): return
        if not input_to_obj('text_input_hsc_year', 'hsc_year', 'HSC passing year'): return
        if not input_to_obj('spinner_hsc_board', 'hsc_board'): return

        photo_path_from = self.text_input_file_choose.text if self.text_input_file_choose.text != '' else 'images/blank_profile_pic.jpg'
        photo_path_to = 'images/profile_pics/' + inp.spinner_dept.text + '-' + inp.text_input_rollno.text + os.path.splitext(photo_path_from)[1]
        shutil.copyfile(photo_path_from, photo_path_to)
        new_student.photo_path = photo_path_to

        if not input_to_obj('spinner_dept', 'dept'): return
        if not input_to_obj('text_input_rollno', 'roll_no'): return

        session.add(new_student)
        session.commit()
        self.reset_btn_do()
        self.label_dialogue.text = 'Student added.'


class FindTabLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(FindTabLayout, self).__init__(**kwargs)

        self.student_info_input_layout = StudentInfoInputLayout(size_hint=(0.50, 0.85), pos_hint={'x': 0, 'y': 0.15})
        self.label_query_res_count = Label(text='', italic=True, size_hint=(0.5, 0.1), pos_hint={'x': 0.5, 'y': 0.9})
        self.recycle_view = RV(size_hint=(0.5, 0.9), pos_hint={'x': 0.5, 'y': 0})

        self.blank_symbol = '--'
        inp = self.student_info_input_layout

        def spinner_modify(spinner):
            spinner.text = self.blank_symbol
            spinner.values.insert(0, self.blank_symbol)

        spinner_modify(inp.spinner_gender)
        spinner_modify(inp.spinner_bloodgroup)
        spinner_modify(inp.spinner_ssc_board)
        spinner_modify(inp.spinner_hsc_board)
        spinner_modify(inp.spinner_dept)

        self.add_widget(self.student_info_input_layout)
        self.add_widget(Button(text='Find', italic=True, on_release=self.find_btn_do, size_hint=(0.20, 0.075), pos_hint={'x': 0.05, 'y': 0.03}))
        self.add_widget(Button(text='Reset', italic=True, on_release=self.reset_btn_do, size_hint=(0.20, 0.075), pos_hint={'x': 0.25, 'y': 0.03}))
        self.add_widget(self.label_query_res_count)
        self.add_widget(self.recycle_view)


    def reset_btn_do(self, *a):
        self.student_info_input_layout.reset_fields()

        inp = self.student_info_input_layout

        inp.spinner_gender.text = self.blank_symbol
        inp.spinner_bloodgroup.text = self.blank_symbol
        inp.spinner_ssc_board.text = self.blank_symbol
        inp.spinner_hsc_board.text = self.blank_symbol
        inp.spinner_dept.text = self.blank_symbol

        self.label_query_res_count.text = ''
        if self.recycle_view in self.children:
            self.remove_widget(self.recycle_view)


    def find_btn_do(self, *a):
        inp = self.student_info_input_layout
        qry = session.query(Student)

        if inp.text_input_firstname.text:
            qry = qry.filter(Student.first_name == inp.text_input_firstname.text)

        if inp.text_input_lastname.text:
            qry = qry.filter(Student.last_name == inp.text_input_lastname.text)

        if inp.text_input_fathersname.text:
            qry = qry.filter(Student.fathers_name == inp.text_input_fathersname.text)

        if inp.text_input_mothersname.text:
            qry = qry.filter(Student.mothers_name == inp.text_input_mothersname.text)

        if inp.spinner_gender.text != self.blank_symbol:
            qry = qry.filter(Student.gender == inp.spinner_gender.text)

        if inp.spinner_bloodgroup.text != self.blank_symbol:
            qry = qry.filter(Student.blood_group == inp.spinner_bloodgroup.text)

        if inp.text_input_dob_day.text:
            qry = qry.filter(func.day(Student.date_of_birth) == int(inp.text_input_dob_day.text))

        if inp.text_input_dob_month.text:
            qry = qry.filter(func.month(Student.date_of_birth) == int(inp.text_input_dob_month.text))

        if inp.text_input_dob_year.text:
            qry = qry.filter(func.year(Student.date_of_birth) == int(inp.text_input_dob_year.text))

        if inp.text_input_address.text:
            qry = qry.filter(Student.address == inp.text_input_address.text)

        if inp.text_input_nationality.text:
            qry = qry.filter(Student.nationality == inp.text_input_nationality.text)

        if inp.text_input_email_address.text:
            qry = qry.filter(Student.email_address == inp.text_input_email_address.text)

        if inp.text_input_phone_no.text:
            qry = qry.filter(Student.phone_no == inp.text_input_phone_no.text)

        if inp.text_input_ssc_roll.text:
            qry = qry.filter(Student.ssc_roll_no == int(inp.text_input_ssc_roll.text))

        if inp.text_input_ssc_reg.text:
            qry = qry.filter(Student.ssc_reg_no == int(inp.text_input_ssc_reg.text))

        if inp.text_input_ssc_gpa.text:
            qry = qry.filter(Student.ssc_gpa == float(inp.text_input_ssc_gpa.text))

        if inp.text_input_ssc_year.text:
            qry = qry.filter(Student.ssc_year == int(inp.text_input_ssc_year.text))

        if inp.spinner_ssc_board.text != self.blank_symbol:
            qry = qry.filter(Student.ssc_board == inp.spinner_ssc_board.text)

        if inp.text_input_hsc_roll.text:
            qry = qry.filter(Student.hsc_roll_no == int(inp.text_input_hsc_roll.text))

        if inp.text_input_hsc_reg.text:
            qry = qry.filter(Student.hsc_reg_no == int(inp.text_input_hsc_reg.text))

        if inp.text_input_hsc_gpa.text:
            qry = qry.filter(Student.hsc_gpa == float(inp.text_input_hsc_gpa.text))

        if inp.text_input_hsc_year.text:
            qry = qry.filter(Student.hsc_year == int(inp.text_input_hsc_year.text))

        if inp.spinner_hsc_board.text != self.blank_symbol:
            qry = qry.filter(Student.hsc_board == inp.spinner_hsc_board.text)

        if inp.spinner_dept.text != self.blank_symbol:
            qry = qry.filter(Student.dept == inp.spinner_dept.text)

        if inp.text_input_rollno.text:
            qry = qry.filter(Student.roll_no == int(inp.text_input_rollno.text))

        self.label_query_res_count.text = str(qry.count()) + ' results found.'

        if self.recycle_view in self.children:
            self.remove_widget(self.recycle_view)

        self.recycle_view = RV(size_hint=(0.5, 0.9), pos_hint={'x': 0.5, 'y': 0})
        self.add_widget(self.recycle_view)
        self.recycle_view.set_data(student_list=qry.all())
        # print("Query result:")
        # for x in qry:
        #     print(x.first_name)
        # print(qry.count())


class HomeScreenLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(HomeScreenLayout, self).__init__(**kwargs)

        tp = TabbedPanel(do_default_tab=False)

        self.th_home = TabbedPanelHeader(text='Home', content=HomeTabLayout())
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
        store = Cache.get('global_data', 'records_store')
        curr_pw = store.get('password')['value'] if store.exists('password') else '1234'

        if self.text_input.text == curr_pw:
            self.text_input.text = ''

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


class EnrollmentSystem(App):
    def __init__(self, **kwargs):
        super(EnrollmentSystem, self).__init__(**kwargs)


    def build(self):
        return MainScreenManager()


def main():
    Cache.register('global_data')

    Cache.append('global_data', 'records_store', JsonStore('others/records.txt'))

    # password: value
    # CSE: start
    # ECE: start
    # BBA: start

    app = EnrollmentSystem()
    app.run()


if __name__ == '__main__':
    main()