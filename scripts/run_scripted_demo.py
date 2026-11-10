import argparse
from pathlib import Path

from skillbridge.config import database_path, gif_dir
from skillbridge.gif import save_gif
from skillbridge.rollout import make_env, run_episode
from skillbridge.trajectory_db import connect, run_query_file, save_episode

QUERIES_DIR = Path(__file__).resolve().parents[1] / "queries"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["needle_reach", "peg_transfer"], default="needle_reach")
    parser.add_argument("--episodes", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--gif", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    env = make_env(args.task)
    connection = connect()

    for episode_index in range(args.episodes):
        seed = args.seed + episode_index
        record = args.gif and episode_index == 0
        result = run_episode(env, args.task, seed, args.noise, record_frames=record)
        episode_id = save_episode(connection, result)
        print(f"episode {episode_id}: seed={seed} success={result.success} steps={result.steps_to_success}")
        if record:
            gif_path = save_gif(result.frames, gif_dir() / f"{args.task}_noise{args.noise}_seed{seed}.gif")
            print(f"gif saved to {gif_path}")

    print(f"database: {database_path()}")
    print(run_query_file(connection, QUERIES_DIR / "policy_summary.sql").to_string(index=False))
    connection.close()
    env.close()


if __name__ == "__main__":
    main()
