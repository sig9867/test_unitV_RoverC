"""
https://github.com/m5stack/M5-ProductExampleCodes/blob/master/App/UnitV/track_ball/track_ball.py
"""
import sensor
import image
from machine import UART
from fpioa_manager import fm
import json
import time
from modules import ws2812

class Led:
    def __init__(self):
        self.w = ws2812(8, 100)
    def set(self, r, g, b):
        self.w.set_led(0, (r, g, b))
        self.w.display()

led = Led()

fm.register(34,fm.fpioa.UART1_TX)   # GPIO34 -- UART1_TX
fm.register(35,fm.fpioa.UART1_RX)   # GPIO35 -- UART1_RX
uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)

# 赤のballを検出
target_lab_threshold = (10, 72, 32, 68, -14, 47)

while True:
    img = sensor.snapshot()
    blobs = img.find_blobs([target_lab_threshold], x_stride = 2, y_stride = 2, pixels_threshold = 400, merge = True, margin = 10)
    data = {'x': 0, 'y': 0, 'xw': 0, 'yw': 0, 'area': 0}
    if blobs:
        areas = [b.area() for b in blobs]
        idx = areas.index(max(areas))
        target = blobs[idx]
        data = {'y': 120 - target[6], 'x': target[5] - 160, 'xw': target[2], 'yw': target[3], 'area': target.area()}
        _ = img.draw_rectangle(target[0:4])
        _ = img.draw_cross(target[5], target[6])
        #img.get_pixel(target[5], target[6])
    uart.write(json.dumps(data) + '\r\n')
    print(data)
    #b = min(data['area'] // 200, 20)
    b = 8
    led.set(b, b, b) if data['area'] == 0 else led.set(b, 0, 0)

