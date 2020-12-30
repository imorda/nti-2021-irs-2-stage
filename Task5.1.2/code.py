import matplotlib.pyplot as plt  # визуализация

width = 160
height = 120
cell_count = 5
threshold = 255//6  # порог бинаризации


def diagonal_generator(second_size, first_size, order):
    """
        Diagonal iteration generator
        :param second_size: matrix width (length of first element in matrix)
        :param first_size: matrix height (length of matrix itself)
        :param order: order to iterate through (0 - from upper left corner,
                            1 - from upper right,
                            2 - from lower right,
                            3 - from lower left)
        :return: iterable object to iterate through matrix in diagonal order
        """
    for first in range(first_size):
        for hor in range(first, -1, -1):
            vert = first - hor
            if order == 1:
                vert = second_size - 1 - vert
            elif order == 2:
                hor = first_size - 1 - hor
                vert = second_size - 1 - vert
            elif order == 3:
                hor = first_size - 1 - hor
            yield hor, vert
    for first in range(1, second_size):
        for hor in range(first_size - 1, -1, -1):
            vert = first + (first_size - 1 - hor)
            if vert >= second_size:
                break
            if order == 1:
                vert = second_size - 1 - vert
            elif order == 2:
                hor = first_size - 1 - hor
                vert = second_size - 1 - vert
            elif order == 3:
                hor = first_size - 1 - hor
            yield hor, vert


def cross(point1, point2, point3, point4):
    """
    Finds intersection point of 2 lines given by 2 points
    :param point1:
    :param point2:
    :param point3:
    :param point4:
    :return: tuple (x, y)
    """
    if point1[0] == point2[0] or point3[0] == point4[0]:
        if point1[0] == point2[0]:
            k_multiplier = (point3[1] - point4[1]) / (point3[0] - point4[0])
            b_value = (point4[0] * point3[1] - point3[0] * point4[1]) / (point4[0] - point3[0])
            x_intersect = point1[0]
        else:
            k_multiplier = (point1[1] - point2[1]) / (point1[0] - point2[0])
            b_value = (point2[0] * point1[1] - point1[0] * point2[1]) / (point2[0] - point1[0])
            x_intersect = point3[0]
        y_intersect = k_multiplier * x_intersect + b_value
        return round(x_intersect), round(y_intersect)

    k1 = (point1[1] - point2[1])/(point1[0] - point2[0])
    k2 = (point3[1] - point4[1])/(point3[0] - point4[0])
    b1 = (point1[1] * point2[0] - point2[1] * point1[0]) / (point2[0] - point1[0])
    b2 = (point3[1] * point4[0] - point4[1] * point3[0]) / (point4[0] - point3[0])
    return round((b2 - b1) / (k1 - k2)), round((b1*k2-b2*k1)/(k2-k1))


def int_hex(u):
    return int(u, 16)


src = []  # исходная картинка
for i in range(height):
    src.append(list(map(int_hex, input().split())))

rgb = []  # разбитая по каналам цвета
for i in src:
    rgb.append([])
    for j in i:
        r = (j & 0xff0000) >> 8*2
        g = (j & 0x00ff00) >> 8
        b = (j & 0x0000ff)
        rgb[-1].append([r, g, b])

