x = list(map(int, input().split(',')))
for j in range(120):
    for i in range(160):
        print(hex(x[j * 160 + i]), end=' ')
    print()
# Эта фигня переводит формат одномерного массива (который даёт триковский getImage() с разделителем-запятой
# В формат, который нужен для code.py
