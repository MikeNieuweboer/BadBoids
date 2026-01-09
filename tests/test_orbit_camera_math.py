import unittest
import numpy as np
from panda3d.core import NodePath
import sys

sys.path.append("../")
from controller.orbit_camera_controller import OrbitCameraController


class DummyMouseWatcher:
    def has_mouse(self):
        return False


class TestOrbitCameraMath(unittest.TestCase):
    def setUp(self):
        self.camera = NodePath("camera")
        self.controller = OrbitCameraController(
            camera=self.camera, mouse_watcher=DummyMouseWatcher(), radius=10.0
        )

    def test_camera_position_yaw_zero_pitch_zero(self):
        self.controller.yaw = 0.0
        self.controller.pitch = 0.0
        self.controller.set_target(np.array([0, 0, 0]))

        self.controller._update_camera_transform()

        pos = self.camera.get_pos()
        self.assertAlmostEqual(pos.x, 0.0, places=4)
        self.assertAlmostEqual(pos.y, -10.0, places=4)
        self.assertAlmostEqual(pos.z, 0.0, places=4)

    def test_camera_position_pitch_90(self):
        self.controller.yaw = 0.0
        self.controller.pitch = 90.0
        self.controller.set_target(np.array([0, 0, 0]))

        self.controller._update_camera_transform()

        pos = self.camera.get_pos()
        self.assertAlmostEqual(pos.z, 10.0, places=4)
