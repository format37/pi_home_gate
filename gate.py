import RPi.GPIO as GPIO
from time import sleep
import datetime
import telebot
import subprocess

script_path = '/home/pi/projects/gate/'

with open(script_path+'token.key','r') as file:
        API_TOKEN=file.read().replace('\n', '')
        file.close()
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
laststate='0'
newstate='0'
chat_id='-1001382003751'

def callBackRising(channel):
        global newstate
        newstate        = str(GPIO.input(12))

dt=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
bot.send_message(chat_id, dt+' monitoring started')

GPIO.add_event_detect(12, GPIO.RISING, callback=callBackRising, bouncetime=300)

while True:
    if newstate!=laststate:
        print('new state:', newstate)
        laststate=newstate
        dt=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(dt, 'capturing')
        result = subprocess.Popen(['python', script_path+'cam.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
        print(stdout.decode('utf-8'))
        if newstate=='0':
            doorState='close'
        else:
            doorState='open'
        with open(script_path+'photo.jpg','rb') as photo:
            bot.send_photo(chat_id, photo, dt+' '+doorState)
        print('waiting 2s..')
        sleep(2)

bot.send_message(chat_id, dt+' monitoring exit')
