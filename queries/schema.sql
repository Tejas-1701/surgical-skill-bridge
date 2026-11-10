CREATE SEQUENCE IF NOT EXISTS episode_id_sequence START 1;

CREATE TABLE IF NOT EXISTS episodes (
    episode_id INTEGER PRIMARY KEY DEFAULT nextval('episode_id_sequence'),
    task VARCHAR NOT NULL,
    policy_type VARCHAR NOT NULL,
    noise_scale DOUBLE NOT NULL,
    seed INTEGER NOT NULL,
    success BOOLEAN NOT NULL,
    steps_to_success INTEGER,
    episode_length INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS timesteps (
    episode_id INTEGER NOT NULL,
    t INTEGER NOT NULL,
    tip_x DOUBLE,
    tip_y DOUBLE,
    tip_z DOUBLE,
    tip_roll DOUBLE,
    tip_pitch DOUBLE,
    tip_yaw DOUBLE,
    jaw DOUBLE,
    action_dx DOUBLE,
    action_dy DOUBLE,
    action_dz DOUBLE,
    action_dyaw DOUBLE,
    action_jaw DOUBLE,
    reward DOUBLE,
    PRIMARY KEY (episode_id, t)
);
