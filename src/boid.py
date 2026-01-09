# boid.py
from math import isclose
import numpy as np


class Boid:
    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        self.position = position.astype(float)
        self.velocity = velocity.astype(float)

    def apply_acceleration(self, acceleration: np.ndarray, dt: float):
        """Update velocity using acceleration and time delta."""
        self.velocity += acceleration * dt

    def limit_speed(self, min_speed: float, max_speed: float):
        """Clamp velocity magnitude."""
        norm = float(np.linalg.norm(self.velocity))
        if isclose(norm, 0):
            return

        if norm < min_speed:
            self.velocity = self.velocity / norm * min_speed
        elif norm > max_speed:
            self.velocity = self.velocity / norm * max_speed

    def update_position(self, dt: float):
        """Advance position using current velocity."""
        self.position += self.velocity * dt
