from mlx import Mlx
import math
import time

mlx = Mlx()
mlx_ptr = mlx.mlx_init()
_, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)

width, height = 19, 21
CELL = 20
win_h = CELL * height
win_w = CELL * width

img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
data, _bpp, sl, fmt = mlx.mlx_get_data_addr(img)

order = "big" if fmt == 1 else "little"

def pack(colour):
    return colour.to_bytes(4, order)

def fill(px, py, w, h, colour):
    # Converte para inteiros
    px = int(px)
    py = int(py)
    w = int(w)
    h = int(h)
    
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

# Variáveis para movimento suave
player_grid_x, player_grid_y = 1, 1  # Posição lógica no grid
player_pixel_x, player_pixel_y = float(1 * CELL), float(1 * CELL)  # Posição real em pixels
target_pixel_x, target_pixel_y = float(1 * CELL), float(1 * CELL)
start_pixel_x, start_pixel_y = float(1 * CELL), float(1 * CELL)
is_moving = False
move_progress = 0.0
move_speed = 8.0  # Células por segundo
current_dir = (0, 0)
next_dir = (0, 0)
last_time = None

# Para animação da boca
mouth_angle = 0
mouth_time = 0

def lerp(a, b, t):
    """Interpolação linear"""
    return a + (b - a) * t

def smoothstep(t):
    """Easing suave"""
    return t * t * (3 - 2 * t)

def draw():
    """Desenha o mapa estático (paredes, pontos)"""
    for y in range(height):
        for x in range(width):
            if matrix[y][x] == 1:
                fill(x * CELL, y * CELL, CELL, CELL, 0xFF0000FF)  # Parede azul
            elif matrix[y][x] == 0:
                # Desenha ponto pequeno no centro
                dot_size = 3
                offset = (CELL - dot_size) // 2
                fill(x * CELL + offset, y * CELL + offset, dot_size, dot_size, 0xFFFFFFFF)

def draw_circle_filled(cx, cy, radius, color):
    """Desenha um círculo preenchido aproximado"""
    cx = int(cx)
    cy = int(cy)
    radius = int(radius)
    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x*x + y*y <= radius*radius:
                fill(cx + x, cy + y, 1, 1, color)

def draw_player():
    """Desenha o Pac-Man na posição atual em pixels com animação da boca"""
    global mouth_angle, mouth_time
    
    # Atualiza animação da boca (abre e fecha)
    mouth_time += 0.016
    mouth_angle = 45 * (math.sin(mouth_time * 15) ** 3)
    
    cx = player_pixel_x + CELL // 2
    cy = player_pixel_y + CELL // 2
    radius = CELL // 2 - 2
    
    # Desenha o corpo amarelo primeiro
    draw_circle_filled(cx, cy, radius, 0xFFFFFF00)
    
    # Desenha a boca (triângulo preto)
    angle_rad = math.radians(current_dir_to_angle())
    mouth_rad = math.radians(mouth_angle / 2)
    
    # Calcula os pontos da boca
    start_angle = angle_rad - mouth_rad
    end_angle = angle_rad + mouth_rad
    
    # Desenha a boca como um setor circular (simplificado)
    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if x*x + y*y <= radius*radius:
                # Calcula o ângulo do ponto
                point_angle = math.atan2(y, x)
                # Ajusta para o mesmo sistema de ângulo
                if point_angle < 0:
                    point_angle += 2 * math.pi
                
                # Verifica se está na boca
                is_in_mouth = False
                if start_angle < end_angle:
                    is_in_mouth = start_angle < point_angle < end_angle
                else:
                    is_in_mouth = point_angle > start_angle or point_angle < end_angle
                
                if is_in_mouth:
                    fill(cx + x, cy + y, 1, 1, 0x00000000)
    
    # Desenha o olho
    eye_offset = 4
    eye_dx = eye_offset if current_dir[0] > 0 else (-eye_offset if current_dir[0] < 0 else 0)
    eye_dy = -3
    eye_x = cx + eye_dx
    eye_y = cy + eye_dy
    fill(int(eye_x) - 1, int(eye_y) - 1, 2, 2, 0x00000000)

def current_dir_to_angle():
    """Converte a direção atual para ângulo em graus"""
    if current_dir == (1, 0):  # Direita
        return 0
    elif current_dir == (-1, 0):  # Esquerda
        return 180
    elif current_dir == (0, -1):  # Cima
        return 270
    elif current_dir == (0, 1):  # Baixo
        return 90
    return 0