grayscale = []  # оттенки серого
for i in rgb:
    grayscale.append([])
    for j in i:
        grayscale[-1].append(sum(j)//len(j))  # перевод в оттенки серого по среднему арифметическому

median_grayscale = [[0 for i in range(width)] for j in range(height)]
median_deltas = [(0, 0), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
for i in range(1, height-1):  # median filter
    for j in range(1, width-1):
        cur = []
        for k in median_deltas:
            cur.append(grayscale[i + k[0]][j + k[1]])
        cur.sort()
        median_grayscale[i][j] = cur[len(median_deltas)//2]

binary = []  # чёрно-белая
# TODO: адаптивная бинаризация?
for i in median_grayscale:
    binary.append([])
    for j in i:
        binary[-1].append(int(j > (255//6)))

binary = binary[4:len(binary)-4]  # ROI
for i in range(len(binary)):
    binary[i] = binary[i][4: len(binary[i]) - 4]
width -= 8
height -= 8

preview = []
for i in binary:
    preview.append(i.copy())

# Проверка на обрезанность
# TODO: поиск углов в обрезанном маркере
# for i in binary[0]:
#     if i == 0:
#         print('L')
#         exit(0)
# for i in binary:
#     if i[0] == 0:
#         print('L')
#         exit(0)
#     elif i[-1] == 0:
#         print('R')
#         exit(0)
# for i in binary[-1]:
#     if i == 0:
#         print('L')
#         exit(0)

# Поиск углов маркера
corners = []  # будем тут хранить коорды углов
for n in range(4):
    for i in diagonal_generator(width, height, n):
        if binary[i[0]][i[1]] == 0:
            if i[0] != 0 and i[1] != 0 and i[0] < height-1 and i[1] < width-1:
                corners.append(i)
            else:
                corners.append((-1, -1))
            break

try:
    while True:
        index = corners.index((-1, -1))
        p1 = corners[(index - 1) % len(corners)]
        p3 = corners[(index + 1) % len(corners)]
        if p1 == (-1, -1):
            if p1 == 0 or p1 == 3:
                print('L')
            else:
                print('R')
            exit(0)
        if p3 == (-1, -1):
            if p3 == 0 or p3 == 3:
                print('L')
            else:
                print('R')
            exit(0)
        sides = [[0, 1], [1, 2], [2, 3], [3, 0]]
        flag = False
        if 0 in sides[index]:
            for i in range(height):
                flag = False
                if binary[i][0] == 0:
                    for j in range(height-1, -1, -1):
                        if binary[j][0] == 0:
                            p4 = (i, 0)
                            p2 = (j, 0)
                            corners[index] = cross(p1, p2, p3, p4)
                            flag = True
                            break
                if flag:
                    break
        if flag:
            continue
        flag = False  # Да, копипаста. И чо теперь?
        if 1 in sides[index]:
            for i in range(width):
                flag = False
                if binary[0][i] == 0:
                    for j in range(width-1, -1, -1):
                        if binary[0][j] == 0:
                            p4 = (0, j)
                            p2 = (0, i)
                            corners[index] = cross(p1, p2, p3, p4)
                            flag = True
                            break
                if flag:
                    break
        if flag:
            continue
        flag = False
        if 2 in sides[index]:
            for i in range(height):
                flag = False
                if binary[i][width-1] == 0:
                    for j in range(height-1, -1, -1):
                        if binary[j][width-1] == 0:
                            p4 = (j, width-1)
                            p2 = (i, width-1)
                            corners[index] = cross(p1, p2, p3, p4)
                            flag = True
                            break
                if flag:
                    break
        if flag:
            continue
        flag = False  # Да, копипаста. И чо теперь?
        if 3 in sides[index]:
            for i in range(width):
                flag = False
                if binary[height-1][i] == 0:
                    for j in range(width-1, -1, -1):
                        if binary[height-1][j] == 0:
                            p4 = (height-1, i)
                            p2 = (height-1, j)
                            corners[index] = cross(p1, p2, p3, p4)
                            flag = True
                            break
                if flag:
                    break
except ValueError:
    pass

corners45 = []  # углы на случай если квадрат у нас косожопый
for i in range(width):
    flag = False
    for j in range(height):
        if binary[j][i] == 0 and i != 0 and j != 0 and j < height-1 and i < width-1:
            corners45.append((j, i))
            flag = True
            break
    if flag:
        break
for i in range(height):
    flag = False
    for j in range(width):
        if binary[i][j] == 0 and i != 0 and j != 0 and i < height-1 and j < width-1:
            corners45.append((i, j))
            flag = True
            break
    if flag:
        break
for i in range(width-1, -1, -1):
    flag = False
    for j in range(height):
        if binary[j][i] == 0 and i != 0 and j != 0 and j < height-1 and i < width-1:
            corners45.append((j, i))
            flag = True
            break
    if flag:
        break
for i in range(height-1, -1, -1):
    flag = False
    for j in range(width):
        if binary[i][j] == 0 and i != 0 and j != 0 and i < height-1 and j < width-1:
            corners45.append((i, j))
            flag = True
            break
    if flag:
        break

if len(corners45) == 4:
    if abs(corners45[0][0] - corners45[2][0]) < cell_count * 2 \
            and abs(corners45[1][1] - corners45[3][1]) < cell_count * 2:
        corners = corners45

if len(corners) < 4:
    print("L")
    exit(0)

cont_segmentation = []  # тут будем хранить коорды сегментации контура
for n in range(4):
    cont_segmentation.append([])
    for i in range(cell_count):
        cell_delta = (corners[n][0] - corners[n-1][0]) / cell_count, (corners[n][1] - corners[n-1][1]) / cell_count
        x = int(corners[n-1][0] + (cell_delta[0] / 2) + cell_delta[0] * i)
        y = int(corners[n-1][1] + (cell_delta[1] / 2) + cell_delta[1] * i)
        cont_segmentation[-1].append((x, y))

# тут будут коорды центров всех квадратов маркера
cell_centers = [[(0, 0) for i in range(cell_count)] for j in range(cell_count)]
for i in range(cell_count):
    for j in range(cell_count):
        cent = cross(cont_segmentation[0][i], cont_segmentation[2][cell_count - 1 - i],
                     cont_segmentation[1][j], cont_segmentation[3][cell_count - 1 - j])
        cell_centers[i][j] = cent
        if 0 <= cent[0] < height and 0 <= cent[1] < width:
            preview[cent[0]][cent[1]] = 3

# проверка на выход из массива значащих пикселей
for i in range(1, cell_count-1):
    for j in range(1, cell_count-1):
        if 0 <= cell_centers[i][j][0] < height and 0 <= cell_centers[i][j][1] < width:
            pass
        else:
            if cell_centers[i][j][1] < 0:
                print('L')
                exit(0)
            elif cell_centers[i][j][1] >= width:
                print('R')
                exit(0)
            elif cell_centers[i][j][1] < abs(cell_centers[i][j][1] - (width-1)):
                # Если пиксель лежит ближе к левой границе
                print('L')
                exit(0)
            else:
                print('R')
                exit(0)
for i in corners:
    preview[i[0]][i[1]] = 5
# TODO: можно посчитать среднее арифметическое ВСЕХ пикселей каждого бита

key = [cell_centers[1][1], cell_centers[1][cell_count-2],
       cell_centers[cell_count-2][cell_count-2], cell_centers[cell_count-2][1]]  # ключевые биты
key_val = []  # значение ключевых битов
for i in key:
    key_val.append(binary[i[0]][i[1]])

if sum(key_val) != 1:
    print("L")
    exit(0)

orientation = -1
for ind, i in enumerate(key_val):
    if i == 1:
        orientation = ind
        break

code = []
parity = -1
if orientation == 0:
    for j in range(2, cell_count-2):
        pos = cell_centers[j][cell_count-2]
        code.append(binary[pos[0]][pos[1]])
    for i in range(cell_count - 3, 1, -1):
        for j in range(1, cell_count-1):
            pos = cell_centers[j][i]
            if i == cell_count // 2 and j == cell_count // 2:
                parity = binary[pos[0]][pos[1]]
            else:
                code.append(binary[pos[0]][pos[1]])
    for j in range(2, cell_count - 2):
        pos = cell_centers[j][1]
        code.append(binary[pos[0]][pos[1]])
elif orientation == 1:
    for j in range(2, cell_count-2):
        pos = cell_centers[1][j]
        code.append(binary[pos[0]][pos[1]])
    for i in range(2, cell_count-2):
        for j in range(1, cell_count-1):
            pos = cell_centers[i][j]
            if i == cell_count // 2 and j == cell_count // 2:
                parity = binary[pos[0]][pos[1]]
            else:
                code.append(binary[pos[0]][pos[1]])
    for j in range(2, cell_count - 2):
        pos = cell_centers[cell_count-2][j]
        code.append(binary[pos[0]][pos[1]])
elif orientation == 2:
    for j in range(cell_count-3, 1, -1):
        pos = cell_centers[j][1]
        code.append(binary[pos[0]][pos[1]])
    for i in range(2, cell_count-2):
        for j in range(cell_count-2, 0, -1):
            pos = cell_centers[j][i]
            if i == cell_count // 2 and j == cell_count // 2:
                parity = binary[pos[0]][pos[1]]
            else:
                code.append(binary[pos[0]][pos[1]])
    for j in range(cell_count-3, 1, -1):
        pos = cell_centers[j][cell_count-2]
        code.append(binary[pos[0]][pos[1]])
elif orientation == 3:
    for j in range(cell_count-3, 1, -1):
        pos = cell_centers[cell_count-2][j]
        code.append(binary[pos[0]][pos[1]])
    for i in range(cell_count-3, 1, -1):
        for j in range(cell_count-2, 0, -1):
            pos = cell_centers[i][j]
            if i == cell_count // 2 and j == cell_count // 2:
                parity = binary[pos[0]][pos[1]]
            else:
                code.append(binary[pos[0]][pos[1]])
    for j in range(cell_count-3, 1, -1):
        pos = cell_centers[1][j]
        code.append(binary[pos[0]][pos[1]])

code.reverse()

if sum(code) % 2 != parity:
    print('L')
    exit(0)

code_str = ''
for i in code:
    code_str += str(i)

code_decimal = int(code_str, 2)
print(code_decimal)

fig, ax = plt.subplots()
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)
ax.imshow(preview)
plt.show()
