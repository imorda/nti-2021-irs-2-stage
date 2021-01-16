if bool(0):
    from TRIK import *
import math
from threading import Thread


TRIK = False


class Robot:  # константы
    cell_size = 35
    wheel_d = 5.6
    track = 15.4
    cpr = 360 if not TRIK else 385
    v = 80
    vstart = 30
    acceleration = 20  # points per second
    pid_window_size = 10
    decel_start_offset = 35  # расстояние до начала замедления
    maze_size = 16

    directions = [
        [(1, 0), (-1, 0)],
        [(0, 1), (0, -1)]
    ]


class Data:  # одометрия
    cur_angle = 0
    pid_error_deque = [0.0 for i in range(Robot.pid_window_size)]
    pid_deque_index = -1
    field = [[-1 for _ in range(Robot.maze_size * 2 + 1)] for _ in range(Robot.maze_size * 2 + 1)]
    robot_pos = (Robot.maze_size, Robot.maze_size)
    borders = [1, 1, len(field)-2, len(field[0])-2]
    encL = 0
    encR = 0
    min_robot_pos = (Robot.maze_size, Robot.maze_size)
    max_robot_pos = (Robot.maze_size, Robot.maze_size)
    finish = False

# -1 - неизвестная клетка
#  0 - пустота
#  1 - препятствие
#  2 - граница поля


# Shortcut methods
mL = brick.motor('M4').setPower
mR = brick.motor('M3').setPower
eL = brick.encoder('E4').read
eR = brick.encoder('E3').read
sF = brick.sensor('D1').read
sB = brick.sensor('D2').read
sL = brick.sensor('A1').read
sR = brick.sensor('A2').read
pi = math.pi
sleep = script.wait
time = script.time


# Base methods
sign = lambda x: -1 if x < 0 else 1
getYaw = lambda: brick.gyroscope().read()[6]


class SpiralGenerator:
    def __init__(self, size):
        self.dir = 1
        self.size = size
        self.iter_lim = size * size
        self.iteration = 0
        self.start_dir = (0, 0)
        self.cur = (0, -1)

    def __next__(self):
        if self.iter_lim == self.iteration:
            raise StopIteration
        if self.dir == 1:
            if self.cur[1] == self.start_dir[1] + self.size - 1:
                self.dir = 2
                self.cur = (self.cur[0] + 1, self.cur[1])
                self.start_dir = self.cur
                self.size -= 1
            else:
                self.cur = (self.cur[0], self.cur[1] + 1)
        elif self.dir == 2:
            if self.cur[0] == self.start_dir[0] + self.size - 1:
                self.dir = 3
                self.cur = (self.cur[0], self.cur[1] - 1)
                self.start_dir = self.cur
            else:
                self.cur = (self.cur[0] + 1, self.cur[1])
        elif self.dir == 3:
            if self.cur[1] == self.start_dir[1] - self.size + 1:
                self.dir = 4
                self.cur = (self.cur[0] - 1, self.cur[1])
                self.start_dir = self.cur
                self.size -= 1
            else:
                self.cur = (self.cur[0], self.cur[1] - 1)
        elif self.dir == 4:
            if self.cur[0] == self.start_dir[0] - self.size + 1:
                self.dir = 1
                self.cur = (self.cur[0], self.cur[1] + 1)
                self.start_dir = self.cur
            else:
                self.cur = (self.cur[0] - 1, self.cur[1])
        self.iteration += 1
        return self.cur

    def __iter__(self):
        return self


def print_field():
    for i in Data.field:
        for j in i:
            print(('-' if j == -1 else j), end=' ')
        print()


def enc_reset():
    brick.encoder('E4').reset()
    brick.encoder('E3').reset()


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


def _drive_enc_(power=Robot.v):
    sgnL = sign(Data.encL - eL())
    sgnR = sign(Data.encR - eR())
    flagL = 0 if eL() < Data.encL else 1
    flagR = 0 if eR() < Data.encR else 1
    while [eL(), Data.encL][flagL] < [Data.encL, eL()][flagL] or [eR(), Data.encR][flagR] < [Data.encR, eR()][flagR]:
        powerL = max(0, min(power, 100)) * sgnL if [eL(), Data.encL][flagL] < [Data.encL, eL()][flagL] else 0
        powerR = max(0, min(power, 100)) * sgnR if [eR(), Data.encR][flagR] < [Data.encR, eR()][flagR] else 0
        motors(powerL, powerR)
        if Data.finish:
            exit(1)
        sleep(10)
    motors(0)


