from rgbled import RgbLed
import time as sys_time
from datetime import datetime, time
import colorsys
from collections import deque


TIME_KEY = 0
HUE_KEY = 1
alarm_colors = [
    (time(6), (0, 1, 0)),

    (time(6, 49, 55), (0.25, 1, 0)),
    (time(6, 50), (0.5, 1, 0)),

    (time(7, 14, 55), (0.75, 0.75, 0)),
    (time(7, 15), (1, 0.5, 0)),

    (time(7, 29, 55), (1, 0.25, 0)),
    (time(7, 30), (1, 0, 0)),

    (time(8), (0, 0, 0))
]
led = RgbLed()


def translate_triple(triple_one, triple_two, percent):
    translate = lambda i: triple_one[i] + percent * (triple_two[i] - triple_one[i])
    one = translate(0)
    two = translate(1)
    three = translate(2)
    return one, two, three


def diff_time(time_one, time_two):
    h = time_one.hour - time_two.hour
    m = time_one.minute - time_two.minute
    s = time_one.second - time_two.second
    ms = time_one.microsecond - time_two.microsecond
    return float(h * 60 * 60 + m * 60 + s + ms * .000001)


try:
    while True:
        adeque = deque(alarm_colors)
        curtime = datetime.now().time()
        last_mapping = (time(0), (0, 0, 0))
        # Find the two times surrounding the current time in our time:color map,
        # then set LED color to appropriate point in HSV gradient between the two
        while len(adeque) > 0:
            pop = adeque.popleft()
            if curtime < pop[0]:
                # Found current time
                diff = float(diff_time(pop[0], last_mapping[0]))
                raw_progress = float(diff_time(curtime, last_mapping[0]))
                cross_fade_ratio = raw_progress / diff
                start_color = colorsys.rgb_to_hsv(*list(last_mapping[HUE_KEY]))
                end_color = colorsys.rgb_to_hsv(*list(pop[HUE_KEY]))
                # Calculate current color
                cur_color = translate_triple(start_color, end_color, cross_fade_ratio)
                # print('diff:' + str(diff) + ' raw:' + str(raw_progress) + ' cross:' + str(cross_fade_ratio) + ' start:' + str(start_color) + ' end:' + str(end_color) + ' cur:' + str(cur_color))
                led.hsv(*cur_color)
                break
            else:
                last_mapping = pop
        sys_time.sleep(0.1)

except KeyboardInterrupt:
    led.pi.stop()



