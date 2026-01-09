import numpy as np
from typing import List, Iterable, Tuple
from scipy.spatial import cKDTree  # pyright: ignore[reportAttributeAccessIssue]

from boid import Boid
from vector_utils import normalize


NeighborData = Iterable[Tuple[int, np.ndarray, float]]
# (neighbor_index, offset_vector, distance)


class Environment:
    def __init__(
        self,
        boids: List[Boid],
        bounds_min: np.ndarray,
        bounds_max: np.ndarray,
        perception_radius: float,
        separation_radius: float,
        max_speed: float,
        min_speed: float,
        weights: dict,
        boundary_margin: float = 1.0,
        boundary_strength: float = 10.0,
    ):
        self.boids = boids
        self.bounds_min = bounds_min.astype(float)
        self.bounds_max = bounds_max.astype(float)

        self.perception_radius = perception_radius
        self.separation_radius = separation_radius
        self.max_speed = max_speed
        self.min_speed = min_speed

        self.weights = weights
        self.boundary_margin = boundary_margin
        self.boundary_strength = boundary_strength

    # ------------------------------------------------------------------
    # Step 1 — snapshot positions
    # ------------------------------------------------------------------
    def _snapshot_positions(self) -> np.ndarray:
        return np.array([boid.position for boid in self.boids], dtype=float)

    # ------------------------------------------------------------------
    # Step 2 — build KD-tree
    # ------------------------------------------------------------------
    def _build_kdtree(self, positions: np.ndarray) -> cKDTree:
        return cKDTree(positions)

    # ------------------------------------------------------------------
    # Step 3 — neighbor index query
    # ------------------------------------------------------------------
    def _query_neighbor_indices(
        self,
        tree: cKDTree,
        position: np.ndarray,
        radius: float,
        self_index: int,
    ) -> List[int]:
        indices = tree.query_ball_point(position, radius)
        return [i for i in indices if i != self_index]

    # ------------------------------------------------------------------
    # Step 4 — neighbor iterator with distances
    # ------------------------------------------------------------------
    def _iter_neighbors_with_distance(
        self,
        boid_index: int,
        positions: np.ndarray,
        neighbor_indices: List[int],
    ) -> NeighborData:
        boid_pos = positions[boid_index]

        for idx in neighbor_indices:
            offset = positions[idx] - boid_pos
            dist = np.linalg.norm(offset)
            if dist > 1e-8:
                yield idx, offset, float(dist)

    # ------------------------------------------------------------------
    # Step 5 — separation force
    # ------------------------------------------------------------------
    def _separation_force_from_neighbors(
        self,
        neighbor_data: NeighborData,
    ) -> np.ndarray:
        force = np.zeros(3)

        for _, offset, dist in neighbor_data:
            if dist < self.separation_radius:
                force -= offset / dist

        return normalize(force) * self.weights.get("separation", 0.0)

    # ------------------------------------------------------------------
    # Step 6 — cohesion force
    # ------------------------------------------------------------------
    def _cohesion_force_from_neighbors(
        self,
        boid_index: int,
        neighbor_data: NeighborData,
        positions: np.ndarray,
    ) -> np.ndarray:
        centers = []

        for idx, _, _ in neighbor_data:
            centers.append(positions[idx])

        if not centers:
            return np.zeros(3)

        center = np.mean(centers, axis=0)
        direction = center - positions[boid_index]
        return normalize(direction) * self.weights.get("cohesion", 0.0)

    # ------------------------------------------------------------------
    # Step 7 — alignment force
    # ------------------------------------------------------------------
    def _alignment_force_from_neighbors(
        self,
        boid_index: int,
        neighbor_data: NeighborData,
    ) -> np.ndarray:
        velocities = []

        for idx, _, _ in neighbor_data:
            velocities.append(self.boids[idx].velocity)

        if not velocities:
            return np.zeros(3)

        avg_velocity = np.mean(velocities, axis=0)
        direction = avg_velocity - self.boids[boid_index].velocity
        return direction * self.weights.get("alignment", 0.0)

    # ------------------------------------------------------------------
    # Boundary force (unchanged, but index-based)
    # ------------------------------------------------------------------
    def _boundary_force(self, position: np.ndarray) -> np.ndarray:
        force = np.zeros(3)

        for i in range(3):
            if position[i] < self.bounds_min[i] + self.boundary_margin:
                force[i] += self.boundary_strength
            elif position[i] > self.bounds_max[i] - self.boundary_margin:
                force[i] -= self.boundary_strength

        return force

    # ------------------------------------------------------------------
    # Step 8 — unified acceleration computation
    # ------------------------------------------------------------------
    def _compute_boid_acceleration(
        self,
        boid_index: int,
        positions: np.ndarray,
        tree: cKDTree,
    ) -> np.ndarray:
        pos = positions[boid_index]

        neighbor_indices = self._query_neighbor_indices(
            tree,
            pos,
            self.perception_radius,
            boid_index,
        )

        neighbor_data = list(
            self._iter_neighbors_with_distance(
                boid_index,
                positions,
                neighbor_indices,
            )
        )

        acc = np.zeros(3)
        acc += self._separation_force_from_neighbors(neighbor_data)
        acc += self._cohesion_force_from_neighbors(boid_index, neighbor_data, positions)
        acc += self._alignment_force_from_neighbors(boid_index, neighbor_data)
        acc += self._boundary_force(pos)

        return acc

    # ------------------------------------------------------------------
    # Step 9 — refactored simulation step
    # ------------------------------------------------------------------
    def step(self, dt: float):
        if not self.boids:
            return

        positions = self._snapshot_positions()
        tree = self._build_kdtree(positions)

        accelerations = [
            self._compute_boid_acceleration(i, positions, tree)
            for i in range(len(self.boids))
        ]

        for boid, acc in zip(self.boids, accelerations):
            boid.apply_acceleration(acc, dt)
            boid.limit_speed(self.min_speed, self.max_speed)
            boid.update_position(dt)

    def get_positions(self) -> np.ndarray:
        """Return a (N, 3) array of boid positions. Returned array is a copy to prevent external mutation."""
        return np.array([boid.position for boid in self.boids], dtype=float)

    def get_velocities(self) -> np.ndarray:
        """Return a (N, 3) array of boid velocities. Returned array is a copy to prevent external mutation."""
        return np.array([boid.velocity for boid in self.boids], dtype=float)

    def get_center_of_mass(self) -> np.ndarray:
        """Return the center of mass of all boids. If no boids exist, returns the origin."""
        if not self.boids:
            return np.zeros(3)
        return np.mean(self.get_positions(), axis=0)
