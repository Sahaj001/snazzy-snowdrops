class Engine:
    def __init__(self, width, height, canvas) -> None:
        self.canvas = canvas
        self.ctx = self.canvas.getContext("2d")
        self.canvas.width = width
        self.canvas.height = height
        self.current_scene = None

    def set_scene(self, scene) -> None:
        self.current_scene = scene
        self.current_scene.engine = self

    def run(self) -> None:
        if self.current_scene:
            self.current_scene.start()
            self.current_scene.render()
