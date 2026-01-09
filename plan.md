# Plan:
Using the steps from the AlphaCodium tests
## Boid logic
> Reflect on the following problem statement and think of any pitfalls and important implementation details, without starting implementing: A boid simulation is required that allows for the simulation of a 3 dimensional swarm of birds. These boids should be instances of a boid class, which are stored in a list in the Environment class. They all have a velocity which is changed according to the 3 basic rules of separation, cohesion and alignment, which accelerates the boids over a given time delta. Besides these rules, there must also be a bounding box restricting the movement of the boids by exerting a force away from the bounds. Only the simulation logic is required.
- This should give the planning model the space to familiarise itself with the problem.

> Using this internal discussion, think of three different solutions to this problem and summarise their functions, classes and flow in natural language.
- Gave three solution with increasing readability, but decreasing performance.

> Further work out a step by step plan to apply the first solution given that you are developping in python and using numpy for vectors.
- Solution 1 was deemed best for clarity (it actually used the class based system from the problem statement)

> Implement the first steps up untill the environment class definition and add unit tests along the way.
- Only focus on one tightly connected part of the logic to keep gpt from losing the plot.

> Implement the first steps up untill the environment class definition and add unit tests along the way.
- Finish the logic part.

## Rendering
> Reflect on the following problem statement and think of any pitfalls and important implementation details, without starting implementing: given the boid logic, these boids must now be rendered efficiently using the panda3d library in 3d. For this the camera must be controllable and the boids must be represented as blue cones in the direction of their velocity.
- This should give the planning model the space to familiarise itself with the problem.

> Come up with three different possible solutions for this problem and summarise their required functions in natural language, along with the flow of the program.
- Gives options and allows for better agreeance between me and the AI.

> Create a more in depth step by step plan for applying the third solution to the problem, including which changes need to be made to already existing code
- Create a more well explained plan that the AI can follow.

> Implement the first phase of this plan for boid rendering using panda3d, creating unittests where possible
- Implement changes to the environment class to open it up to other files.

> Implement the second phase of this plan for boid rendering using panda3d, creating unittests where possible
- Implement the actual rendering of the boids.

> The lquaternion used in boid_view seems to not have the called function available:
> ERROR: test_nonzero_velocity_returns_quat (test_orientation_math.TestBoidOrientationMath.test_nonzero_velocity_returns_quat)
> ----------------------------------------------------------------------
> Traceback (most recent call last):
>  File "/home/mike/School/Complex/tests/test_orientation_math.py", line 21, in test_nonzero_velocity_returns_quat
>    quat = BoidView.compute_orientation_from_velocity(vel)
>   File "/home/mike/School/Complex/tests/../src/boid_view.py", line 48, in compute_orientation_from_velocity
>     quat.set_from_rotation_mat(
>     ^^^^^^^^^^^^^^^^^^^^^^^^^^
> AttributeError: 'panda3d.core.LQuaternionf' object has no attribute 'set_from_rotation_mat'

> Reflect on why this went wrong and then think of a solution
- Bugfixing


>Create more unittests for the new version of the boid view class:
>import numpy as np
>from panda3d.core import LQuaternionf, NodePath, Vec3
>
>class BoidView:
>    """
>    Represents a single boid visually in Panda3D.
>    """
>
>    def __init__(self, boid_index: int, parent_node: NodePath, model: NodePath):
>        self.index = boid_index
>        self.node = model.copy_to(parent_node)
>        self.node.set_color(0, 0, 1, 1)  # Blue
>        self.last_orientation = LQuaternionf()
>
>    def update(self, position: np.ndarray, velocity: np.ndarray):
>        """
>        Update the NodePath position and orientation based on the boid state.
>        """
>        # Update position
>        self.node.set_pos(*position)
>
>        self.node.set_hpr(velocity)
>
>    def set_hpr(self, velocity: np.ndarray):
>        """
>        Compute the HPR in case the speed is significantly different from 0 and assign it to the node.
>        """
>        speed = np.linalg.norm(velocity)
>        if speed < 1e-5:
>            self.node.set_quat(self.last_orientation)
>            return
>
>        vel_vec = Vec3(*velocity)
>        vel_vec.normalize()
>
>        heading = np.degrees(np.arctan2(vel_vec.x, vel_vec.y))  # Y-forward
>        pitch = -np.degrees(np.arcsin(vel_vec.z))
>        roll = 0.0
>        self.node.set_hpr(heading, pitch, roll)
>        quat = self.node.get_quat()
>        self.last_orientation = quat
- Test the newly generated code

> Ok, now that the boid_view is working, implement the third phase of the plan
- Implement de connecting parts of the code.

## Extra logic
