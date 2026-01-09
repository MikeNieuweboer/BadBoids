# vector_utils.py
import numpy as np
import sys

sys.path.append("../src")


def norm(vec: np.ndarray) -> float:
    """Return Euclidean norm of a vector."""
    return float(np.linalg.norm(vec))


def normalize(vec: np.ndarray) -> np.ndarray:
    """Return normalized vector, or zero vector if magnitude is zero."""
    n = np.linalg.norm(vec)
    if n == 0.0:
        return np.zeros_like(vec)
    return vec / n


def limit_magnitude(vec: np.ndarray, max_magnitude: float) -> np.ndarray:
    """Clamp vector magnitude to max_magnitude."""
    n = np.linalg.norm(vec)
    if n > max_magnitude:
        return (vec / n) * max_magnitude
    return vec
