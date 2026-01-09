import numpy as np


def orbit_position(target, radius, yaw_deg, pitch_deg):
    """
    Compute camera position in a Z-up coordinate system.

    target: (x, y, z)
    returns: (x, y, z)
    """
    yaw = np.radians(yaw_deg)
    pitch = np.radians(pitch_deg)

    x = radius * np.cos(pitch) * np.sin(yaw)
    y = -radius * np.cos(pitch) * np.cos(yaw)
    z = radius * np.sin(pitch)

    return (
        target[0] + x,
        target[1] + y,
        target[2] + z,
    )
