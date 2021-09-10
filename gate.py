import RPi.GPIO as GPIO
from time import sleep
import datetime
import subprocess
import picamera
import requests
import os
import urllib

camera = picamera.PiCamera()
#camera.resolution = (2592, 1944)#max camera resolution
camera.resolution = (1280, 1280)#telegram fast photo size
camera.rotation= 270

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
laststate='0'
newstate='0'


def callBackRising(channel):
    global newstate
    newstate = str(GPIO.input(12))


def send_photo_from_local_file_to_telegram(photo_path):
    token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.environ.get('TELEGRAM_CHAT', '')
    session = requests.Session()
    get_request = 'https://api.telegram.org/bot' + token
    get_request += '/sendPhoto?chat_id=' + chat_id
    files = {'photo': open(photo_path, 'rb')}
    session.post(get_request, files=files)


def send_to_telegram(message):
	token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
	chat_id = os.environ.get('TELEGRAM_CHAT', '')
	session = requests.Session()
	get_request = 'https://api.telegram.org/bot' + token	
	get_request += '/sendMessage?chat_id=' + chat_id
	get_request += '&text=' + urllib.parse.quote_plus(message)
	session.get(get_request)


def take_photo(camera):
    camera.start_preview()
    #time.sleep(2)
    camera.capture('/home/pi/photo.jpg')
    camera.stop_preview()


send_to_telegram(str(datetime.datetime.now())+' monitoring started')

GPIO.add_event_detect(12, GPIO.RISING, callback=callBackRising, bouncetime=300)

while True:
    if newstate!=laststate:
        print('new state:', newstate)
        laststate=newstate
        #dt=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        #print(dt, 'capturing')
        #result = subprocess.Popen('python', script_path+'cam.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #stdout, stderr = result.communicate()
        take_photo(camera)
        #print(stdout.decode('utf-8'))
        if newstate=='0':
            doorState='close'
        else:
            doorState='open'
        #with open('/home/pi/photo.jpg','rb') as photo:
        #bot.send_photo(chat_id, photo, dt+' '+doorState)
        send_photo_from_local_file_to_telegram('/home/pi/photo.jpg')
        #print('waiting 2s..')
        sleep(2)
