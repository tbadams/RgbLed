import RPIO as GPIO
import time
import colorsys

# http://www.instructables.com/id/Raspberry-Pi-3-RGB-LED-With-Using-PWM/

GPIO.setmode(GPIO.BCM)
RUNNING = True

# Setup pins
green = 20
red = 16
blue = 21
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

#Configure PWM
Freq = 100
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)
RED.start(50)
GREEN.start(50)
BLUE.start(50)


def hsv(h, s, v):
    normalized_hsv = list(colorsys.hsv_to_rgb(h, s, v))
    normalized_hsv = tuple(int(i * 100) for i in normalized_hsv)
    return rgb(*list(normalized_hsv))


def rgb(r, g, b):
    RED.ChangeDutyCycle(100 - r)
    GREEN.ChangeDutyCycle(100 - g)
    BLUE.ChangeDutyCycle(100 - b)


def hue_rotate(period = 4):
    RUNNING = True
    try:
        while RUNNING:
            for x in range(0, 1000):
                hsv(x/1000.0, 1, 1)
                time.sleep((period * 1.0)/1000)
    except KeyboardInterrupt:
        RUNNING = False
        GPIO.cleanup()


def hue_transit(start = 0, end = 1.0, duration = 4):
    diff = end - start
    for x in range(0, 1000):
        hsv(start + (x / 1000.0) * diff, 1, 1)
        time.sleep(duration/1000.0)

