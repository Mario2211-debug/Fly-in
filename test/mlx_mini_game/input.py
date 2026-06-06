# input.py

def handle_key(keycode, move_fn, exit_fn):
    if keycode == 65361:
        move_fn(-1, 0)
    elif keycode == 65363:
        move_fn(1, 0)
    elif keycode == 65362:
        move_fn(0, -1)
    elif keycode == 65364:
        move_fn(0, 1)
    elif keycode in (27, 52, 65307):
        exit_fn()