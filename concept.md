# Concepts
As I am currently busy implementing a [terminal boid swarm](https://github.com/MikeNieuweboer/cli-boids) using rust, I will use my own knowledge as the source:

## The three flocking rules
A boid swarm is a set of points which move using at least the following three rules:
- **Separation**: any boid tries to evade any of the other boids that come within its avoidance range.
- **Alignment**: any boid tries to match its velocity to that of the boids around it.
- **Cohesion**: any boid accelerates towards the center of the boids within a certain range around it.

## Key parameters and their role:
Each of the parameters influence the simulation in its own way:
- **Boid Count**: By increasing the number of boids, each of the boid masses will likely grow in size.
- **Perception Radius**: The larger the radius, the higher the chance of all boids coming together into one large mass.
- **Maximum Speed**: Really says it all, doesn't it?
- **Rule Weights**: Can change the behavior of the boids from barely moving when all weights are low, to rapidly accelerating with a high alignment value, or circling a point when there is only cohesion.
- **Boundary Conditions**: These conditions are some of the largest factors in introducing more unpredictable behaviors, as in case the boundaries loop around, the boids will likely only every move in one general direction, while having boundaries that force the boids back will create the interesting patterns that one can see online.

## Emergent Behavior:
The complex behavior that can be seen here will likely/hopefully mimic bird swarms, where the boids start forming these dynamic masses that move through the space, in which case we can conclude that the simulation is likely working.

## Data Structure and Algorithm Flow:
As we are using an object oriented programming language, we can represent boids as objects of the boid class, which in the beginning only contain a position and velocity in 3D space. These boids are then stored in a World object, which at first only contains a list, but can later be extended to use the kd-tree from scipy. This object allows for the gathering of all boids that need to be checked against based on the perception and avoidance radii. The boids that are returned from this object will all be checked for whether they are close enough and if they are, the correct rule will be applied to change their velocity and their velocity.

For the visualisation, Panda3D will be used as a performing alternative to 3D visualisations such as matplotlib.
