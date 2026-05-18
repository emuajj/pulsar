import tkinter as tk
import numpy as np
from knob import Knob


class GUI:
    def __init__(self, state):
        self.state = state

        self.root = tk.Tk()
        self.root.title("Pulsar Synth")

        # -------------------
        # KNOB (F0)
        # -------------------
        self.k1 = Knob(
            self.root,
            min_val=5.0,
            max_val=30.0,
            value=state.f0,
            label="F0 (Hz)",
            callback=self.set_f0
        )
        self.k1.pack()

        # -------------------
        # CANVAS 3D
        # -------------------
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()

        # rotation user
        self.angle_x = 0.0
        self.angle_y = 0.0

        self.last_x = 0
        self.last_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.draw()

    # -------------------
    # KNOB
    # -------------------
    def set_f0(self, v):
        self.state.f0 = v

    # -------------------
    # mouse control
    # -------------------
    def on_down(self, e):
        self.last_x = e.x
        self.last_y = e.y

    def on_drag(self, e):
        dx = e.x - self.last_x
        dy = e.y - self.last_y

        self.angle_y += dx * 0.01
        self.angle_x += dy * 0.01

        self.last_x = e.x
        self.last_y = e.y

        self.update_state()
        self.draw()

    # -------------------
    # ROTATION
    # -------------------
    def rotate(self, v):
        x, y, z = v

        # Y
        cy, sy = np.cos(self.angle_y), np.sin(self.angle_y)
        x, z = cy*x + sy*z, -sy*x + cy*z

        # X
        cx, sx = np.cos(self.angle_x), np.sin(self.angle_x)
        y, z = cx*y - sx*z, sx*y + cx*z

        return np.array([x, y, z])

    # -------------------
    # PERSPECTIVE PROJECTION
    # -------------------
    def project(self, v):
        scale = 180
        distance = 3.0

        z = v[2] + distance
        f = scale / z

        x = 200 + v[0] * f
        y = 200 - v[1] * f

        return x, y

    # -------------------
    # PHYSICS LINK (audio)
    # -------------------
    def update_state(self):
        L = 1.0

        p1 = self.rotate(np.array([0, 0, -L/2]))
        p2 = self.rotate(np.array([0, 0,  L/2]))

        x1, y1 = self.project(p1)
        x2, y2 = self.project(p2)

        visible_length = np.hypot(x2 - x1, y2 - y1)

        max_len = 220.0  # tuning constant
        intensity = visible_length / max_len

        self.state.view_intensity = float(np.clip(intensity, 0.0, 1.0))

    # -------------------
    # DRAW SYSTEM
    # -------------------
    def draw(self):
        self.canvas.delete("all")

        L = 1.0

        spin_p1 = np.array([0, 0, -L/2])
        spin_p2 = np.array([0, 0,  L/2])

        tilt = 0.6

        def mag(v):
            x, y, z = v
            cy, sy = np.cos(tilt), np.sin(tilt)
            y, z = cy*y - sy*z, sy*y + cy*z
            return np.array([x, y, z])

        mag_p1 = mag(np.array([0, 0, -L/2]))
        mag_p2 = mag(np.array([0, 0,  L/2]))

        spin_p1 = self.rotate(spin_p1)
        spin_p2 = self.rotate(spin_p2)

        mag_p1 = self.rotate(mag_p1)
        mag_p2 = self.rotate(mag_p2)

        x1, y1 = self.project(spin_p1)
        x2, y2 = self.project(spin_p2)

        mx1, my1 = self.project(mag_p1)
        mx2, my2 = self.project(mag_p2)

        self.canvas.create_line(x1, y1, x2, y2, fill="cyan", width=3)
        self.canvas.create_line(mx1, my1, mx2, my2, fill="orange", width=2)

        self.canvas.create_oval(190, 190, 210, 210, outline="white")

    # -------------------
    def run(self):
        self.root.mainloop()