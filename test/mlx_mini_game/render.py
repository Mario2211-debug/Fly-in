# render.py

CELL = 50


def pack(colour, order):
    return colour.to_bytes(4, order)


def fill(data, sl, win_w, win_h, px, py, w, h, colour, order):
    packed = pack(colour, order)

    for yy in range(max(0, py), min(win_h, py + h)):
        base = yy * sl
        for xx in range(max(0, px), min(win_w, px + w)):
            off = base + xx * 4
            data[off:off+4] = packed


def draw(matrix, data, sl, win_w, win_h, order):
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):

            val = matrix[y][x]

            px = x * CELL
            py = y * CELL

            if val == 1:
                fill(data, sl, win_w, win_h, px, py, CELL,
                     CELL, 0xFF0000FF, order)
            elif val == 2:
                fill(data, sl, win_w, win_h, px, py, CELL,
                     CELL, 0xFFFF0000, order)
            else:
                fill(data, sl, win_w, win_h, px, py, CELL,
                     CELL, 0xFFFFFFFF, order)