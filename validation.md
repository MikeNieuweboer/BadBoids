# Validation

## Behavior
By testing out several different configurations (by changing the inputs in src/main.py), it can be seen that each of the parameters cause their expected behavior, namely:
- **Alignment**: When all other parameters are off, this leads to nearby boids pointing in the exact same direction and trying to outcompete eachothers velocities. That they move in the same direction does, however, not directly lead to the classic masses of birds that can be observed, as it doesn't account for the cohesion.
- **Cohesion**: When increasing this parameter, along with the perception radius, this causes all boids to converge to the center of the bounding box, as expected.
- **Separation**: In the a properly configured simulation (, which already shows the swarm like behavior), the separation seemingly has the smallest effect of the three rules, but when focussing solely on this rule, along with an increase separation radius, it clearly causes the boids to move away from eachother, leading to a situation that could be best described as deterministic chaos.

Using the current parameters, even if the boids start at random locations, they start forming their own flocks, which together form complex patterns, especially at the borders, where there are even more mechanics at play.

## Parameter exploration
- Boid Count: fewer boids means smaller flocks and less interaction in the space.
- Perception radius: smaller radius leads to more independent behavior, while larger radius leads to flocking around the center of the bounding box.
- Maximum speed: higher maximum speed currently leads to increased importance of the alignment (as it scales with speed), causing more independent behavior.
- Rule weights: as previously explained, more cohesion means more drift towards the local center, more alignment means a larger tendency towars the same direction, but also more of a pong effect, where the boids follow a straight line bouncing from border to border. Lastly a larger separation value leads to the boids having a larger tendency to separate and a more extreme reaction when they meet/get close.
- Boundary conditions (not implemented in this version, but was of importance in my own rust based implementation): a periodic boundary leads to less agitation and therefore causes the boids to continuously go in one direction. The repulsive boundaries cause more agitations and therefore leads to more complex behavior.

## Reflection
I still by all accounts think that AI is a scourge to the world and would like to minimize my ussage of it, but implementing a 3d boid simulation using an unknown graphics library within a couple of days would not have been possible without it.

The Alphacodium structure of reflecting on the problem, generating solutions, implementing the best ones and iterating based on generated tests, worked surprisingly well. The implementation of the boid logic and its later upgrade with the kdTree worked in one try and even though the free version of chatGPT was used (the one without an account, requiring manual copy and paste to a website), I can not think of any improvements which would have led to a better workflow, except for maybe giving more information about the file structure, as I had to manually alter the imports to work.

The rendering part was however where it failed, as there were very few meaningfull unittests that could be made for this part and the Panda3D library is likely used so little that it oftentimes did not know what to do. This meant that it would already start hallucinating all kinds of different pitfalls in the reflection stage, leading to complicated and subpar code in the code generation phase. For debugging I would then oftentimes repeat either the same flow, or just ask a singular question stating the problem at hand, such as incorrect directions of the boid's cones, which did work most of the times, but would oftentimes still be unnecessarily complex.

For future improvements of this workflow, I should likely create templates for each phase, which contain even more limits to what the LLM should do in that phase, along with using a better agentic model that can actually use tools to understand the project and can be given more specific instructions (, such as having a architect, documentation and implementation model).

As to whether having the requirements stated beforehand changed how I worked, I could not say, as I normally do not work with AI and as a computer scientist, I have had the chance to already develop an intuition for how to develop and structure code, making such a plan less relevant.
