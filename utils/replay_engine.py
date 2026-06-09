class ReplayEngine:
    def __init__(self, history):
        self.history = history or []
        self.index = 0
        self.paused = True
        self.speed = 1

    def current(self):
        if not self.history:
            return None
        self.index = max(0, min(self.index, len(self.history) - 1))
        return self.history[self.index]

    def next(self):
        if self.index < len(self.history) - 1:
            self.index += 1

    def prev(self):
        if self.index > 0:
            self.index -= 1

    def toggle(self):
        self.paused = not self.paused

    def restart(self):
        self.index = 0

    def update(self):
        if not self.paused:
            for _ in range(self.speed):
                self.next()