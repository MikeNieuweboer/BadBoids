import unittest
import numpy as np
import sys

sys.path.append("../src")

from boid import Boid
from environment import Environment


class TestEnvironmentStep(unittest.TestCase):
    def test_step_moves_boids(self):
        b1 = Boid(np.array([0, 0, 0]), np.array([1, 0, 0]))

        env = Environment(
            boids=[b1],
            bounds_min=np.array([-10, -10, -10]),
            bounds_max=np.array([10, 10, 10]),
            perception_radius=5.0,
            separation_radius=1.0,
            max_speed=5.0,
            weights={},
        )

        env.step(dt=1.0)
        self.assertGreater(b1.position[0], 0)

    def test_step_respects_max_speed(self):
        b = Boid(np.array([0, 0, 0]), np.array([100, 0, 0]))

        env = Environment(
            boids=[b],
            bounds_min=np.array([-10, -10, -10]),
            bounds_max=np.array([10, 10, 10]),
            perception_radius=5.0,
            separation_radius=1.0,
            max_speed=5.0,
            weights={},
        )

        env.step(dt=1.0)
        self.assertLessEqual(np.linalg.norm(b.velocity), 5.0)
