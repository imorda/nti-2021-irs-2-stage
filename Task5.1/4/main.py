X, Y = 12, 12
WALLS = [
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    [0, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 1, 0, 0],
    [1, 0, 0, 1],
    [1, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 1, 1, 0]
]

INF = 10 ** 9


def decode_direction(direction: str) -> int:
    return {"U": 0, "R": 1, "D": 2, "L": 3}[direction]


def encode_direction(direction: int) -> str:
    return {0: "U", 1: "R", 2: "D", 3: "L"}[direction]


def cell_by_coords(y: int, x: int) -> int:
    return y * X + x


def coords_by_cell(cell: int) -> (int, int):
    return cell // X, cell % X


def forward_coords(y: int, x: int, direction: int) -> (int, int):
    if direction == 0:
        return y - 1, x
    elif direction == 1:
        return y, x + 1
    elif direction == 2:
        return y + 1, x
    elif direction == 3:
        return y, x - 1
    else:
        raise ValueError


def bfs_with_rotates_on_2d_labyrinth(start_y: int, start_x: int, start_direction: int) -> list:
    dist = [[[INF, INF, INF, INF] for _ in range(X)] for _ in range(Y)]
    dist[start_y][start_x][start_direction] = 0
    used = [[[False, False, False, False] for _ in range(X)] for _ in range(Y)]

    queue = [(start_y, start_x, start_direction)]
    current_element = 0
    while current_element < len(queue):
        y, x, direction = queue[current_element]
        cell = cell_by_coords(y, x)
        current_element += 1
        if used[y][x][direction]:
            continue
        used[y][x][direction] = True
        for new_y, new_x, new_direction in [(y, x, (direction - 1) % 4), (y, x, (direction + 1) % 4),
                                            (*forward_coords(y, x, direction), direction)]:
            if new_direction == direction and WALLS[cell][direction]:
                continue
            if dist[y][x][direction] + 1 < dist[new_y][new_x][new_direction]:
                dist[new_y][new_x][new_direction] = dist[y][x][direction] + 1
                queue.append((new_y, new_x, new_direction))

    return [[min(t) for t in line] for line in dist]


def robots_together(y: int, x: int, steps: int, dist: list) -> bool:
    cell = cell_by_coords(y, x)
    for direction in range(4):
        if WALLS[cell][direction]:
            continue
        new_y, new_x = forward_coords(y, x, direction)
        if dist[new_y][new_x] <= steps:
            return True
    return False


def main():
    y1, x1, dir1 = input().split()
    y1, x1, dir1 = int(y1) - 1, int(x1) - 1, decode_direction(dir1)
    y2, x2, dir2 = input().split()
    y2, x2, dir2 = int(y2) - 1, int(x2) - 1, decode_direction(dir2)

    dist = bfs_with_rotates_on_2d_labyrinth(y2, x2, dir2)

    y, x, direction = y1, x1, dir1
    steps = 0
    while not robots_together(y, x, steps, dist):
        steps += 1
        cell = cell_by_coords(y, x)
        if WALLS[cell][(direction - 1) % 4]:
            if WALLS[cell][direction]:
                direction = (direction + 1) % 4
            else:
                y, x = forward_coords(y, x, direction)
        else:
            direction = (direction - 1) % 4
            if robots_together(y, x, steps, dist):
                break
            else:
                steps += 1
                y, x = forward_coords(y, x, direction)

    print(steps)


if __name__ == "__main__":
    main()
