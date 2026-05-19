import tkinter as tk
import numpy as np
import time
from knob import Knob


class GUI:
    def __init__(self, state):
        self.state = state

        self.root = tk.Tk()
        self.root.title("Pulsar Synth")

        # tiempo global para animaciones
        self.t0 = time.time()

        # -------------------
        # KNOB F0
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
        # NOISE
        # -------------------
        self.k2 = Knob(
            self.root,
            min_val=0,
            max_val=1,
            value=state.noise_level,
            label="Noise Level",
            callback=self.set_noise_level
        )
        self.k2.pack()

        # -------------------
        # MAGNETIC TILT
        # -------------------
        self.k3 = Knob(
            self.root,
            min_val=0.0,
            max_val=np.pi/2,
            value=state.magnetic_tilt,
            label="Magnetic Tilt",
            callback=self.set_tilt
        )
        self.k3.pack()

        # -------------------
        # CANVAS
        # -------------------
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()

        # cámara
        self.angle_x = 0.0
        self.angle_y = 0.0

        self.last_x = 0
        self.last_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_down)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.running = True
        self.animate()
        
    def animate(self):
        if not self.running:
            return

        self.update_state()
        self.draw()

        self.root.after(16, self.animate)  # ~60 FPS

    # -------------------
    # CALLBACKS
    # -------------------
    def set_f0(self, v):
        self.state.f0 = v

    def set_noise_level(self, v):
        self.state.noise_level = v

    def set_tilt(self, v):
        self.state.magnetic_tilt = v

    # -------------------
    # INPUT
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

    # -------------------
    # ROTATION 3D
    # -------------------
    def rotate(self, v):
        x, y, z = v

        cy, sy = np.cos(self.angle_y), np.sin(self.angle_y)
        x, z = cy*x + sy*z, -sy*x + cy*z

        cx, sx = np.cos(self.angle_x), np.sin(self.angle_x)
        y, z = cx*y - sx*z, sx*y + cx*z

        return np.array([x, y, z])

    # -------------------
    # PROJECTION
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
    # PHYSICS LINK (intensity)
    # -------------------
    def update_state(self):
        L = 1.0

        p1 = self.rotate(np.array([0, 0, -L/2]))
        p2 = self.rotate(np.array([0, 0,  L/2]))

        x1, y1 = self.project(p1)
        x2, y2 = self.project(p2)

        visible_length = np.hypot(x2 - x1, y2 - y1)

        self.state.view_intensity = float(
            np.clip(visible_length / 220.0, 0.0, 1.0)
        )

    # -------------------
    # DRAW
    # -------------------
    def draw(self):
        self.canvas.delete("all")

        L = 1.0

        # -------------------
        # EJES
        # -------------------
        spin_p1 = self.rotate(np.array([0, 0, -L/2]))
        spin_p2 = self.rotate(np.array([0, 0,  L/2]))

        tilt = self.state.magnetic_tilt

        def mag(v):
            x, y, z = v
            cy, sy = np.cos(tilt), np.sin(tilt)
            y, z = cy*y - sy*z, sy*y + cy*z
            return np.array([x, y, z])

        mag_p1 = self.rotate(mag(np.array([0, 0, -L/2])))
        mag_p2 = self.rotate(mag(np.array([0, 0,  L/2])))

        x1, y1 = self.project(spin_p1)
        x2, y2 = self.project(spin_p2)

        mx1, my1 = self.project(mag_p1)
        mx2, my2 = self.project(mag_p2)

        self.canvas.create_line(x1, y1, x2, y2, fill="cyan", width=3)
        self.canvas.create_line(mx1, my1, mx2, my2, fill="orange", width=2)

        # -------------------
        # CENTRO
        # -------------------
        self.canvas.create_oval(190, 190, 210, 210, outline="white")

        # -------------------
        # 🌌 OBJETO ORBITANTE
        # -------------------
        t = time.time() - self.t0

        omega = 2 * np.pi * self.state.f0
        theta = omega * t
    
        radius = 0.6

        orbit_local = np.array([
            radius * np.cos(theta),
            radius * np.sin(theta),
            0
        ])

        orbit_world = self.rotate(orbit_local)
        x, y = self.project(orbit_world)

        self.canvas.create_oval(
            x - 4, y - 4,
            x + 4, y + 4,
            fill="white",
            outline=""
        )

    # -------------------
    def run(self):
        self.root.mainloop()