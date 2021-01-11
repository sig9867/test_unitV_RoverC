from m5stack import lcd, btnA
from m5ui import M5TextBox, setScreenColor
from uiflow import wait_ms
import json
import utime
import machine
from roverc import get_controll_speed, RoverC

class AppBase:
    def __init__(self):
        self.uart = machine.UART(1, tx=32, rx=33)
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.reqClose = False
    
    def run(self):
        while not self.reqClose:
            d = self.get_from_uart()
            self.state_machine(d)
            self.display(d)
            self.checkClose()
        self.onClose()
    
    def get_from_uart(self):
        pass
    
    def state_machine(self, d):
        pass
    
    def display(self, d):
        pass
    
    def onClose(self):
        pass

    def checkClose(self):
        pass

setScreenColor(0x111111)
label0 = M5TextBox(17, 53, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)


class RoverApp(AppBase):
    def __init__(self):
        super().__init__()
        self.state = 'init'
        self.rv = RoverC()
        self.pre_x = 0

    def get_from_uart(self):
        while True:
            if self.uart.any():
                s = self.uart.readline()
                try:
                    d = json.loads(s)
                    assert(len(list(d.keys())) == 5)
                    return d
                except:
                    pass
    def state_machine(self, d):
        print(self.state)
        if self.ball_exist(d):
            self.state = 'servo'
            self.servo(d)
            self.pre_x = d['x']
            return
        if self.state == 'init':
            self.tstart = utime.ticks_ms()
            self.state = 'init_waiting'
            return
        if self.state == 'init_waiting':
            if utime.ticks_ms() - self.tstart > 200:
                self.state = 'turn_right' if self.pre_x < 0 else 'turn_left'
            return
        if self.state == 'turn_right' or self.state == 'turn_left':
            v = 26
            self.rv.move([v, -v, v, -v]) if self.state == 'turn_right' else self.rv.move([-v, v, -v, v])
            return
        if self.state == 'servo':
            self.state = 'init'
        
    
    def ball_exist(self, d):
        return d['area'] > 0
    
    def servo(self, d):
        v = get_controll_speed(d['x'], d['xw'], method='shift')
        self.rv.move(v)
    
    def checkClose(self):
        self.reqClose = btnA.wasPressed()

    def onClose(self):
        self.rv.stop()
    
    def display(self, d):
        label0.setText(str(d))

        #print(d)


if __name__ == '__main__':
    RoverApp().run()

"""

setScreenColor(0x111111)
label0 = M5TextBox(17, 53, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)

uart1 = machine.UART(1, tx=32, rx=33)
uart1.init(115200, bits=8, parity=None, stop=1)
while True:
    if uart1.any():
        s = uart1.readline()
        label0.setText(s)
        try:
            d = json.loads(s)
            assert(len(list(d.keys())) == 5)
        except:
            print(s)
            break
        #wait_ms(10)
        print(get_controll_speed(d['x'], d['xw']))
        
"""