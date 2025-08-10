class MenuScene:
    def start(self) -> None:
        print("Menu Scene started")

    def render(self) -> None:
        ctx = self.engine.ctx
        ctx.fillStyle = "red"
        ctx.fillRect(50, 50, 200, 150)
