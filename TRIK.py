from enum import Enum


class KeysEnum(Enum):
    Left = 105
    Up = 103
    Down = 108
    Enter = 28
    Right = 106
    Power = 116
    Esc = 1


class Gyroscope:
    """
    Представляет гироскоп контроллера ТРИК.
    В состоянии покоя среднее значение выходного
    сигнала гироскопа не равно нулю и называется
    смещением нуля (bias) или систематической ошибкой (bias error).

    Параметр обусловлен многими факторами и может изменяться,
    например, в зависимости от окружающей температуры.

    Для правильной работы гироскопа необходимо
    вычитать смещение нуля из приходящих значений.
    Вычислить его можно с помощью метода «calibrate».

    Так как калибровка занимает длительное время,
    то при частом запуске модели можно выполнять ее один раз,
    после чего запоминать значение в переменную с помощью «getCalibrationVaules»,
    а при запуске программы вместо калибровки вызывать «setCalibrationValues».
    """
    def __init__(self):
        pass

    def read(self) -> list:
        """
        Возвращает массив из семи элементов:
            0−2 — угловые скорости по трем осям (в миллиградусах/секунды),
            3 — время последнего замера (в микросекундах),
            4−6 — углы наклона по трем осям (в миллиградусах).
        :return: list
        """
        return list()

    def calibrate(self, msec: int) -> None:
        """
        Вычисляет смещение нуля в течение указанного времени и инициализирует
        гироскоп этим параметром, сбрасывает текущие углы наклона.
        Рекомендуемое время калибровки — 10−20 секунд.
        :param msec: время в миллисекундах.
        :type msec: int
        :return: None
        """
        return

    def getCalibrationValues(self) -> tuple:
        """
        Возвращает объект, в котором содержатся необходимые данные о смещении нуля.
        :return: tuple
        """
        return tuple()

    def isCalibrated(self) -> bool:
        """
        Возвращает true в случае завершении калибровки, false — в противном случае.
        :return: bool
        """
        return False

    def readRawData(self) -> list:
        """
        Возвращает массив из трех элементов с угловыми скоростями по трем осям.
        :return:
        """
        return list()

    def setCalibrationValues(self, values) -> None:
        """
        Устанавливает объект, содержащий необходимые параметры о смещении нуля.

        Так как калибровка занимает длительное время, то при частом запуске модели можно
        выполнять ее один раз, после чего запоминать значение в переменную с помощью
        «getCalibrationValues», а при запуске программы вместо калибровки вызывать
        «setCalibrationValues».
        :param values: Значения, полученные из "getCalibrationValues"
        :type values: tuple
        :return:
        """
        return


class Accelerometer:
    """
    Представляет акселерометр контроллера ТРИК.
    """
    def __init__(self):
        pass

    def read(self) -> list:
        """
        Возвращает текущее показание сенсора в виде массива из трёх элементов,
        соответствующих показаниям сенсора по каждой из осей.
        :return: [x, y, z]
        """
        return list()


class Battery:
    """
    Предоставляет доступ к информации о батарее или блоке питания.
    """
    def __init__(self):
        pass

    def readVoltage(self) -> float:
        """
        Возвращает текущий вольтаж батареи (или блока питания) в вольтах.
        :return: float
        """
        return 1.01


