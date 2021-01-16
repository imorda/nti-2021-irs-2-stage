if bool(0):
    from TRIK import *
import math


TRIK = False


class Robot:  # константы
    wheelD = 5.6
    track = 17.5
    cpr = 360 if not TRIK else 385
    v = 80
    vstart = 30
    acceleration = 20  # points per second
    gyro_kp = 0.002  # П коэффиент для езды по гироскопу
    kp = 0.05  # П/ПИД регулятор коэффициент
    ki = 0.04  # И/ПИД регулятор коэффициент
    kd = 0.03  # Д/ПИД регулятор коэффициент
    pid_window_size = 10
    decel_start_offset = 35  # расстояние до начала замедления


class Data:  # одометрия
    cur_angle = 0
    pid_error_deque = [0.0 for i in range(Robot.pid_window_size)]
    pid_deque_index = -1


# Shortcut methods
mL = brick.motor('M4').setPower
mR = brick.motor('M3').setPower
eL = brick.encoder('E4').read
eR = brick.encoder('E3').read
sF = brick.sensor('D1').read
# sL = brick.sensor('A2').read
pi = math.pi
sleep = script.wait
time = script.time


# Base methods
sign = lambda x: -1 if x < 0 else 1
getYaw = lambda: brick.gyroscope().read()[6]


def motors(vL=None, vR=None):
    vL = Robot.v if vL == None else vL
    vR = vL if vR == None else vR
    mL(vL)
    mR(vR)


def gyro_calibrate(N = -1):
    if N == -1:
        N = 10000 if TRIK else 2000
    brick.gyroscope().calibrate(N)
    script.wait(N + 1000)


def forward_gyro(cm = 52.5):
    path = (cm / (pi * Robot.wheelD)) * Robot.cpr
    path = path + eL()  # Add start encoder value
    start_time = time()
    sgn = sign(cm)
    decel_offset = (Robot.decel_start_offset / (pi * Robot.wheelD)) * Robot.cpr
    decel_start = None
    flag = 0 if eL() < path else 1
    while [eL(), path][flag] < [path, eL()][flag]:
        power_delta = Robot.acceleration * ((time() - start_time) / 1000)
        power_accel = min(Robot.vstart + power_delta, Robot.v)
        power_decel = Robot.v
        if decel_start is not None:
            power_delta_decel = Robot.acceleration * ((time() - decel_start) / 1000)
            power_decel = max(Robot.vstart, Robot.v - power_delta_decel)
        power = min(power_accel, power_decel)
        if path - eL() < decel_offset and decel_start is None:
            decel_start = time()
        error = Data.cur_angle - getYaw()  # Proportional steering
        correction = error * Robot.gyro_kp
        motors(max(0, min(power + correction * sgn, 100)) * sgn, max(0, min(power - correction * sgn, 100)) * sgn)
        # print(power)
        sleep(10)
    motors(0)
    # print(time() - decel_start)  # print the deceleration actual time after simulation


def rotate_gyro_absolute(angle):
    """
    Rotates robot to a given value (NOTE: accepts values from -180 to 180 degrees!!!)
    """
    if not TRIK:
        forward_gyro(5)
    if abs(angle) < 200:
        angle *= 1000
    Data.cur_angle = angle
    sgn = sign(angle - getYaw())
    if abs(angle - getYaw()) >= 180000:
        sgn *= -1
    motors((Robot.v//2) * sgn, (Robot.v//-2) * sgn)
    while abs(angle - getYaw()) > 3000:
        sleep(10)
    motors(0)
    if not TRIK:
        forward_gyro(-5)
    print('Rotate', angle, 'done!')


def rotate_gyro_relative(angle):
    angle *= 1000
    rotate_gyro_absolute(((Data.cur_angle + angle + 180000) % 360000) - 180000)
    print('Rotate', angle, '(relative) done!')


def pid_controller(value: float, setpoint: float) -> float:
    """
    Calculates PID correction
    :param value: current sensor value
    :param setpoint: target sensor value
    :return: correction value
    """
    err = value - setpoint
    Data.pid_deque_index = (Data.pid_deque_index + 1) % Robot.pid_window_size
    Data.pid_error_deque[Data.pid_deque_index] = err
    P = err * Robot.kp
    I = sum(Data.pid_error_deque) / 10 * Robot.ki
    D = (Data.pid_error_deque[Data.pid_deque_index] - Data.pid_error_deque[
        (Data.pid_deque_index + Robot.pid_window_size + 1) % Robot.pid_window_size]) * Robot.kd
    return P + I + D


def pid_correction_to_motors(base_speed: int, correction: float) -> None:
    """
    Runs motor based on calculated PID correction
    :param base_speed: default speed
    :param correction: PID correction value
    :return:
    """
    motors(min(max(base_speed * (1-correction), 10), 100), min(max(base_speed * (1+correction), 10), 100))


# Main code
def main():
    print('Start')
    rotate_gyro_relative(-90)
    forward_gyro(50)
    rotate_gyro_relative(90)
    while True:
        pid_correction_to_motors(Robot.v, pid_controller(sF(), 20.0))
        sleep(2)


if __name__ == '__main__':
    gyro_calibrate()
    main()
