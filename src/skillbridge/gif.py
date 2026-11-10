from pathlib import Path

import imageio.v2 as imageio
import numpy as np


def save_gif(frames: list, path: Path, fps: int = 8, downscale: int = 2) -> Path:
    small_frames = [np.asarray(frame)[::downscale, ::downscale, :3].astype(np.uint8) for frame in frames]
    imageio.mimsave(path, small_frames, duration=1000 / fps, loop=0)
    return path