class Display:
    """
    Предоставляет доступ к дисплею робота.

    Размер экрана: 240*320 пикселей.
    """
    def __init__(self):
        pass

    def addLabel(self, text: str, x: int, y: int) -> None:
        """
        Вывести на экран указанный текст в указанные координаты.
        Если в указанных координатах уже был текст, он будет заменён новым.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param text: выводимый текст
        :type text: str
        :param x: координаты экрана
        :type x: int
        :param y: координаты экрана
        :type y: int
        :return: None
        """
        return

    def clear(self) -> None:
        """
        Очистить окно для рисования.
        :return: None
        """
        return

    def drawArc(self, x: int, y: int, l: int, h: int, fr: int, to: int) -> None:
        """
        Нарисовать дугу эллипса, вписанного в прямоугольник с левым верхним углом
        в указанных координатах и имеющий заданную ширину и высоту.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param x: координаты левого верхнего угла прямоугольника на экране
        :param y: координаты левого верхнего угла прямоугольника на экране
        :param l: ширина прямоугольника
        :param h: высота прямоугольника
        :param fr: начальный угол, ограничивающий дугу
        :param to: конечный угол, ограничивающий дугу
        :return: None
        """
        return

    def drawEllipse(self, x: int, y: int, l: int, h: int, filled: bool = False) -> None:
        """
        Нарисовать эллипс, вписанный в прямоугольник с левым верхним углом
        в указанных координатах и имеющий заданную ширину и высоту.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param x: координаты левого верхнего угла прямоугольника
        :param y: координаты левого верхнего угла прямоугольника
        :param l: ширина прямоугольника
        :param h: высота прямоугольника
        :param filled: заливать фигуру или нет, по умолчанию false
        :return: None
        """
        return

    def drawLine(self, x0: int, y0: int, x1: int, y1: int) -> None:
        """
        Нарисовать линию с началом и концом в заданных координатах.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param x0: координаты начала линии
        :param y0: координаты начала линии
        :param x1: координаты конца линии
        :param y1: координаты конца линии
        :return: None
        """
        return

    def drawPoint(self, x: int, y: int) -> None:
        """
        Нарисовать точку в заданных координатах.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param x: координаты точки
        :param y: координаты точки
        :return: None
        """
        return

    def drawRect(self, x: int, y: int, l: int, h: int, filled: bool) -> None:
        """
        Нарисовать прямоугольник с левым верхним углом
        в указанных координатах и имеющий заданную ширину и высоту.
        Изменения на дисплее произойдут только после вызова метода «redraw».
        :param x: координаты левого верхнего угла прямоугольника
        :param y: координаты левого верхнего угла прямоугольника
        :param l: ширина прямоугольника
        :param h: высота прямоугольника
        :param filled: заливать фигуру или нет, по умолчанию false
        :return: None
        """
        return

    def hide(self) -> None:
        """
        Закрыть и очистить окно для рисования.
        :return: None
        """
        return

    def redraw(self) -> None:
        """
        Перерисовать окно для рисования.
        Изменения на дисплее произойдут только после вызова этого метода.
        :return: None
        """
        return

    def removeLabels(self) -> None:
        """
        Удалить с экрана весь текст, добавленный на него вызовами метода «addLabel».
        :return: None
        """
        return

    def setBackground(self, color: str) -> None:
        """
        Установить фон экрана в указанный цвет.
        Возможные цвета:
            white,
            red, darkRed,
            green, darkGreen,
            blue, darkBlue,
            cyan, darkCyan,
            magenta, darkMagenta,
            yellow, darkYellow,
            gray, darkGray, lightGray,
            black.
        :param color: цвет
        :return: None
        """
        return

    def setPainterColor(self, color: str) -> None:
        """
        Установить цвет кисти, которой рисуются графические примитивы.
        Возможные цвета:
            white,
            red, darkRed,
            green, darkGreen,
            blue, darkBlue,
            cyan, darkCyan,
            magenta, darkMagenta,
            yellow, darkYellow,
            gray, darkGray, lightGray,
            black.
        :param color: цвет
        :return: None
        """
        return

    def setPainterWidth(self, d: int) -> None:
        """
        Установить толщину кисти, которой рисуются графические примитивы, в пикселях.
        :param d: толщина
        :return: None
        """
        return

    def show(self, array: list, width: int, height: int, format: str) -> None:
        """
        Вывести на дисплей контроллера изображение, преобразованное из однородного массива данных.
        :param array: одномерный целочисленный массив, имеющий размеры width×height
        :param width: ширина изображения
        :param height: высота изображения
        :param format: В качестве параметра format необходимо передать формат,
                        в котором представлен каждый элемент массива.
                        Сейчас поддержаны форматы: «rgb32», «grayscale8», «rgb888».
        :return:
        """
        return

    def showImage(self, imagePath: str) -> None:
        """
        Вывести на экран изображение, предварительно загруженное на робот.
        :param imagePath: В качестве параметра необходимо указать имя файла с изображением
                        (в форматах BMP, GIF, JPG, JPEG, PNG, PBM, PGM, PPM, TIFF, XBM, XPM),
                        путь указывается либо абсолютным, либо относительно папки trik.
        :return: None
        """
        return


