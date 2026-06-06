from mlx import Mlx

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
_, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)


width, heigth = 19, 21
CELL = 20
win_h = CELL * heigth
win_w = CELL * width


img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
data, _bpp, sl, fmt = mlx.mlx_get_data_addr(img)


order = "big" if fmt == 1 else "little"


def pack(colour):
    return colour.to_bytes(4, order)


def fill(px, py, w, h, colour):
    packed = pack(colour)
    for yy in range(max(0, py), min(win_h, py + h)):
        base = yy * sl
        for xx in range(max(0, px), min(win_w, px + w)):
            off = base + xx * 4
            data[off:off + 4] = packed


matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


player_x, player_y = 1, 1


def draw():
    for y in range(heigth):
        for x in range(width):
            if matrix[y][x] == 1:
                fill(x * CELL, y * CELL, CELL, CELL, 0xFF0000FF)
            elif matrix[y][x] == 2:
                fill(x * CELL, y * CELL, CELL, CELL, 0xFFFF0000)
            else:
                fill(x * CELL, y * CELL, CELL, CELL, 0xFFFFFFFF)


def move(dx, dy):
    global player_x, player_y
    nx, ny = player_x + dx, player_y + dy

    if (nx >= 0 and nx <= 21) and (ny >= 0 and ny >= 0) and matrix[ny][nx] != 1:
        matrix[player_y][player_x] = 0
        matrix[ny][nx] = 2
        player_x, player_y = nx, ny
        draw()


def on_key(keycode,  param):
    if keycode == 65361:
        move(-1, 0)
    elif keycode == 65363:
        move(1, 0)
    elif keycode == 65362:
        move(0, -1)
    elif keycode == 65364:
        move(0, 1)
    elif keycode in (27, 52, 65307):
        mlx.mlx_loop_exit(mlx_ptr)


def on_close(param):
    mlx.mlx_loop_exit(mlx_ptr)


def render(param):
    mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)


window = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "Jogo")


draw()
mlx.mlx_key_hook(window, on_key, None)
mlx.mlx_hook(window, 33, 0, on_close, None)

mlx.mlx_loop_hook(mlx_ptr, render, None)

print("Use as setas para mover")
mlx.mlx_loop(mlx_ptr)


mlx.mlx_destroy_image(mlx_ptr, img)
mlx.mlx_destroy_window(mlx_ptr, window)
mlx.mlx_release(mlx_ptr)
