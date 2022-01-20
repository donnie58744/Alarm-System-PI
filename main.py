import RPi.GPIO as GPIO
import time
import sys
import json
import requests

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
    while True: 
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
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
