import kivy
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, WipeTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem
from validate_email import validate_email
import speech_recognition as sr
from email.message import EmailMessage
from kivy.graphics import *
from kivy.clock import Clock
import smtplib
import pyttsx3
from kivy.core.window import Window
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
from datetime import datetime
import asyncio
from kivy.app import async_runTouchApp
from kivymd.uix.card import MDCardSwipe
from kivy.properties import StringProperty
import re
import helper

listener = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except:
        pass


email_list = {
    'dude': 'COOL_DUDE_EMAIL',
    'bts': 'diamond@bts.com',
    'pink': 'jennie@blackpink.com',
    'lisa': 'lisa@blackpink.com',
    'irene': 'irene@redvelvet.com',
}


class LoginScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class AnimScreen(Screen):
    pass


class WelcomeScreen(Screen):
    pass


class MailScreen(Screen):
    pass


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()


sm = ScreenManager(transition=FadeTransition())
sm.add_widget(LoginScreen(name='loginscreen'))
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(MailScreen(name='mailscreen'))
sm.add_widget(AnimScreen(name='animscreen'))
sm.add_widget(SignupScreen(name='signupscreen'))


class DemoApp(MDApp):

    def __init__(self):
        super().__init__()
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.client['Signup']
        self.collection = self.mydb.User_Information

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.string = Builder.load_string(helper.help_str)
        self.string.get_screen('loginscreen').ids.login_email.bind(
            on_text_validate=self.login,
            on_focus=self.login,
        )
        return self.string

    def signup(self):

        FIRSTNAME = self.string.get_screen('signupscreen').ids.firstname.text
        LASTNAME = self.string.get_screen('signupscreen').ids.lastname.text
        EMAIL = self.string.get_screen('signupscreen').ids.email.text
        PASSWORD = self.string.get_screen('signupscreen').ids.password.text

        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

        if FIRSTNAME.isalpha() and len(FIRSTNAME) > 1:
            if LASTNAME.isalpha() and len(LASTNAME) > 1:
                if (re.search(regex, EMAIL)):
                    l, u, p, d = 0, 0, 0, 0
                    if (len(PASSWORD) >= 8):
                        for i in PASSWORD:

                            if (i.islower()):
                                l += 1

                            if (i.isupper()):
                                u += 1

                            if (i.isdigit()):
                                d += 1

                            if (i == '@' or i == '$' or i == '_'):
                                p += 1
                    if (l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(PASSWORD)):
                        record = {
                            'firstname': FIRSTNAME,
                            'lastname': LASTNAME,
                            'email': EMAIL,
                            'password': PASSWORD,
                            'date': datetime.now(),
                            'mail-log': []
                        }

                        result = self.collection.insert_one(record)
                        self.string.get_screen('loginscreen').manager.current = 'loginscreen'
                    else:
                        cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                        self.dialog = MDDialog(title='Invalid input', text='Please enter a valid password',
                                               buttons=[cancel_btn])
                        self.dialog.open()
                else:
                    cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                    self.dialog = MDDialog(title='Invalid input', text='Please enter a valid email',
                                           buttons=[cancel_btn])
                    self.dialog.open()
            else:
                cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid input', text='Please enter a valid name',
                                       buttons=[cancel_btn])
                self.dialog.open()
        else:
            cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid input', text='Please enter a valid name',
                                   buttons=[cancel_btn])
            self.dialog.open()

    def animate(self, *args):
        with self.string.get_screen('animscreen').ids.anim_info.canvas:
            Color(0, 0, 0)
            self.line = Line(points=(280, 250, 330, 250), width=10)
        ani = Animation(points=(470, 250, 510, 250))
        ani += Animation(points=(280, 250, 330, 250), duration=1.5)
        ani.repeat = True
        ani.start(self.line)
        Clock.schedule_once(self.login, 5)

    def login(self, *args):
        loginEmail = self.string.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.string.get_screen('loginscreen').ids.login_password.text
        firstname = self.collection.find_one({'email': loginEmail}, {'firstname': 1})
        lastname = self.collection.find_one({'email': loginEmail}, {'lastname': 1})
        user_found = self.collection.find_one({"email": loginEmail})
        if user_found:
            if loginPassword == user_found['password']:
                print("Login Success!")
                self.on_start()
                self.string.get_screen(
                    'welcomescreen').ids.fullname.text = f"{firstname['firstname']} {lastname['lastname']}"
                self.string.get_screen('welcomescreen').ids.email_id.text = f"{loginEmail}"
                self.string.get_screen('welcomescreen').manager.current = 'welcomescreen'
                self.string.get_screen('welcomescreen').ids.username_info.text = f"Welcome {loginEmail}"

            else:
                print("Wrong Password")
                Animation.stop_all(self.line)
                cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Wrong Password', text='Please enter a valid password',
                                       buttons=[cancel_btn])
                self.string.get_screen('loginscreen').manager.current = 'loginscreen'
                self.dialog.open()

        else:
            print("User not found")
            cancel_btn = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='User not found', text='Please enter a registered email',
                                   buttons=[cancel_btn])
            self.string.get_screen('loginscreen').manager.current = 'loginscreen'
            self.dialog.open()

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def send_email(self, receiver, subject, message):

        CLIENT_SECRET_FILE = '''Your Client Secret file'''
        API_NAME = 'gmail'
        API_VERSION = 'v1'
        SCOPES = ['https://mail.google.com/']
        email = self.string.get_screen('loginscreen').ids.login_email.text
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        emailMsg = message
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = receiver
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)

        self.collection.update_one({'email': email},
                                   {'$push': {
                                       'mail-log': {'receiver': receiver, 'subject': subject, 'message': emailMsg,
                                                    'time': datetime.now()}}})

        '''
        loginEmail = self.string.get_screen('loginscreen').ids.login_email.text
        loginPassword = self.string.get_screen('loginscreen').ids.login_password.text
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(loginEmail, loginPassword)
        email = EmailMessage()
        email['From'] = loginEmail
        email['To'] = receiver
        email['Subject'] = subject
        email.set_content(message)
        server.send_message(email)
        '''

    def back(self):
        self.string.get_screen('welcomescreen').manager.current = 'welcomescreen'

    def remove_item(self, instance):
        self.string.get_screen('mailscreen').ids.md_list.remove_widget(instance)

    def on_start(self):
        email = self.string.get_screen('loginscreen').ids.login_email.text
        rec = self.collection.find_one({'email': email}, {'mail-log.receiver': 1})
        sub = self.collection.find_one({'email': email}, {'mail-log.subject': 1})
        text = self.collection.find_one({'email': email}, {'mail-log.message': 1})

        recList = []
        subList = []
        textList = []

        if rec is not None:
            for value in rec['mail-log']:
                list1 = list(value.values())
                recList.extend(list1)

        if sub is not None:
            for value in sub['mail-log']:
                list2 = list(value.values())
                subList.extend(list2)

        if text is not None:
            for value in text['mail-log']:
                list3 = list(value.values())
                textList.extend(list3)

        for i in range(len(recList)):
            for j in range(len(subList)):
                for k in range(len(textList)):
                    if i == j == k:
                        self.string.get_screen('mailscreen').ids.md_list.add_widget(
                            SwipeToDeleteItem(text=f"To: {recList[i]}",
                                              secondary_text=f"{subList[j]}",
                                              tertiary_text=f"{textList[k]}")
                        )

    def call(self, *args):
        asyncio.run(self.get_email_info())

    async def nested1(self, receiver):

        self.string.get_screen('welcomescreen').ids.receiver_info.text = f"To {receiver}"

    async def nested2(self, subject):

        self.string.get_screen('welcomescreen').ids.subject_info.text = f"Subject {subject}"

    async def nested3(self, message):

        self.string.get_screen('welcomescreen').ids.message_info.text = f"Text {message}"

    def get_email_info(self, *args):
        talk('To Whom you want to send email')
        name = get_info()
        receiver = email_list[name]
        print(receiver)
        talk('What is the subject of your email?')
        subject = get_info()
        talk('Tell me the text in your email')
        message = get_info()
        self.send_email(receiver, subject, message)
        talk('Hey. Your email is sent')


DemoApp().run()
