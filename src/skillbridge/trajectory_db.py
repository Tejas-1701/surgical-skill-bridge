from pathlib import Path

import duckdb
import pandas as pd

from skillbridge.config import database_path, schema_path
from skillbridge.rollout import EpisodeResult

TIMESTEP_COLUMNS = [
    "t", "tip_x", "tip_y", "tip_z", "tip_roll", "tip_pitch", "tip_yaw", "jaw",
    "action_dx", "action_dy", "action_dz", "action_dyaw", "action_jaw", "reward",
]


def connect(path: Path | None = None) -> duckdb.DuckDBPyConnection:
    connection = duckdb.connect(str(path or database_path()))
    connection.execute(schema_path().read_text())
    return connection


def save_episode(connection: duckdb.DuckDBPyConnection, result: EpisodeResult) -> int:
    episode_id = connection.execute(
        """
        INSERT INTO episodes (task, policy_type, noise_scale, seed, success, steps_to_success, episode_length)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        RETURNING episode_id
        """,
        [result.task, result.policy_type, result.noise_scale, result.seed,
         result.success, result.steps_to_success, len(result.rows)],
    ).fetchone()[0]

    timesteps = pd.DataFrame(result.rows, columns=TIMESTEP_COLUMNS)
    timesteps.insert(0, "episode_id", episode_id)
    connection.register("new_timesteps", timesteps)
    connection.execute("INSERT INTO timesteps SELECT * FROM new_timesteps")
    connection.unregister("new_timesteps")
    return episode_id


def run_query_file(connection: duckdb.DuckDBPyConnection, query_path: Path) -> pd.DataFrame:
    return connection.execute(query_path.read_text()).df()
