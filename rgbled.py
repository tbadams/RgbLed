import time
import colorsys
import pigpio

PIGPIO_MAX = 255.0


class RgbLed(object):
    def __init__(self, red_gpio=16, green_gpio=20, blue_gpio=21, max_val=1.0):
        self.pi = pigpio.pi()
        self.red = red_gpio
        self.green = green_gpio
        self.blue = blue_gpio
        self.max = max_val

    def __del__(self):
        self.pi.stop()

    def r(self, value):
        """Set the red LED level to the specified value."""
        self.pi.set_PWM_dutycycle(self.red, value * (PIGPIO_MAX / self.max))

    def g(self, value):
        """Set the green LED level to the specified value."""
        self.pi.set_PWM_dutycycle(self.green, value * (PIGPIO_MAX / self.max))

    def b(self, value):
        """Set the blue LED level to the specified value."""
        self.pi.set_PWM_dutycycle(self.blue, value * (PIGPIO_MAX / self.max))

    def rgb(self, r=0.0, g=0.0, b=0.0):
        """Set the RGB LED to the RGB color specified."""
        self.r(r)
        self.g(g)
        self.b(b)

    def w(self, value):
        """Set the LED to white with a brightness specified by the given value"""
        self.rgb(value, value, value)

    def hsv(self, h, s=1.0, v=1.0):
        """Sets the LED to the color specified by the hue, saturation and value parameters.
        's' and 'v' must be between 0 and 1, while h will be interpreted as a value between 0 and self.max."""
        h /= self.max  # Normalize
        normalized_rgb = list(colorsys.hsv_to_rgb(h, s, v))
        in_rgb = [i * self.max for i in normalized_rgb]
        self.rgb(*list(in_rgb))

    def hue_rotate(self, period=4):
        RUNNING = True
        try:
            while RUNNING:
                for x in range(0, 1000):
                    self.hsv((x / 1000.0) * self.max)
                    time.sleep((period * 1.0) / 1000)
        except KeyboardInterrupt:
            RUNNING = False

    def hue_transit(self, start=0, end=1.0, duration=4):
        diff = end - start
        for x in range(0, 1000):
            self.hsv(start + (x / 1000.0) * diff)
            time.sleep(duration / 1000.0)


