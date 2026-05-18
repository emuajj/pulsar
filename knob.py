import tkinter as tk
import math

class Knob(tk.Canvas):
    def __init__(self, master, min_val, max_val, callback=None, label="", value=None,step=None, **kwargs):

        super().__init__(master, width=120, height=140, **kwargs)

        self.configure(bg="black", highlightthickness=0)

        self.min_val = min_val
        self.max_val = max_val
        self.callback = callback
        self.label = label
        self.step = step

        self.value = value if value is not None else min_val
        self.center = 60
        self.radius = 45

        self.angle = -135
        
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Button-1>", self.drag)
        
        self.draw()

    def value_to_angle(self, value):
        return -135 + (value - self.min_val) / (self.max_val - self.min_val) * 270

    def drag(self, event):
        dx = event.x - self.center
        dy = event.y - self.center

        angle = math.degrees(math.atan2(-dy, dx))
        angle = max(-135, min(135, angle))

        self.angle = angle

        ratio = (angle + 135) / 270
        self.value = self.min_val + ratio * (self.max_val - self.min_val)

        # optional step quantization
        if self.step:
            self.value = round(self.value / self.step) * self.step

        if self.callback:
            self.callback(self.value)

        self.draw()

    def draw(self):
        self.delete("all")

        self.create_oval(10, 10, 110, 110, outline="#666", width=2)

        rad = math.radians(self.angle)
        x = self.center + self.radius * math.cos(rad)
        y = self.center - self.radius * math.sin(rad)

        self.create_line(self.center, self.center, x, y, fill="red", width=3)

        self.create_text(60, 125, text=self.label, fill="white")

        self.create_text(
            60, 90,
            text=f"{self.value:.3e}" if abs(self.value) < 0.01 else f"{self.value:.3f}",
            fill="white",
            font=("Arial", 10)
        )