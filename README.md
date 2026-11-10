# Surgical Skill Bridge

Can a surgical skill assessor trained on human data judge and improve robot policies?

I train policies for da Vinci–style surgical tasks in simulation (SurRoL), train a skill assessor on human surgeon kinematics (JIGSAWS), and then score robot trajectories for "surgeon-likeness".

## Status

| Week | Deliverable | Status |
|---|---|---|
| 1 | SurRoL running on Colab, scripted demo GIF, trajectory database | Done |
| 2 | Rollouts for needle reach and peg transfer logged to DuckDB | Next |

## Quick start

On Colab, open `notebooks/01_setup_and_scripted_demo.ipynb` and run all cells.

Locally:

```bash
bash setup.sh
python scripts/run_scripted_demo.py --task needle_reach --episodes 5 --gif
```

## Layout

```
src/skillbridge/   rollout, database and config code
scripts/           command-line entry points
queries/           schema and saved SQL analysis queries
notebooks/         thin Colab notebooks that call the code above
```

## Simulator

I use the original SurRoL release (commit `b151ad6`, IROS 2021), which runs headless on Python 3.12 with gym 0.26.

## Data

Trajectories go into a DuckDB file (`trajectories.duckdb`) with `episodes` and `timesteps` tables. On Colab it lives in Google Drive, and locally in `outputs/`.
