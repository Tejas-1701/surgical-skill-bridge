import os
from pathlib import Path

COLAB_DRIVE_ROOT = Path("/content/drive/MyDrive/surgical-skill-bridge")
LOCAL_ROOT = Path(__file__).resolve().parents[2] / "outputs"


def running_in_colab() -> bool:
    return "COLAB_RELEASE_TAG" in os.environ


def output_root() -> Path:
    override = os.environ.get("SKILLBRIDGE_OUTPUT")
    if override:
        root = Path(override)
    elif running_in_colab() and COLAB_DRIVE_ROOT.parent.exists():
        root = COLAB_DRIVE_ROOT
    else:
        root = LOCAL_ROOT
    root.mkdir(parents=True, exist_ok=True)
    return root


def gif_dir() -> Path:
    path = output_root() / "gifs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def database_path() -> Path:
    return output_root() / "trajectories.duckdb"


def schema_path() -> Path:
    return Path(__file__).resolve().parents[2] / "queries" / "schema.sql"
