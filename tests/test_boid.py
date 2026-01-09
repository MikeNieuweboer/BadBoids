# test_boid.py
import unittest
import numpy as np
import sys

sys.path.append("../src")
from boid import Boid


class TestBoid(unittest.TestCase):
    def test_apply_acceleration(self):
        b = Boid(position=np.zeros(3), velocity=np.zeros(3))
        acceleration = np.array([1.0, 0.0, 0.0])
        b.apply_acceleration(acceleration, dt=2.0)

        np.testing.assert_array_equal(b.velocity, np.array([2.0, 0.0, 0.0]))

    def test_limit_speed(self):
        b = Boid(position=np.zeros(3), velocity=np.array([10.0, 0.0, 0.0]))
        b.limit_speed(5.0)
        self.assertAlmostEqual(float(np.linalg.norm(b.velocity)), 5.0)

    def test_update_position(self):
        b = Boid(position=np.zeros(3), velocity=np.array([1.0, 2.0, 3.0]))
        b.update_position(dt=2.0)

        np.testing.assert_array_equal(b.position, np.array([2.0, 4.0, 6.0]))

    def test_full_physics_step(self):
        b = Boid(position=np.zeros(3), velocity=np.zeros(3))
        b.apply_acceleration(np.array([1.0, 0.0, 0.0]), dt=1.0)
        b.limit_speed(10.0)
        b.update_position(dt=1.0)

        np.testing.assert_array_equal(b.position, np.array([1.0, 0.0, 0.0]))


if __name__ == "__main__":
    unittest.main()
