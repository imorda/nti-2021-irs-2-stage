import os


n, m = 600, 800
# n, m = 10, 10

data0 = [[] for _ in range(n)]
if os.getenv("LOCAL"):
    with open('tests/1', 'r') as f:
        for i in range(n):
            data0[i] = f.readline().rstrip().split()
else:
    for i in range(n):
        data0[i] = input().split()


data = [[-1 for _ in range(m)] for _ in range(n)]
next_color = 0
for i in range(n):
    for j in range(m):
        if data[i][j] != -1:
            continue
        data[i][j] = next_color
        next_color += 1

        queue = [(i, j)]
        while len(queue) > 0:
            a, b = queue.pop()
            neighs = [(a - 1, b), (a, b + 1), (a + 1, b), (a, b - 1)]
            for aa, bb in neighs:
                if 0 <= aa < n and 0 <= bb < m and data0[aa][bb] == data0[a][b] and data[aa][bb] == -1:
                    data[aa][bb] = data[a][b]
                    queue.append((aa, bb))

ans = 0
colors = {}
for i in range(n):
    for j in range(m):
        cur = data[i][j]
        if cur == 0:
            continue
        if cur not in colors:
            colors[cur] = set()

        neighs = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
        for a, b in neighs:
            if 0 <= a < n and 0 <= b < m and data[a][b] != cur:
                colors[cur].add((a, b))
                ans = max(ans, len(colors[cur]))

print(ans)
