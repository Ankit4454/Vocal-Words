#!/usr/bin/env python
# coding: utf-8

# In[2]:


import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
import os
import smtplib
import imghdr
from email.message import EmailMessage


    
# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"kiri: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file
    
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['kanteliyaankit@gmail.com', 'kanteliyaankit@gmail.com']

msg = EmailMessage()


        

msg['From'] = EMAIL_ADDRESS
msg['To'] = 'kanteliyaankit@gmail.com'

r = sr.Recognizer()
with sr.Microphone() as source:
    speak("speak subject :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        msg['Subject'] = text
    except:
        print("Sorry could not recognize what you said")
    speak("speak message :")
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        msg.set_content(text)
    except:
        print("Sorry could not recognize what you said")






with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)    
    



  

