from panda3d.core import NodePath, Loader
from boid_view import BoidView
import numpy as np


class SceneView:
    """
    Holds all visual objects of the scene.
    """

    def __init__(self, parent_node: NodePath, num_boids: int, loader: Loader):
        self.root = NodePath("SceneRoot")
        self.root.reparent_to(parent_node)

        # Load shared cone model
        self.model = loader.load_model("../models/cone.egg")
        self.model.set_scale(0.2)

        # Create BoidViews
        self.boid_views = [BoidView(i, self.root, self.model) for i in range(num_boids)]

    def update(self, positions: np.ndarray, velocities: np.ndarray):
        """
        Update all boid visuals.
        """
        for i, boid_view in enumerate(self.boid_views):
            boid_view.update(positions[i], velocities[i])
