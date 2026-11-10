from dataclasses import dataclass, field

import numpy as np

TASK_MAX_STEPS = {
    "needle_reach": 50,
    "peg_transfer": 150,
}


def make_env(task: str):
    if task == "needle_reach":
        from surrol.tasks.needle_reach import NeedleReach
        return NeedleReach(render_mode=None)
    if task == "peg_transfer":
        from surrol.tasks.peg_transfer import PegTransfer
        return PegTransfer(render_mode=None)
    raise ValueError(f"Unknown task: {task}")


@dataclass
class EpisodeResult:
    task: str
    policy_type: str
    noise_scale: float
    seed: int
    success: bool = False
    steps_to_success: int | None = None
    rows: list = field(default_factory=list)
    frames: list = field(default_factory=list)


def scripted_action(env, observation, noise_scale: float, rng: np.random.Generator) -> np.ndarray:
    action = np.asarray(env.get_oracle_action(observation), dtype=np.float64)
    if noise_scale > 0:
        action[:3] += rng.normal(0.0, noise_scale, size=3)
    return np.clip(action, -1.0, 1.0)


def run_episode(env, task: str, seed: int, noise_scale: float = 0.0,
                record_frames: bool = False, frame_stride: int = 1) -> EpisodeResult:
    rng = np.random.default_rng(seed)
    env.seed(seed)
    np.random.seed(seed)
    observation = env.reset()
    policy_type = "scripted" if noise_scale == 0 else "noisy_scripted"
    result = EpisodeResult(task=task, policy_type=policy_type, noise_scale=noise_scale, seed=seed)

    if record_frames:
        result.frames.append(env.render("rgb_array"))

    for t in range(TASK_MAX_STEPS[task]):
        action = scripted_action(env, observation, noise_scale, rng)
        tip_state = observation["observation"][:7].copy()
        observation, reward, _, info = env.step(action.copy())
        result.rows.append([t, *tip_state.tolist(), *action[:5].tolist(), float(reward)])

        if record_frames and t % frame_stride == 0:
            result.frames.append(env.render("rgb_array"))

        if info["is_success"]:
            result.success = True
            result.steps_to_success = t + 1
            break

    if record_frames:
        result.frames.append(env.render("rgb_array"))
    return result
