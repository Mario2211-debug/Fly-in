from mlx import Mlx
import time

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
_, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)

width, height = 1280, 720
img = mlx.mlx_new_image(mlx_ptr, width, height)
data, _bpp, sl, fmt = mlx.mlx_get_data_addr(img)
window = mlx.mlx_new_window(mlx_ptr, width, height, "Movimento Smooth")

# Posição do jogador (em pixels, floats para precisão)
player_x, player_y = float(width // 2), float(height // 2)
size = 20

# Velocidade (pixels por segundo)
velocity_x = 0.0
velocity_y = 0.0

# Constantes de movimento
speed = 300.0  # pixels por segundo (movimento horizontal)
gravity = 800.0  # pixels por segundo²
jump_force = -400.0  # pixels por segundo (impulso do pulo)
ground_y = height - size  # chão

# Estados
is_on_ground = False
last_time = time.time()

def pack(colour):
    return colour.to_bytes(4, 'big')

def calculate_delta():
    global last_time
    now = time.time()
    delta = now - last_time
    last_time = now
    return min(delta, 0.033)  # Limita a 33ms para evitar saltos grandes

def on_key(keycode, param):
    global velocity_x
    
    if keycode in (27, 52, 65307):  # ESC
        mlx.mlx_loop_exit(mlx_ptr)
    
    # Movimento horizontal (A/D)
    if keycode == 97:  # A
        velocity_x = -speed
    elif keycode == 100:  # D
        velocity_x = speed
    
    # Pulo (W ou Espaço)
    elif keycode == 119 or keycode == 32:  # W ou Espaço
        jump()

def on_key_release(keycode, param):
    global velocity_x
    
    # Para o movimento horizontal quando soltar A/D
    if keycode == 97:  # A
        if velocity_x < 0:
            velocity_x = 0
    elif keycode == 100:  # D
        if velocity_x > 0:
            velocity_x = 0

def jump():
    global velocity_y, is_on_ground
    
    # Só pode pular se estiver no chão
    if is_on_ground:
        velocity_y = jump_force
        is_on_ground = False

def update():
    global player_x, player_y, velocity_y, is_on_ground
    
    delta = calculate_delta()
    if delta <= 0:
        return
    
    # Atualiza posição horizontal
    player_x += velocity_x * delta
    
    # Aplica gravidade
    velocity_y += gravity * delta
    player_y += velocity_y * delta
    
    # Colisão com o chão
    if player_y >= ground_y:
        player_y = ground_y
        velocity_y = 0
        is_on_ground = True
    
    # Colisão com o teto (opcional)
    if player_y < 0:
        player_y = 0
        if velocity_y < 0:
            velocity_y = 0
    
    # Limita nas bordas laterais
    if player_x < 0:
        player_x = 0
    elif player_x > width - size:
        player_x = width - size

def clear():
    """Limpa a imagem com preto"""
    data[:] = b'\x00' * len(data)

def draw_square(x, y, size, color):
    """Desenha um quadrado na posição (x,y)"""
    x, y = int(x), int(y)
    bpp = _bpp // 8
    packed = pack(color)
    
    for yy in range(max(0, y), min(height, y + size)):
        base = yy * sl
        for xx in range(max(0, x), min(width, x + size)):
            off = base + xx * bpp
            data[off:off + 4] = packed

def draw():
    """Desenha o frame atual"""
    # clear()
    
    # Desenha o chão (opcional)
    ground_color = 0x003366FF  # Azul escuro
    for y in range(int(ground_y), height):
        for x in range(0, width):
            draw_square(x, y, 1, ground_color)
    
    # Desenha o jogador (amarelo para destacar)
    player_color = 0xFFFF00FF if is_on_ground else 0xFFAA00FF
    draw_square(player_x, player_y, size, player_color)
    
    # Mostra informações na janela (via título)
    info = f"Pos: ({int(player_x)}, {int(player_y)}) | Vel: ({velocity_x:.0f}, {velocity_y:.0f}) | Ground: {is_on_ground}"
    # mlx.mlx_set_window_title(mlx_ptr, window, info)

def game_loop(mlx_ptr):
    update()
    draw()
    mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)

def on_close(param):
    mlx.mlx_loop_exit(mlx_ptr)

def main():
    global last_time
    last_time = time.time()
    
    # Hooks
    mlx.mlx_key_hook(window, on_key, None)
    # mlx.mlx_key_release_hook(window, on_key_release, None)  # Importante!
    mlx.mlx_hook(window, 33, 0, on_close, None)
    mlx.mlx_loop_hook(mlx_ptr, game_loop, None)
    
    print("=== Movimento Smooth === ")
    print("A/D - Movimento horizontal")
    print("W/Espaço - Pular")
    print("ESC - Sair")
    
    mlx.mlx_loop(mlx_ptr)
    
    # Limpeza
    mlx.mlx_destroy_image(mlx_ptr, img)
    mlx.mlx_destroy_window(mlx_ptr, window)
    mlx.mlx_release(mlx_ptr)

if __name__ == '__main__':
    main()