def forward_enc_simplified(cm=52.5):
    path = (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.encL += path  # Add start encoder value
    Data.encR += path  # Difference correction
    _drive_enc_()


def rotate_enc_simplified_relative(angle):
    if not TRIK:
        forward_enc_simplified(5)
    if abs(angle) < 200:
        angle *= 1000
    if abs(angle) >= 180000:
        angle -= 360000
    cm = Robot.track * pi * (angle / 360000)
    Data.encL += (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.encR -= (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.cur_angle += angle
    _drive_enc_(Robot.v//2)
    if not TRIK:
        forward_enc_simplified(-5)


def rotate_enc_simplified_absolute(angle):
    if abs(angle) < 200:
        angle *= 1000
    rotate_enc_simplified_relative(angle - Data.cur_angle)


def forward_enc_simplified_while(check_func, dir=1, power=Robot.v):
    """
    Едет по гироскому пока check_func возвращает True
    :param check_func: функция, по которой надо останавливать цикл (возвращает bool)
    :param dir: 1 - вперёд, -1 - назад
    :param power: скорость
    :return:
    """
    sgn = sign(dir)
    while check_func():
        motors(max(0, min(power, 100)) * sgn, max(0, min(power, 100)) * sgn)
        if Data.finish:
            exit(1)
        sleep(1)
    Data.encL = eL()
    Data.encR = eR()
    motors(0)


def forward_gyro(cm=float(Robot.cell_size), additional_corrections=0.0):
    gyro_kp = 0.002  # П коэффиент для езды по гироскопу
    path = (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.encL += path  # Add start encoder value
    Data.encR += path  # Add start encoder value

    # start_time = time()
    sgn = sign(cm)
    # decel_offset = (Robot.decel_start_offset / (pi * Robot.wheelD)) * Robot.cpr
    # decel_start = None
    flag = 0 if eL() < Data.encL else 1
    while [eL(), Data.encL][flag] < [Data.encL, eL()][flag]:
        # power_delta = Robot.acceleration * ((time() - start_time) / 1000)
        # power_accel = min(Robot.vstart + power_delta, Robot.v)
        # power_decel = Robot.v
        # if decel_start is not None:
        #     power_delta_decel = Robot.acceleration * ((time() - decel_start) / 1000)
        #     power_decel = max(Robot.vstart, Robot.v - power_delta_decel)
        # power = min(power_accel, power_decel)
        # if Data.encL - eL() < decel_offset and decel_start is None:
        #     decel_start = time()
        power = Robot.v
        error = Data.cur_angle - getYaw()  # Proportional steering
        if error > 180000:
            error -= 360000
        correction = error * gyro_kp
        motors(max(0, min(power + correction * sgn + additional_corrections, 100)) * sgn,
               max(0, min(power - correction * sgn - additional_corrections, 100)) * sgn)
        if Data.finish:
            exit(1)
        sleep(10)
    motors(0)
    # print(time() - decel_start)  # print the deceleration actual time after simulation


def forward_gyro_while(check_func, dir=1, power=Robot.v):
    """
    Едет по гироскому пока check_func возвращает True
    :param check_func: функция, по которой надо останавливать цикл (возвращает bool)
    :param dir: 1 - вперёд, -1 - назад
    :param power: скорость
    :return:
    """
    gyro_kp = 0.002  # П коэффиент для езды по гироскопу
    sgn = sign(dir)
    while check_func():
        error = Data.cur_angle - getYaw()  # Proportional steering
        correction = error * gyro_kp
        motors(max(0, min(power + correction * sgn, 100)) * sgn, max(0, min(power - correction * sgn, 100)) * sgn)
        if Data.finish:
            exit(1)
        sleep(1)
    Data.encL = eL()
    Data.encR = eR()
    motors(0)


def rotate_gyro_absolute(angle):
    """
    Rotates robot to a given value (NOTE: accepts values from -180 to 180 degrees!!!)
    """
    if not TRIK:
        forward_gyro(5)
    if abs(angle) < 200:
        angle *= 1000
    cm = Robot.track * pi * ((angle - Data.cur_angle) / 360000)
    Data.encL += (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.encR -= (cm / (pi * Robot.wheel_d)) * Robot.cpr
    Data.cur_angle = angle
    sgn = sign(angle - getYaw())
    if abs(angle - getYaw()) >= 180000:
        sgn *= -1
    motors(Robot.v * sgn, Robot.v * sgn)
    if Data.finish:
        exit(1)
    while abs(angle - getYaw()) > 3000:
        sleep(1)
        if Data.finish:
            exit(1)
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
    kp = 0.05  # П/ПИД регулятор коэффициент
    ki = 0.04  # И/ПИД регулятор коэффициент
    kd = 0.03  # Д/ПИД регулятор коэффициент
    err = value - setpoint
    Data.pid_deque_index = (Data.pid_deque_index + 1) % Robot.pid_window_size
    Data.pid_error_deque[Data.pid_deque_index] = err
    P = err * kp
    I = sum(Data.pid_error_deque) / 10 * ki
    D = (Data.pid_error_deque[Data.pid_deque_index] - Data.pid_error_deque[
        (Data.pid_deque_index + Robot.pid_window_size + 1) % Robot.pid_window_size]) * kd
    return P + I + D


def pid_correction_to_motors(base_speed: int, correction: float) -> None:
    """
    Runs motor based on calculated PID correction
    :param base_speed: default speed
    :param correction: PID correction value
    :return:
    """
    motors(min(max(base_speed * (1-correction), 10), 100), min(max(base_speed * (1+correction), 10), 100))
    if Data.finish:
        exit(1)


def get_neighbors(pos: tuple) -> list:
    """
    Получает смежные вершины графа (в лабиринте).
    Всё происходит в 3D
    :param pos: текущее положение (x, y, z)
    :return: [(x, y, z) * len(neighbors)]
    """
    ans = [((pos[0] + 1) % len(Robot.directions), pos[1], pos[2])]  # мы всегда можем повернуть в этой же клетке
    for i in Robot.directions[pos[0]]:
        if 0 <= pos[1] + i[0] < len(Data.field) and 0 <= pos[2] + i[1] < len(Data.field[pos[1] + i[0]]) \
                and Data.field[pos[1] + i[0]][pos[2] + i[1]] < 1:
            ans.append((pos[0], pos[1] + i[0], pos[2] + i[1]))
    return ans


def get_orientation() -> int:
    return (((Data.cur_angle + 180000 - 45000) // 90000) % 4) % 2


def BFS3D(target: list) -> list:
    """
    По списку смежностей (трёхмерному)
    :param target: list(tuple(x,y,z)) - все целевые вершины
    :return: list(tuple) если найдено инчае пустой list
    """
    target_cp = target.copy()
    target = []
    for i in target_cp:
        target += [(j, i[0], i[1]) for j in range(len(Robot.directions))] if len(i) == 2 else [i]
    start = get_orientation(), Data.robot_pos[0], Data.robot_pos[1]
    print('START', start)
    print('TARGET', target)
    queue = [start]
    done = [[[False for _ in range(len(Data.field[j]))] for j in range(len(Data.field))]
            for _ in range(len(Robot.directions))]  # посмотрели ли вершину
    marked = [[[(-1, -1, -1) for _ in range(len(Data.field[j]))] for j in range(len(Data.field))]
              for _ in range(len(Robot.directions))]  # прошлая вершина
    while len(queue) > 0:
        if Data.finish:
            exit(1)
        cur = queue[0]
        queue = queue[1:]
        if not done[cur[0]][cur[1]][cur[2]]:
            done[cur[0]][cur[1]][cur[2]] = True
            for i in get_neighbors(cur):
                if not done[i[0]][i[1]][i[2]]:
                    queue.append(i)
                    marked[i[0]][i[1]][i[2]] = cur
                    if i in target:  # если нашли
                        ans = []
                        j = i
                        ans.append(i)
                        while j != start:  # восстановление ответа
                            j = marked[j[0]][j[1]][j[2]]
                            ans.append(j)
                            if Data.finish:
                                exit(1)
                        ans.reverse()
                        print("PATH:", ans)
                        return ans
    return []


def localize() -> None:
    while Data.borders[2] - Data.borders[0] >= Robot.maze_size:
        if Data.finish:
            exit(1)
        target = Data.max_robot_pos[0] + 1, -1
        for i in range(len(Data.field[Data.max_robot_pos[0] + 1])):
            if Data.field[Data.max_robot_pos[0] + 1][i] < 1:
                if target[1] == -1 or abs(target[1] - Data.robot_pos[1]) > abs(i - Data.robot_pos[1]):
                    target = (Data.max_robot_pos[0] + 1, i)
        path = BFS3D([target])
        if len(path) == 0 or target == (Data.max_robot_pos[0] + 1, -1):
            Data.borders[2] = Data.max_robot_pos[0]
            update_borders()
            print("No path found X")
        ride_path(path)
    print('X loc done!')
    while Data.borders[3] - Data.borders[1] >= Robot.maze_size:
        if Data.finish:
            exit(1)
        target = -1, Data.min_robot_pos[1] - 1
        for i in range(len(Data.field)):
            if Data.field[i][Data.min_robot_pos[1] - 1] < 1:
                if target[0] == -1 or abs(target[0] - Data.robot_pos[0]) > abs(i - Data.robot_pos[0]):
                    target = (i, Data.min_robot_pos[1] - 1)
        path = BFS3D([target])
        if len(path) == 0 or target == (-1, Data.min_robot_pos[1] - 1):
            Data.borders[1] = Data.min_robot_pos[1]
            update_borders()
            print("No path found Y", Data.min_robot_pos[1] - 1)
        ride_path(path)
    print('Y loc done!')


def update_obstacles():
    Data.field[Data.robot_pos[0]][Data.robot_pos[1]] = 0
    distances = [sF(), sR(), sB(), sL()]
    deltas = [
        [(1, 0), (0, 1), (-1, 0), (0, -1)],
        [(0, -1), (1, 0), (0, 1), (-1, 0)]
        ]
    for i in range(len(distances)):
        if distances[i] < 35:
            Data.field[Data.robot_pos[0] +
                       deltas[get_orientation()][i][0]][Data.robot_pos[1] +
                                                        deltas[get_orientation()][i][1]] = 1
        elif distances[i] < 75:
            Data.field[Data.robot_pos[0] +
                       deltas[get_orientation()][i][0] * 2][Data.robot_pos[1] +
                                                            deltas[get_orientation()][i][1] * 2] = 1
            Data.field[Data.robot_pos[0] +
                       deltas[get_orientation()][i][0]][Data.robot_pos[1] +
                                                        deltas[get_orientation()][i][1]] = 0
        else:
            Data.field[Data.robot_pos[0] +
                       deltas[get_orientation()][i][0] * 2][Data.robot_pos[1] +
                                                            deltas[get_orientation()][i][1] * 2] = 0
            Data.field[Data.robot_pos[0] +
                       deltas[get_orientation()][i][0]][Data.robot_pos[1] +
                                                        deltas[get_orientation()][i][1]] = 0
    print_field()


def ride_path(path):
    for i in range(1, len(path)):
        for j in range(i, len(path)):
            if Data.field[path[j][1]][path[j][2]] > 0:
                return
        print(path[i - 1], '--->', path[i])
        if path[i][0] != path[i-1][0]:
            target_angle = 0 if path[i][0] == 1 else 90
            precise_90_degree_turn(target_angle - Data.cur_angle)
        else:
            forward_gyro((path[i][1] - path[i-1][1] + path[i-1][2] - path[i][2]) * Robot.cell_size,
                         distance_corrector_proportional())

        Data.robot_pos = (path[i][1], path[i][2])
        Data.min_robot_pos = (min(path[i][1], Data.min_robot_pos[0]), min(path[i][2], Data.min_robot_pos[1]))
        Data.max_robot_pos = (max(path[i][1], Data.max_robot_pos[0]), max(path[i][2], Data.max_robot_pos[1]))
        update_obstacles()
        update_borders()
        print('POSITION:', Data.robot_pos)


def update_borders() -> None:
    """
    Обновляет массив поля согласно заданным границам (заполняет всё, что за пределами границ стенами)
    :return:
    """
    Data.borders[0] = max(Data.borders[0], Data.robot_pos[0]-(Robot.maze_size-1))
    Data.borders[1] = max(Data.borders[1], Data.robot_pos[1]-(Robot.maze_size-1))
    Data.borders[2] = min(Data.borders[2], Data.robot_pos[0]+(Robot.maze_size-1))
    Data.borders[3] = min(Data.borders[3], Data.robot_pos[1]+(Robot.maze_size-1))

    for i in range(Data.borders[0]):
        for j in range(len(Data.field[i])):
            Data.field[i][j] = 2
    for j in range(Data.borders[1]):
        for i in range(len(Data.field)):
            Data.field[i][j] = 2
    for i in range(len(Data.field)-1, Data.borders[2], -1):
        for j in range(len(Data.field[i])):
            Data.field[i][j] = 2
    for j in range(len(Data.field[0])-1, Data.borders[3], -1):
        for i in range(len(Data.field)):
            Data.field[i][j] = 2


def proximity_corrector():
    """
    Corrects the robot position according to the walls position
    :return:
    """
    if sF() < 16:
        print("CORRECT TOO CLOSE FRONT")
        forward_gyro_while(lambda: sF() < 16, -1, 30)
    if 17 < sF() < 35:
        print("CORRECT TOO FAR FRONT")
        forward_gyro_while(lambda: sF() > 17, 1, 30)
    if sB() < 16:
        print("CORRECT TOO CLOSE BACK")
        forward_gyro_while(lambda: sB() < 16, 1, 30)
    if 17 < sB() < 35:
        print("CORRECT TOO FAR BACK")
        forward_gyro_while(lambda: sB() > 17, -1, 30)


def _turn_dir_free_(dir, corrections_enable=True):
    """
    Rotates robot
    :param dir: determines the turn direction (1 - clockwise, -1 - counterclockwise)
    :param corrections_enable: enables proximity corrections
    :return:
    """
    proximity_corrector()
    dir = sign(dir)
    if not TRIK:
        forward_gyro(5 - Robot.track/2)
    if sF() < 23 + (5 - Robot.track/2):
        print("CORRECT TOO CLOSE FRONT")
        forward_gyro_while(lambda: sF() < (17 + (5 - Robot.track/2)), -1, 30)
    angle = 90000
    if abs(Data.cur_angle - getYaw()) >= 180000:
        angle -= 360000
    cm = 2 * Robot.track * pi * (angle / 360000)
    amount = (cm / (pi * Robot.wheel_d)) * Robot.cpr
    if dir > 0:
        Data.encL += amount
    else:
        Data.encR += amount
    _drive_enc_(Robot.v//2)
    Data.cur_angle += angle * dir
    if not TRIK:
        forward_gyro(-5 - Robot.track/2)
    if corrections_enable:
        proximity_corrector()
    print('Rotate', Data.cur_angle, 'done!')


def _turn_opposite_dir_free_(dir, corrections_enable=True):
    """
    Rotates robot
    :param dir: determines the turn direction (1 - clockwise, -1 - counterclockwise)
    :param corrections_enable: enables proximity corrections
    :return:
    """
    proximity_corrector()
    dir = sign(dir)
    if not TRIK:
        forward_gyro(5 - Robot.track/2)
    if sF() < 23 + (5 - Robot.track/2):
        print("CORRECT TOO CLOSE FRONT")
        forward_gyro_while(lambda: sF() < (17 + (5 - Robot.track/2)), -1, 30)
    angle = 90000
    if abs(Data.cur_angle - getYaw()) >= 180000:
        angle -= 360000
    cm = 2 * Robot.track * pi * (angle / 360000)
    amount = (cm / (pi * Robot.wheel_d)) * Robot.cpr
    if dir < 0:
        Data.encL += amount
    else:
        Data.encR += amount
    _drive_enc_(Robot.v//2)
    Data.cur_angle -= angle * dir
    if not TRIK:
        forward_gyro(5 + Robot.track/2)
    if dir < 0:
        Data.encL -= amount
    else:
        Data.encR -= amount
    _drive_enc_(Robot.v//2)
    Data.cur_angle += angle * dir
    if sF() < 23 + (5 - Robot.track/2):
        print("CORRECT TOO CLOSE FRONT")
        forward_gyro_while(lambda: sF() < (23 + (5 - Robot.track/2)), -1, 30)
    if dir > 0:
        Data.encL += amount
    else:
        Data.encR += amount
    _drive_enc_(Robot.v//2)
    Data.cur_angle += angle * dir
    if corrections_enable:
        proximity_corrector()
    print('Rotate', Data.cur_angle, 'done!')


def _turn_front_free_(dir, corrections_enable=True):
    """
    Rotates robot
    :param dir: determines the turn direction (1 - clockwise, -1 - counterclockwise)
    :param corrections_enable: enables proximity corrections
    :return:
    """
    proximity_corrector()
    dir = sign(dir)
    if not TRIK:
        forward_gyro(5 + Robot.track/2)
    angle = 90000
    if abs(Data.cur_angle - getYaw()) >= 180000:
        angle -= 360000
    Data.cur_angle += angle * dir
    cm = 2 * Robot.track * pi * (angle / 360000)
    amount = (cm / (pi * Robot.wheel_d)) * Robot.cpr
    if dir < 0:
        Data.encL -= amount
    else:
        Data.encR -= amount
    _drive_enc_(Robot.v // 2)
    if not TRIK:
        forward_gyro(- 5 + Robot.track/2)
    if corrections_enable:
        proximity_corrector()
    print('Rotate', Data.cur_angle, 'done!')


def precise_90_degree_turn(dir, corrections_enable=True):
    """
    Turns robot in a maze by 90 degrees precisely
    :param dir: 1 - clockwise, -1 - counterclockwise
    :param corrections_enable: enables proximity corrections
    :return:
    """
    dir = sign(dir)
    if sF() > 35:
        _turn_front_free_(dir, corrections_enable)
    elif dir > 0:
        if sR() > 35:
            _turn_dir_free_(dir, corrections_enable)
        elif sL() > 35:
            _turn_opposite_dir_free_(dir, corrections_enable)
        else:
            raise NotImplementedError("Unknown turn type")
    else:
        if sL() > 35:
            _turn_dir_free_(dir, corrections_enable)
        elif sR() > 35:
            _turn_opposite_dir_free_(dir, corrections_enable)
        else:
            raise NotImplementedError("Unknown turn type")


# Main code
def main():
    print('Start')

    print('Correction')
    forward_gyro(Robot.cell_size/2)
    precise_90_degree_turn(90, False)
    forward_gyro(Robot.cell_size/2)

    print('Localize')
    update_obstacles()
    update_borders()
    localize()
    print('Location succeed!')
    print_field()

    print('Search start')
    status = False
    while not status:
        if Data.finish:
            exit(1)
        print('Searching again...')
        status = spiral_obstacle_search()
    print('Success!!!')


def watchdog(time_limit):
    """
    Watches the encoders value. If their value doesn't change much for more than
    time_limit ms - it kills the program
    :param time_limit:
    :return:
    """
    last_val1 = eL()
    last_val2 = eR()
    watch_timestamp = time()
    while True:
        if abs(eL() - last_val1) > 10 and abs(eR() - last_val2) > 10:
            last_val1 = eL()
            last_val2 = eR()
            watch_timestamp = time()
        if time() - watch_timestamp > time_limit:
            Data.finish = True
            break
        sleep(100)


def distance_corrector_proportional():
    """
    For maintaining the good distance to the wall while riding through the maze cells
    :return: correction value
    """
    kp = 2
    correction = 0
    if sL() < 16:
        correction = 16 - sL()
    elif 17 < sL() < 35:
        correction = 17 - sL()
    elif sR() < 16:
        correction = sR() - 16
    elif 17 < sR() < 35:
        correction = sR() - 17
    return correction * kp


def spiral_obstacle_search() -> bool:
    """
    Проходит по спирали от границы поля. (Выполняет одну итерацию поиска!)
    Если находит неизвестную клетку - пытается построить до неё путь.
    Находит препятствие - выводит ответ
    :return: True если успешно найден ответ, False если нет
    """
    for i in SpiralGenerator(Data.borders[2] - Data.borders[0] + 1):
        position = Data.borders[0] + i[0], Data.borders[1] + i[1]
        cell_type = Data.field[position[0]][position[1]]
        if cell_type == -1:
            path = BFS3D([position])
            if len(path) == 0:
                continue
            ride_path(path)
            return False
        elif cell_type == 1:
            ans = min(position[0] - Data.borders[0],
                      Data.borders[2] - position[0],
                      position[1] - Data.borders[1],
                      Data.borders[3] - position[1]) * Robot.cell_size
            print('FOUND:', i, 'ANSWER:', ans)
            brick.display().addLabel(str(ans), 0, 0)
            brick.display().redraw()
            return True


if __name__ == '__main__':
    gyro_calibrate()
    enc_reset()
    Thread(target=watchdog, args=(10000,), daemon=True).start()
    main()
