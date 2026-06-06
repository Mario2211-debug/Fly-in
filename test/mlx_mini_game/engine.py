# engine.py

from mlx import Mlx

from matrix import matrix, WIDTH, HEIGHT
from player import move
from render import draw, CELL
from input import handle_key

mlx = Mlx()
mlx_ptr = mlx.mlx_init()

win_w = WIDTH * CELL
win_h = HEIGHT * CELL

img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
data, _, sl, fmt = mlx.mlx_get_data_addr(img)

order = "big" if fmt == 1 else "little"

window = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "Jogo")


def on_key(keycode, param):
    handle_key(
        keycode,
        lambda dx, dy: update(dx, dy),
        lambda: mlx.mlx_loop_exit(mlx_ptr)
    )


def update(dx, dy):
    move(matrix, dx, dy)
    draw(matrix, data, sl, win_w, win_h, order)


def render(param):
    mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)


mlx.mlx_key_hook(window, on_key, None)
mlx.mlx_hook(window, 33, 0, lambda p: mlx.mlx_loop_exit(mlx_ptr), None)
mlx.mlx_loop_hook(mlx_ptr, render, None)

draw(matrix, data, sl, win_w, win_h, order)

print("Use as setas para mover")
mlx.mlx_loop(mlx_ptr)


mlx.mlx_destroy_image(mlx_ptr, img)
mlx.mlx_destroy_window(mlx_ptr, window)
mlx.mlx_release(mlx_ptr)