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
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print(((magnitude),))
    time.sleep(0.1)
    cp.pixels[0] = (0, int(magnitude), 0)
    cp.pixels[1] = (0, 0, int(cp.light))