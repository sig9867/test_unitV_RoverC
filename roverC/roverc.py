import hat

class RoverC:
    def __init__(self):
        self.rv = hat.get(hat.ROVERC)
    
    def move(self, v):
        print(v)
        self.rv.SetAllPulse(v[0], v[1], v[2], v[3])
    
    def stop(self):
        self.move([0, 0, 0, 0])

def get_controll_speed(x, xwidth, method='turn'):
    x_target = 0
    xwidth_target = 120
    K = 1.0
    v = int(K * (xwidth_target - xwidth))
    K = 0.4
    theta = int(K * ( x_target - x))
    v_plus = min(v + theta, 99)
    v_plus = max(v_plus, -99)
    v_minus = min(v - theta, 99)
    v_minus = max(v_minus, -99)
    if method == 'shift':
        return [v_plus, v_minus, v_minus, v_plus]
    return [v_plus, v_minus, v_plus, v_minus]
