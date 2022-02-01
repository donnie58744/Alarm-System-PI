from os import system
import RPi.GPIO as GPIO
import time
import sys
import json
import requests
from threading import Thread

thread_running = True

greenLight = 40
yellowLight = 16
blueLight = 31
redLight = 12

greenBtn = 35
yellowBtn = 37

sensorPin = 11

trigger = False
active = True
count = 0

webhook_url = "YOUR_WEBHOOK_URL"


def setup():
    GPIO.setmode(GPIO.BOARD)
    
    #setup lights
    GPIO.setup(greenLight, GPIO.OUT)
    GPIO.setup(yellowLight, GPIO.OUT)
    GPIO.setup(blueLight, GPIO.OUT)
    GPIO.setup(redLight, GPIO.OUT)

    GPIO.output(greenLight, GPIO.LOW)
    GPIO.output(yellowLight, GPIO.LOW)
    GPIO.output(blueLight, GPIO.LOW)
    GPIO.output(redLight, GPIO.LOW)
    
    GPIO.setup(greenBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(yellowBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(sensorPin, GPIO.IN)

def loop():
    global active
    global thread_running
    while thread_running: 
        if GPIO.input(greenBtn)==GPIO.LOW:
            # Turn Off Lights
            GPIO.output(greenLight, GPIO.LOW)
            GPIO.output(yellowLight, GPIO.LOW)
            GPIO.output(blueLight, GPIO.LOW)
            GPIO.output(redLight, GPIO.LOW)
            
            # Turn On Lights
            GPIO.output(greenLight, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.output(yellowLight, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.output(blueLight, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.output(redLight, GPIO.HIGH)
            time.sleep(1.5)
            GPIO.output(greenLight, GPIO.LOW)
            time.sleep(1.5)
            GPIO.output(yellowLight, GPIO.LOW)
            time.sleep(1.5)
            GPIO.output(blueLight, GPIO.LOW)
            time.sleep(1.5)
            GPIO.output(redLight, GPIO.LOW)

            active = True
            
        if GPIO.input(yellowBtn) == GPIO.LOW:
            GPIO.output(yellowLight, GPIO.HIGH)
            
            global count
            
            count +=1
            
            active = False
            
            if count == 2:
                active = True
                GPIO.output(yellowLight, GPIO.LOW)
                count = 0
            
        sensor()

def command():
    global thread_running
    
    while True:
        userInput = input()

        if (userInput == 'stop'):
            print('STOPING')
            thread_running = False
            exit()
        elif (userInput == 'login'):
            # Check user login
            print('Username:')
            username = input()
            print('Password:')
            password = input()
            print(username + '|' + password)
            
            
def sensor():
    if GPIO.input(sensorPin)==GPIO.HIGH and active == True:
        GPIO.output(redLight,GPIO.HIGH)
        
        slack_data = {'text': "INTRUDER!"}
        response = requests.post(
            webhook_url, data =json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        
        time.sleep(3)
        
        GPIO.output(redLight, GPIO.LOW)

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        t1 = Thread(target=loop)
        t2 = Thread(target=command)

        t1.start()
        t2.start()
        
        t2.join()
        
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()