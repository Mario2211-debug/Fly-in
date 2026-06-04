from mlx import Mlx


mlx = Mlx()
mlx_ptr = mlx.mlx_init()
window = mlx.mlx_new_window(mlx_ptr, 800, 600, "Minha janela", )


def render(param):
    # mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)
    pass


def on_key(keycode, _params) -> None:
    if keycode in (52, 27, 65307):
        mlx.mlx_loop_exit(mlx_ptr)


def on_close(_param: object) -> None:
    mlx.mlx_loop_exit(mlx_ptr)


mlx.mlx_key_hook(window, on_key, None)
mlx.mlx_hook(window, 33, 0, on_close, None)

mlx.mlx_loop_hook(mlx_ptr, render, None)
mlx.mlx_loop(mlx_ptr)

mlx.mlx_destroy_window(mlx_ptr, window)
mlx.mlx_release(mlx_ptr)
