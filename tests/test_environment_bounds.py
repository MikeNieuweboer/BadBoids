import unittest
import numpy as np
import sys

sys.path.append("../src")
from boid import Boid
from environment import Environment


class TestBoundaryForce(unittest.TestCase):
    def test_boundary_pushes_inward(self):
        b = Boid(np.array([0.1, 5, 5]), np.zeros(3))

        env = Environment(
            boids=[b],
            bounds_min=np.zeros(3),
            bounds_max=np.ones(3) * 10,
            perception_radius=5.0,
            separation_radius=1.0,
            max_speed=10.0,
            weights={},
            boundary_margin=1.0,
            boundary_strength=5.0,
        )

        force = env._boundary_force(b)
        self.assertGreater(force[0], 0)