def move_to(dx, dy):
    """Inicia movimento suave para uma direção"""
    global next_dir, is_moving
    
    # Se não está movendo, começa imediatamente
    if not is_moving:
        start_move(dx, dy)
    else:
        # Senão, guarda para o próximo movimento
        if (dx, dy) != (0, 0):
            next_dir = (dx, dy)

def start_move(dx, dy):
    """Inicia o movimento na direção especificada"""
    global is_moving, move_progress, current_dir
    global target_pixel_x, target_pixel_y, start_pixel_x, start_pixel_y
    global player_grid_x, player_grid_y
    
    nx = player_grid_x + dx
    ny = player_grid_y + dy
    
    # Verifica colisão com parede
    if 0 <= nx < width and 0 <= ny < height and matrix[ny][nx] != 1:
        is_moving = True
        move_progress = 0.0
        current_dir = (dx, dy)
        
        # Guarda posição inicial e destino
        start_pixel_x = player_pixel_x
        start_pixel_y = player_pixel_y
        target_pixel_x = float(nx * CELL)
        target_pixel_y = float(ny * CELL)
        next_dir = (0, 0)

def update_movement(delta_time):
    """Atualiza a posição do jogador com base no delta time"""
    global is_moving, move_progress, player_grid_x, player_grid_y
    global player_pixel_x, player_pixel_y, start_pixel_y, start_pixel_x
    
    if is_moving:
        # Incrementa o progresso
        move_progress += move_speed * delta_time
        
        if move_progress >= 1.0:
            # Movimento completo
            move_progress = 1.0
            
            # Atualiza a posição lógica no grid
            player_grid_x += current_dir[0]
            player_grid_y += current_dir[1]
            
            # Come o ponto se existir
            if matrix[player_grid_y][player_grid_x] == 0:
                matrix[player_grid_y][player_grid_x] = 2  # Marca como visitado
                # Redesenha a área para remover o ponto
                fill(player_grid_x * CELL, player_grid_y * CELL, CELL, CELL, 0x00000000)
            
            # Sincroniza posição pixel
            player_pixel_x = target_pixel_x
            player_pixel_y = target_pixel_y
            start_pixel_x = player_pixel_x
            start_pixel_y = player_pixel_y
            
            # Move completo
            is_moving = False
            
            # Verifica se tem movimento na fila
            if next_dir != (0, 0):
                start_move(next_dir[0], next_dir[1])
        else:
            # Interpolação suave (usando smoothstep para easing)
            t = smoothstep(move_progress)
            player_pixel_x = lerp(start_pixel_x, target_pixel_x, t)
            player_pixel_y = lerp(start_pixel_y, target_pixel_y, t)

def on_key(keycode, param):
    if keycode == 65361:  # Esquerda
        move_to(-1, 0)
    elif keycode == 65363:  # Direita
        move_to(1, 0)
    elif keycode == 65362:  # Cima
        move_to(0, -1)
    elif keycode == 65364:  # Baixo
        move_to(0, 1)
    elif keycode in (27, 52, 65307):  # ESC
        mlx.mlx_loop_exit(mlx_ptr)

def on_close(param):
    mlx.mlx_loop_exit(mlx_ptr)

def render(param):
    global last_time
    
    # Calcula delta time
    current_time = time.time()
    if last_time is None:
        last_time = current_time
        # Primeiro desenho inicial
        draw()
        mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)
        return
    
    delta_time = min(current_time - last_time, 0.033)  # Limita a 33ms
    last_time = current_time
    
    # Atualiza movimento
    update_movement(delta_time)
    
    # Redesenha apenas a área do jogador (otimização)
    # Para simplificar, redesenhamos o frame inteiro
    fill(0, 0, win_w, win_h, 0x00000000)
    draw()
    draw_player()
    
    # Mostra na janela
    mlx.mlx_put_image_to_window(mlx_ptr, window, img, 0, 0)

# Inicialização
window = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "Pac-Man Smooth")
draw()  # Desenha o mapa inicial

# Configura hooks
mlx.mlx_key_hook(window, on_key, None)
mlx.mlx_hook(window, 33, 0, on_close, None)
mlx.mlx_loop_hook(mlx_ptr, render, None)

print("Use as setas para mover o Pac-Man com animação suave!")
print("Pressione ESC para sair")
mlx.mlx_loop(mlx_ptr)

# Limpeza
mlx.mlx_destroy_image(mlx_ptr, img)
mlx.mlx_destroy_window(mlx_ptr, window)
mlx.mlx_release(mlx_ptr)