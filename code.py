# ESP01 Sensor
# Light, Sound, Temperature

import array
import math
import time
 
import audiobusio
import board


from adafruit_circuitplayground import cp

def mean(values):
    return sum(values) / len(values)
 
 
def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
 
    return math.sqrt(sum_of_samples / len(values))
 
 
mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))

while True:
    time.sleep(0.1)
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    cp.pixels[0] = (0, int(magnitude), 0) # sound sensor
    cp.pixels[1] = (0, 0, int(cp.light)) # light sensor
    cp.pixels[2] = (int(cp.temperature), 0, 0)
    if cp.switch:
        cp.pixels[3] = (int(cp.light) * int(magnitude), int(cp.temperature) * int(cp.light), int(magnitude) * int(cp.temperature))
    if cp.shake(shake_threshold=20):
        print("Shake detected!")
        cp.red_led = True
        cp.pixels[3] = (255, 255, 0)
        time.sleep(15)
    else:
        cp.red_led = False
        cp.pixels[3] = (0, 0, 0)
    x, y, z = cp.acceleration
    cp.pixels[4] = (int(x), int(y), int(z))
    cp.pixels[5] = (int(magnitude), int(cp.light), int(cp.temperature))
    cp.pixels[6] = (31, 31, 31)
    cp.pixels[7] = (63, 63, 63)
    cp.pixels[8] = (127, 127, 127)
    cp.pixels[9] = (255, 255, 255)
    # print("Slide switch:", cp.switch)