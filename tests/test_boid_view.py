import unittest
import numpy as np
from panda3d.core import NodePath
import sys

sys.path.append("../src")
from boid_view import BoidView


class TestBoidView(unittest.TestCase):
    def setUp(self):
        self.parent = NodePath("parent")
        self.model = NodePath("model")
        self.view = BoidView(0, self.parent, self.model)

    def test_update_sets_position(self):
        position = np.array([1.0, 2.0, 3.0])
        velocity = np.array([0.0, 1.0, 0.0])

        self.view.update(position, velocity)

        pos = self.view.node.get_pos()
        self.assertAlmostEqual(pos.x, 1.0)
        self.assertAlmostEqual(pos.y, 2.0)
        self.assertAlmostEqual(pos.z, 3.0)

    def test_forward_velocity_orientation(self):
        velocity = np.array([0.0, 1.0, 0.0])

        self.view.set_hpr(velocity)

        h, p, r = self.view.node.get_hpr()
        self.assertAlmostEqual(h, 0.0, places=4)
        self.assertAlmostEqual(p, 0.0, places=4)
        self.assertAlmostEqual(r, 0.0, places=4)

    def test_rightward_velocity_heading(self):
        velocity = np.array([1.0, 0.0, 0.0])

        self.view.set_hpr(velocity)

        h, p, _r = self.view.node.get_hpr()
        self.assertAlmostEqual(h, 90.0, places=4)
        self.assertAlmostEqual(p, 0.0, places=4)

    def test_upward_velocity_pitch(self):
        velocity = np.array([0.0, 0.0, 1.0])

        self.view.set_hpr(velocity)

        h, p, r = self.view.node.get_hpr()
        self.assertAlmostEqual(p, -90.0, places=4)

    def test_zero_velocity_preserves_orientation(self):
        # First set a valid orientation
        velocity = np.array([1.0, 0.0, 0.0])
        self.view.set_hpr(velocity)

        quat_before = self.view.node.get_quat()

        # Now apply zero velocity
        zero_velocity = np.array([0.0, 0.0, 0.0])
        self.view.set_hpr(zero_velocity)

        quat_after = self.view.node.get_quat()

        self.assertTrue(quat_before.almost_equal(quat_after))

    def test_near_zero_velocity_treated_as_zero(self):
        velocity = np.array([1.0, 0.0, 0.0])
        self.view.set_hpr(velocity)

        quat_before = self.view.node.get_quat()

        tiny_velocity = np.array([1e-8, 0.0, 0.0])
        self.view.set_hpr(tiny_velocity)

        quat_after = self.view.node.get_quat()

        self.assertTrue(quat_before.almost_equal(quat_after))
