import unittest
import numpy as np
from boid import Boid
from environment import Environment


class TestEnvironmentStateAccess(unittest.TestCase):
    def setUp(self):
        self.b1 = Boid(np.array([1, 2, 3]), np.array([0.1, 0.2, 0.3]))
        self.b2 = Boid(np.array([4, 5, 6]), np.array([0.4, 0.5, 0.6]))

        self.env = Environment(
            boids=[self.b1, self.b2],
            bounds_min=np.zeros(3),
            bounds_max=np.ones(3) * 10,
            perception_radius=5.0,
            separation_radius=2.0,
            max_speed=10.0,
            weights={},
        )

    def test_get_positions_shape_and_values(self):
        positions = self.env.get_positions()

        self.assertEqual(positions.shape, (2, 3))
        np.testing.assert_array_equal(positions, np.array([[1, 2, 3], [4, 5, 6]]))

    def test_get_velocities_shape_and_values(self):
        velocities = self.env.get_velocities()

        self.assertEqual(velocities.shape, (2, 3))
        np.testing.assert_array_equal(
            velocities, np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])
        )

    def test_returned_arrays_are_copies(self):
        positions = self.env.get_positions()
        positions[0, 0] = 999

        # Internal boid state must remain unchanged
        self.assertEqual(self.b1.position[0], 1)

    def test_center_of_mass(self):
        center = self.env.get_center_of_mass()
        np.testing.assert_array_equal(center, np.array([2.5, 3.5, 4.5]))

    def test_center_of_mass_empty_environment(self):
        empty_env = Environment(
            boids=[],
            bounds_min=np.zeros(3),
            bounds_max=np.ones(3),
            perception_radius=5.0,
            separation_radius=2.0,
            max_speed=10.0,
            weights={},
        )

        np.testing.assert_array_equal(empty_env.get_center_of_mass(), np.zeros(3))


if __name__ == "__main__":
    unittest.main()