class colorSensor:
    """
    Видеокамера в режиме датчика цвета.
    """
    def __init__(self, id: str):
        """
        Constructor
        :param id: port id
        :type id: str
        """
        pass

    def init(self, value: bool) -> None:
        """
        Включает видеокамеру и инициализирует её в режиме датчика цвета.
        :param value: Булевый параметр определяет, выводить ли на экран изображение с камеры:
                        true - выводить
                        false - не выводить
        :type value: bool
        :return: None
        """
        return

    def read(self, x: int, y: int) -> list:
        """
        Возвращает массив с координатами доминирующего цвета
        в цветовой шкале RGB в указанном участке кадра.
        Кадр делится на квадраты сеткой, по умолчанию 3 на 3,
        размерность сетки можно задать в model-config.xml на роботе.
        Квадраты индексируются с 1. То есть (1, 1) — это левый верхний
        край кадра, (2, 2) — его центр.
        :param x: X координата
        :type x: int
        :param y: Y координата
        :type y: int
        :return: Массив из трёх элементов от 0 до 255, индексирующийся с 0.
                    Нулевой элемент содержит интенсивность красного (0 — совсем нет, 255 — очень много),
                    первый — интенсивность зелёного, второй — интенсивность синего.
                    Например, (0, 0, 0) — чёрный, (255, 255, 255) — белый, (255, 0, 0) — красный.
        """
        return list()

    def stop(self) -> None:
        """
        Выключает видеокамеру и прекращает работу датчика.
        :return: None
        """
        return


class Encoder:
    """
    Представляет энкодеры силовых моторов, подключающиеся к портам E1, E2, E3, E4.
    """
    def __init__(self, port: str):
        """
        Constructor
        :param port: port id
        """
        pass

    def read(self) -> int:
        """
        Возвращает текущее показание энкодера в тиках на заданном порту.
        :return: положение энкодера
        """
        return 1

    def reset(self) -> None:
        """
        Сбрасывает в 0 текущее показание энкодера.
        :return:
        """
        return

    def readRawData(self) -> int:
        """
        Возвращает текущее показание энкодера в «тиках» на заданном порту.
        :return: положение энкодера
        """
        return 1


class Keys:
    """
    Служит для работы с кнопками на пульте робота
    """
    def __init__(self):
        pass

    def isPressed(self, code: int) -> bool:
        """
        Возвращает true, если кнопка с указанным кодом нажата в данный момент.
        :param code: Код кнопки (можно получить через KeysEnum)
        :return: bool (Состояиние кнопки)
        """
        return False

    def reset(self) -> None:
        """
        Сбрасывает запомненные нажатия кнопок.
        :return: None
        """
        return

    def wasPressed(self, code: int) -> bool:
        """
        Возвращает, была ли нажата кнопка с указанным кодом,
        сбрасывает запомненные нажатия для этой кнопки.
        :param code: Код кнопки (можно получить через KeysEnum)
        :return: bool (Состояиние кнопки)
        """
        return False


class Led:
    """
    Предоставляет управление светодиодом на корпусе робота.
    """
    def red(self) -> None:
        """
        Включает светодиод в режим «красный».
        :return: None
        """
        return

    def green(self) -> None:
        """
        Включает светодиод в режим «зеленый».
        :return: None
        """
        return

    def orange(self) -> None:
        """
        Включает светодиод в режим «оранжевый».
        :return: None
        """
        return

    def off(self) -> None:
        """
        Выключает светодиод.
        :return: None
        """
        return


class LineSensor:
    """
    Видеокамера в режиме датчика линии.
    """
    def __init__(self, id: str):
        """
        Constructor
        :param id: port id
        :type id: str
        """
        pass

    def detect(self) -> None:
        """
        Определяет доминирующий цвет в вертикальной полосе
        в центре кадра и запоминает его как цвет линии.
        После этого метод «read» начинает возвращать данные для этой линии.
        :return: None
        """
        return

    def init(self, show: bool) -> None:
        """
        Включает видеокамеру и инициализирует её в режиме датчика линии.
        :param show: Булевый параметр определяет, выводить ли на экран изображение с камеры:
                        true — выводить,
                        false — не выводить.
        :return: None
        """
        return

    def read(self) -> list:
        """
        Считывает данные с камеры
        :return: Возвращает массив, в ячейках которого находятся следующие данные:
                    в нулевой ячейке координата по оси X центра линии относительно центра кадра
                    (от -100 до 100, -100 — центр линии на краю кадра слева);

                    в первой ячейке — вероятность перекрёстка (число от 0 до 100, показывающее
                    сколько точек цвета линии находится в горизонтальной полосе в центре кадра);

                    во второй ячейке — относительный размер линии, число от 0 до 100
                    (100 — линия занимает почти весь кадр, 0 — линии нет на кадре).
        """
        return list()

    def stop(self) -> None:
        """
        Выключает видеокамеру и прекращает работу датчика.
        :return: None
        """
        return


