# test_vector_utils.py
import unittest
import numpy as np
import sys

sys.path.append("../src")
from vector_utils import norm, normalize, limit_magnitude


class TestVectorUtils(unittest.TestCase):
    def test_norm(self):
        v = np.array([3.0, 4.0, 0.0])
        self.assertAlmostEqual(norm(v), 5.0)

    def test_normalize(self):
        v = np.array([0.0, 3.0, 4.0])
        n = normalize(v)
        self.assertAlmostEqual(norm(n), 1.0)

    def test_normalize_zero_vector(self):
        v = np.zeros(3)
        n = normalize(v)
        np.testing.assert_array_equal(n, np.zeros(3))

    def test_limit_magnitude(self):
        v = np.array([10.0, 0.0, 0.0])
        limited = limit_magnitude(v, 5.0)
        self.assertAlmostEqual(norm(limited), 5.0)

    def test_limit_magnitude_no_change(self):
        v = np.array([3.0, 4.0, 0.0])
        limited = limit_magnitude(v, 10.0)
        np.testing.assert_array_equal(limited, v)


if __name__ == "__main__":
    unittest.main()
