# Alarm-System-PI
 An alarm system that when motion is detected it messages you on slack

### Py Library Requirements:

	pip install RPi.GPIO
	pip install mfrc522

### Electronics:

- IR Motion Sensor
- 4 LEDs
- 2 GPIO Buttons

### Setup:
**(GPIO pins are in board mode)**

- Green Light Pin: 40
- Blue Light Pin: 31
- Yellow Light Pin: 16
- Red Light Pin: 12
- Yellow Button Pin: 37
- Sensor Data Pin: 11

**You might need to adjust the IR Sensor Sensitivity and Time Delay**

**Make sure you create a slack webhook**

### How To Use:

- Green Button: Starts a timer so you have time to leave the area
- Yellow Button: Toggles the alarm on and off

### What I Used:

- Raspberry Pi 4
- PIR Sensor Model #: HC-SR501
- Buttons are simple press buttons
- The Lights are simple LED lights