class Motor:
    """
    Предоставляет управление мотором робота (силовым или сервомотором),
    подключающимся к портам M1, …, M4, S1, ..., S6.
    """
    def __init__(self, port: str):
        """
        Constructor
        :param port: В качестве параметра необходимо указать порт.
        """
        pass

    def brake(self, durationMs: int) -> None:
        """
        Блокировка моторов для торможения в течение указанного времени в миллисекундах.
        :param durationMs: В качестве параметра необходимо указать время в миллисекундах.
        :return: None
        """
        return

    def power(self) -> int:
        """
        Возвращает текущую мощность мотора (от -100 до 100).
        :return: Мощность мотора
        """
        return 50

    def powerOff(self) -> None:
        """
        Выключает мотор.
        :return: None
        """
        return

    def setPower(self, power: int) -> None:
        """
        Включает мотор с указанной мощностью.
        :param power: В качестве параметра необходимо указать мощность.
        Мощность задаётся в диапазоне от -100 («полный назад») до 100 («полный вперёд»).
        0 соответствует force break, то есть мотор останавливается, при этом он заблокирован
        и остаётся под напряжением.
        :return: None
        """
        return


class ObjectSensor:
    """
    Видеокамера в режиме датчика объекта.
    Захватывает контрастный объект в центре кадра
    и возвращает его координаты и размер в кадре.
    """
    def __init__(self):
        pass

    def detect(self) -> None:
        """
        Определяет доминирующий цвет в центре кадра и запоминает его как цвет объекта.
        После этого метод «read» начинает возвращать данные для объекта.
        :return: None
        """
        return

    def init(self, show: bool) -> None:
        """
        Включает видеокамеру и инициализирует её в режиме датчика объекта.
        :param show: Булевый параметр определяет,
                        выводить ли на экран изображение с камеры (true — выводить).
        :return: None
        """
        return

    def read(self) -> list:
        """
        Возвращает массив, в ячейках которого находятся следующие данные:
        В нулевой ячейке координата по оси X центра объекта относительно центра кадра
        (от -100 до 100, -100 — центр объекта на краю кадра слева);

        В первой ячейке — координата по оси Y центра объекта относительно центра кадра
        (от -100 до 100, -100 — центр объекта на краю кадра сверху);

        Во второй ячейке — относительный размер объекта, число от 0 до 100
        (100 — объекта занимает почти весь кадр, 0 — объекта нет на кадре).
        :return: list
        """
        return list()

    def stop(self) -> None:
        """
        Выключает видеокамеру и прекращает работу датчика.
        :return: None
        """
        return


class Sensor:
    """
    Представляет сенсор (аналоговый или цифровой), подключающийся к портам A1, …, A6, D1, D2.
    """
    def __init__(self, portName: str):
        """
        Constructor
        :param portName: A1, …, A6, D1, D2
        """
        pass

    def read(self) -> int:
        """
        Возвращает текущее показание сенсора (цифрового или аналогового),
        подключённого к данному порту. Возвращается приведённое значение,
        зависящее от конфигурации порта, которая описывается в файле model-config.xml
        в папке trik на роботе.

        Например, ИК-датчик расстояния возвращает значение в сантиметрах.
        :return: value
        """
        return 10

    def readRawData(self) -> int:
        """
        Возвращает текущее «сырое» показание сенсора (цифрового или аналогового),
        подключённого к данному порту. Диапазон значений зависит от конкретного сенсора
        и не учитывает конфигурацию робота (возвращаются физические показания сенсора,
        например, задержка принятого ультразвукового сигнала).
        :return: value
        """
        return 10


