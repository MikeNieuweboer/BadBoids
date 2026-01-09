from panda3d.core import ClockObject
from scene_view import SceneView
from controller.orbit_camera_controller import OrbitCameraController
from panda3d.core import WindowProperties


class AppController:
    """
    Coordinates simulation, rendering, and camera updates.
    """

    def __init__(self, environment, base):
        self.environment = environment
        self.base = base

        self.scene_view = SceneView(
            parent_node=base.render,
            num_boids=len(environment.boids),
            loader=base.loader,
        )

        self.camera_controller = OrbitCameraController(
            camera=base.camera,
        )

        self.is_orbiting = False
        self._last_mouse_pos = None

        props = WindowProperties()
        props.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(props)

        base.accept("mouse1", self.start_orbit)
        base.accept("mouse1-up", self.stop_orbit)

        base.accept("wheel_up", lambda: self.camera_controller.zoom(-1))
        base.accept("wheel_down", lambda: self.camera_controller.zoom(1))
        self.clock = ClockObject.get_global_clock()

    def update(self, task):
        dt = self.clock.get_dt()
        dt = min(dt, 0.05)  # Clamp for stability

        # 1. Step simulation
        self.environment.step(dt)

        # 2. Fetch simulation state
        positions = self.environment.get_positions()
        velocities = self.environment.get_velocities()
        center = self.environment.get_center_of_mass()

        # 3. Update visuals
        self.scene_view.update(positions, velocities)

        # 4. Handle mouse delta (ALWAYS READ MOUSE)
        if self.base.mouseWatcherNode.has_mouse():
            mouse = self.base.mouseWatcherNode.get_mouse()

            if self._last_mouse_pos is not None:
                dx = mouse.x - self._last_mouse_pos[0]
                dy = mouse.y - self._last_mouse_pos[1]

                if self.is_orbiting:
                    # scale factor tuned empirically
                    self.camera_controller.rotate(
                        dx * self.base.win.getXSize(), dy * self.base.win.getYSize()
                    )

            self._last_mouse_pos = (mouse.x, mouse.y)
        self.camera_controller.set_target(center)
        self.camera_controller.update()
        return task.cont

    def start_orbit(self):
        self.is_orbiting = True
        self._last_mouse_pos = None

    def stop_orbit(self):
        self.is_orbiting = False
        self._last_mouse_pos = None
