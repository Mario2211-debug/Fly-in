# renderer.py
from mlx import Mlx

CELL = 80
MARGIN = 60
NODE_R = 14  # raio do nó
LINE_W = 2   # espessura da aresta


class Renderer:
    def __init__(self, conf):
        self.conf = conf
        self.needs_render = True
        self.all_hubs = [conf.start] + conf.hubs + [conf.end]

        # calcula bounds
        self.min_x = min(h.x for h in self.all_hubs)
        self.min_y = min(h.y for h in self.all_hubs)
        max_x = max(h.x for h in self.all_hubs)
        max_y = max(h.y for h in self.all_hubs)

        # tamanho da janela
        self.win_w = (max_x - self.min_x) * CELL + MARGIN * 2
        self.win_h = (max_y - self.min_y) * CELL + MARGIN * 2

        # inicializa mlx
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(
            self.ptr, self.win_w, self.win_h, "Fly-in")
        self.img = self.mlx.mlx_new_image(
            self.ptr, self.win_w, self.win_h)
        self.data, self._bpp, self.sl, fmt = \
            self.mlx.mlx_get_data_addr(self.img)

        self.order = "big" if fmt == 1 else "little"

    def to_pixel(self, hx, hy):
        """converte coordenadas do hub para pixeis"""
        px = (hx - self.min_x) * CELL + MARGIN
        py = (hy - self.min_y) * CELL + MARGIN
        return px, py

    def pack(self, colour):
        return colour.to_bytes(4, self.order)

    def fill(self, px, py, w, h, colour):
        packed = self.pack(colour)
        for yy in range(max(0, py), min(self.win_h, py + h)):
            base = yy * self.sl
            for xx in range(max(0, px), min(self.win_w, px + w)):
                off = base + xx * 4
                self.data[off:off + 4] = packed

    def draw_line(self, x0, y0, x1, y1, colour):
        """Bresenham — desenha linha entre dois pontos"""
        packed = self.pack(colour)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            # espessura da linha — desenha LINE_W pixeis à volta
            for tx in range(-LINE_W, LINE_W):
                for ty in range(-LINE_W, LINE_W):
                    nx, ny = x0 + tx, y0 + ty
                    if 0 <= nx < self.win_w and 0 <= ny < self.win_h:
                        off = ny * self.sl + nx * 4
                        self.data[off:off + 4] = packed
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def hub_colour(self, hub):
        """cor do nó baseada no zone_type"""
        if hub == self.conf.start:
            return 0xFF00CC44   # verde
        if hub == self.conf.end:
            return 0xFF00AAFF   # azul
        if hub.zone_type == "restricted":
            return 0xFF0033FF   # vermelho
        if hub.zone_type == "priority":
            return 0xFF00FFCC   # ciano
        return 0xFFCCCCCC       # cinza

    def draw_map(self):
        # fundo
        self.fill(0, 0, self.win_w, self.win_h, 0xFF1A1A1A)

        # arestas
        for conn in self.conf.connections:
            h1 = self.conf.get_hub_by_name(conn.zone1)
            h2 = self.conf.get_hub_by_name(conn.zone2)
            if h1 and h2:
                x1, y1 = self.to_pixel(h1.x, h1.y)
                x2, y2 = self.to_pixel(h2.x, h2.y)
                self.draw_line(x1, y1, x2, y2, 0xFF444444)

        # nós
        for hub in self.all_hubs:
            px, py = self.to_pixel(hub.x, hub.y)
            colour = self.hub_colour(hub)
            self.fill(px - NODE_R, py - NODE_R,
                      NODE_R * 2, NODE_R * 2, colour)

    def draw_labels(self):
        """labels de todos os hubs"""
        for hub in self.all_hubs:
            px, py = self.to_pixel(hub.x, hub.y)
            # nome do hub por baixo do nó
            self.mlx.mlx_string_put(self.ptr, self.win,
                                    px - NODE_R, py + NODE_R + 4,
                                    0xFFFFFF, hub.name)
            # coordenadas por cima
            self.mlx.mlx_string_put(self.ptr, self.win,
                                    px - NODE_R, py - NODE_R - 12,
                                    0xAAAAAA, f"({hub.x},{hub.y})")

    def draw_legend(self):
        """legenda das cores no canto direito"""
        lx = self.win_w - 180
        ly = 20
        spacing = 20

        items = [
            (0xFF00CC44, "start"),
            (0xFF00AAFF, "end / goal"),
            (0xFFCCCCCC, "normal"),
            (0xFF0033FF, "restricted (custo 2)"),
            (0xFF00FFCC, "priority"),
            (0xFFFFAA00, "drone"),
        ]

        self.mlx.mlx_string_put(self.ptr, self.win,
                                lx, ly, 0xFFFFFF, "--- legenda ---")
        for i, (colour, label) in enumerate(items):
            y = ly + (i + 1) * spacing
            self.fill(lx, y, 12, 12, colour)
            self.mlx.mlx_string_put(self.ptr, self.win,
                                    lx + 16, y, 0xFFFFFF, label)

    def draw_buttons(self):
        """botões fullsize e half"""
        # fullsize
        self.fill(10, 10, 80, 22, 0xFF333333)
        self.mlx.mlx_string_put(self.ptr, self.win,
                                18, 15, 0xFFFFFF, "fullsize")
        # half
        self.fill(100, 10, 60, 22, 0xFF333333)
        self.mlx.mlx_string_put(self.ptr, self.win,
                                108, 15, 0xFFFFFF, "half")

    def on_mouse(self, button, x, y, param):
        """deteta clique nos botões"""
        if button == 1:  # botão esquerdo
            # fullsize
            if 10 <= x <= 90 and 10 <= y <= 32:
                self.set_scale(1.0)
            # half
            elif 100 <= x <= 160 and 10 <= y <= 32:
                self.set_scale(0.5)

    def set_scale(self, scale):
        """reconstrói a imagem com nova escala"""
        global CELL, MARGIN
        CELL = int(80 * scale)
        MARGIN = int(60 * scale)

        max_x = max(h.x for h in self.all_hubs)
        max_y = max(h.y for h in self.all_hubs)
        self.win_w = (max_x - self.min_x) * CELL + MARGIN * 2
        self.win_h = (max_y - self.min_y) * CELL + MARGIN * 2

        self.mlx.mlx_destroy_image(self.ptr, self.img)
        self.img = self.mlx.mlx_new_image(self.ptr, self.win_w, self.win_h)
        self.data, self._bpp, self.sl, fmt = \
            self.mlx.mlx_get_data_addr(self.img)
        self.draw_map()

    def render(self, param):
        self.mlx.mlx_put_image_to_window(self.ptr, self.win, self.img, 0, 0)
        self.draw_labels()
        self.draw_legend()
        self.draw_buttons()
        self.needs_render = False  # só desenha uma vez


    def on_close(self, param):
        self.mlx.mlx_loop_exit(self.ptr)

    def run(self):
        self.draw_map()
        self.mlx.mlx_hook(self.win, 33, 0, self.on_close, None)
        self.mlx.mlx_hook(self.win, 4, 0, self.on_mouse, None)  # mouse click
        self.mlx.mlx_loop_hook(self.ptr, self.render, None)
        self.mlx.mlx_loop(self.ptr)
        self.mlx.mlx_destroy_image(self.ptr, self.img)
        self.mlx.mlx_destroy_window(self.ptr, self.win)
        self.mlx.mlx_release(self.ptr)