class Marker:
    """
    Предоставляет доступ к рисованию маркером заданного цвета на полу.
    Доступен только в режиме 2D модели.
    """
    def __init__(self):
        pass

    def down(self, color: str) -> None:
        """
        Начать рисование маркером заданного цвета на полу.
        При движении робота в двумерной модели за ним будет оставаться цветная линия.
        Если был установлен маркер другого цвета, он будет заменен.
        :param color: Цвет. Возможные цвета:
                        white,
                        red, darkRed,
                        green, darkGreen,
                        blue, darkBlue,
                        cyan, darkCyan,
                        magenta, darkMagenta,
                        yellow, darkYellow,
                        gray, darkGray, lightGray,
                        black.
        :return: None
        """
        return

    def up(self) -> None:
        """
        Закончить рисование маркером.
        :return: None
        """
        return

    def isDown(self) -> bool:
        """
        Возвращает true, если маркер активен, false - если нет.
        :return: bool
        """
        return False

    def setDown(self, value: bool) -> None:
        """
        Вызывает метод down("black"), или up() в зависимости от аргумента.
        :param value: bool
        :return: None
        """
        return


class brick:
    """
    Объект «brick» представляет контроллер ТРИК и предоставляет доступ к устройствам робота.
    """
    def accelerometer(self) -> Accelerometer:
        """
        Предоставляет доступ к акселерометру
        :return: Gyroscope class
        """
        return Accelerometer()

    def battery(self) -> Battery:
        """
        Предоставляет доступ к информации об аккумуляторе
        :return: Battery class
        """
        return Battery()

    def colorSensor(self, id: str) -> colorSensor:
        """
        Предоставляет доступ к датчику цвета по видеокамере.
        :param id: port id
        :type id: str
        :return: colorSensor class
        """
        return colorSensor(id)

    def display(self) -> Display:
        """
        Предоставляет доступ к дисплею робота.
        :return: Display class
        """
        return Display()

    def encoder(self, portName: str) -> Encoder:
        """
        Предоставляет доступ к энкодеру на указанном порту.
        :param portName: порт
        :return: Encoder class
        """
        return Encoder(portName)

    def getStillImage(self) -> list:
        """
        Получить фотографию с камеры в виде массива байт.
        :return: массив байт, составляющий фотографию с камеры
        """
        return list()

    def gyroscope(self) -> Gyroscope:
        """
        Предоставляет доступ к гироскопу
        :return: Gyroscope class
        """
        return Gyroscope()

    def keys(self) -> Keys:
        """
        Предоставляет доступ к кнопкам на корпусе робота
        :return: Keys class
        """
        return Keys()

    def led(self) -> Led:
        """
        Предоставляет доступ к светодиоду на корпусе робота
        :return: Led class
        """
        return Led()

    def lineSensor(self, port: str) -> LineSensor:
        """
        Предоставляет доступ к датчику линии по видеокамере
        :param port: port id ("video1"/"video2")
        :return: LineSensor class
        """
        return LineSensor(port)

    def motor(self, port: str) -> Motor:
        """
        Предоставляет доступ к мотору (силовому или сервомотору) на указанном порту.
        :param port: В качестве параметра необходимо указать порт.
        :return: Motor class
        """
        return Motor(port)

    def objectSensor(self) -> ObjectSensor:
        """
        Предоставляет доступ к датчику объекта по видеокамере
        :return: ObjectSensor class
        """
        return ObjectSensor()

    def playSound(self, filename: str) -> None:
        """
        Проиграть звуковой файл.
        :param filename: В качестве параметра необходимо указать имя файла с абсолютным путем
                            или путем относительно папки trik на контроллере.
        :return: None
        """
        return

    def playTone(self, frequency: int, time: int) -> None:
        """
        Проиграть звук с заданной частотой.
        :param frequency: Частота звука frequency
        :param time: Время time в мс, в течение которого необходимо проигрывать звук.
        :return: None
        """
        return

    def say(self, string: str) -> None:
        """
        Произнести строку (на русском или английском языке).
        :param string: В качестве параметра необходимо указать строку на английском или русском языке.
        :return: None
        """
        return

    def sensor(self, portName: str) -> Sensor:
        """
        Предоставляет доступ к сенсору на указанном порту
        :param portName: A1, …, A6, D1, D2
        :return: Sensor class
        """
        return Sensor(portName)

    def stop(self) -> None:
        """
        Останавливает все моторы и активные датчики, убирает нарисованное на дисплее.
        :return: None
        """
        return

    def marker(self) -> Marker:
        """
        Предоставляет доступ к рисованию маркером заданного цвета на полу.
        Доступен только в режиме двумерной модели
        :return: Marker class
        """
        return Marker()
