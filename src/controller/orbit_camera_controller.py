from panda3d.core import Vec3, NodePath
from controller.camera_math import orbit_position


class OrbitCameraController:
    def __init__(
        self,
        camera: NodePath,
        radius=20.0,
        sensitivity=0.2,
        zoom_sensitivity=2.0,
        min_pitch=-80,
        max_pitch=80,
        min_radius=75.0,
        max_radius=200.0,
    ):
        self.camera = camera

        self.yaw = 0.0
        self.pitch = -20.0
        self.radius = radius

        self.sensitivity = sensitivity
        self.zoom_sensitivity = zoom_sensitivity

        self.min_pitch = min_pitch
        self.max_pitch = max_pitch
        self.min_radius = min_radius
        self.max_radius = max_radius

        self.target = Vec3(0, 0, 0)

    def set_target(self, target):
        self.target = Vec3(*target)

    # ---- INPUT HOOKS ----

    def rotate(self, dx, dy):
        self.yaw -= dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch))

    def zoom(self, direction):
        self.radius -= direction * self.zoom_sensitivity
        self.radius = max(self.min_radius, min(self.max_radius, self.radius))

    # ---- FRAME UPDATE ----

    def update(self):
        x, y, z = orbit_position(
            self.target,
            self.radius,
            self.yaw,
            self.pitch,
        )
        self.camera.set_pos(x, y, z)
        self.camera.look_at(self.target)
