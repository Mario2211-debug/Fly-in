# player.py

player_x = 1
player_y = 1


def move(matrix, dx, dy):
    global player_x, player_y

    nx = player_x + dx
    ny = player_y + dy

    # limites do mundo
    if nx < 0 or ny < 0:
        return
    if ny >= len(matrix) or nx >= len(matrix[0]):
        return

    # colisão
    if matrix[ny][nx] == 1:
        return

    # atualizar estado
    matrix[player_y][player_x] = 0
    matrix[ny][nx] = 2

    player_x = nx
    player_y = ny
