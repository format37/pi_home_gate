import RPi.GPIO as GPIO
from time import sleep
import requests
import datetime
import picamera
import time
from lex import send_to_telegram

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN)
laststate='0'
newstate='0'
filepath = 'photo.jpg'
group='-1001382003751'

def callBackRising(channel):
	global newstate
	newstate	= str(GPIO.input(12))	

send_to_telegram(group,'monitoring started')

GPIO.add_event_detect(12, GPIO.RISING, callback=callBackRising, bouncetime=300)

with picamera.PiCamera() as camera:
	#camera.resolution = (2592, 1944)#max camera resolution
	camera.resolution = (1280, 1280)#telegram fast photo size
	camera.rotation= 270
	camera.start_preview()
	try:
		while True:								
			if newstate!=laststate:
				laststate=newstate
				camera.capture(filepath)
				dt=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				if newstate=='0':
					doorState='close'
				else:
					doorState='open'				
				with open(filepath,'rb') as fh:
					#photo
					mydata = fh.read()
					headers_data={"Origin":"http://scriptlab.net","Referer":"http://scriptlab.net/telegram/bots/relaybot/",'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
					response = requests.put('http://scriptlab.net/telegram/bots/relaybot/relayPhotoViaPut.php',data=mydata,headers=headers_data,params={'file': filepath})
					
					send_to_telegram(group,dt+' '+doorState)

			sleep(2)
				
	except KeyboardInterrupt:
		GPIO.cleanup()
		send_to_telegram(group,'monitoring stopped')

send_to_telegram(group,'monitoring exit')