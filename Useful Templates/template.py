if bool(0):
    from TRIK import *

TRIK = False


class Robot:  # константы
    wheelD = 5.6
    track = 17.5
    cpr = 360 if not TRIK else 385
    v = 80
    vstart = 30
    acceleration = 20  # points per second
    kp = 0.002  # П регулятор
    decel_start_offset = 35  # расстояние до начала замедления


class Data:  # одометрия
    cur_angle = 0
