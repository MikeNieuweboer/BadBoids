from ctypes import alignment
from typing import List
from direct.showbase.ShowBase import ShowBase
from boid import Boid
from controller.app_controller import AppController
from environment import Environment
import numpy as np


class BoidApp(ShowBase):
    def __init__(
        self,
        boid_count: int,
        bounds_min: np.ndarray,
        bounds_max: np.ndarray,
        perception_radius: float,
        separation_radius: float,
        max_speed: float,
        min_speed: float,
        alignment: float,
        separation: float,
        cohesion: float,
        boundary_margin: float,
        boundary_force: float,
        seed: int = 43,
    ):
        ShowBase.__init__(self)

        self._gen = np.random.Generator(np.random.PCG64(seed))

        boids = self._create_boids(boid_count, bounds_min, bounds_max)
        weights = {
            "alignment": alignment,
            "cohesion": cohesion,
            "separation": separation,
        }

        env = Environment(
            boids,
            bounds_min,
            bounds_max,
            perception_radius,
            separation_radius,
            max_speed,
            min_speed,
            weights,
            boundary_margin,
            boundary_force,
        )

        self.controller = AppController(env, self)
        self.task_mgr.add(self.controller.update, "update")

    def _create_boids(
        self, boid_count: int, bounds_min: np.ndarray, bounds_max: np.ndarray
    ) -> List[Boid]:
        boids = []
        start_velocity = np.zeros(3)
        for _ in range(boid_count):
            position = self._gen.uniform(bounds_min, bounds_max)
            boids.append(Boid(position, start_velocity))
        return boids


if __name__ == "__main__":
    bound_min = np.array([-60, -60, -60])
    bound_max = np.array([60, 60, 60])
    perception_radius = 15
    separation_radius = 1
    max_speed = 10
    min_speed = 3
    alignment = 0.05
    cohesion = 2
    separation = 0.3
    boundary_force = 10
    boundary_margin = 15
    app = BoidApp(
        300,
        bound_min,
        bound_max,
        perception_radius,
        separation_radius,
        max_speed,
        min_speed,
        alignment,
        separation,
        cohesion,
        boundary_margin,
        boundary_force,
    )
    app.run()
