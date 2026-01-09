import numpy as np
from panda3d.core import LQuaternionf, NodePath


class BoidView:
    """
    Represents a single boid visually in Panda3D.
    """

    def __init__(self, boid_index: int, parent_node: NodePath, model: NodePath):
        self.index = boid_index
        self.node = model.copy_to(parent_node)
        self.node.set_color(0, 0, 1, 1)  # Blue
        self.last_orientation = LQuaternionf()

    def update(self, position: np.ndarray, velocity: np.ndarray):
        """
        Update the NodePath position and orientation based on the boid state.
        """
        # Update position
        self.node.set_pos(*position)

        self.node.look_at(*(position + velocity))
