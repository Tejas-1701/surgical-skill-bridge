SELECT
    episode_id,
    t,
    ROUND(tip_x, 4) + 0.0 AS tip_x,
    ROUND(tip_y, 4) + 0.0 AS tip_y,
    ROUND(tip_z, 4) + 0.0 AS tip_z,
    ROUND(tip_roll, 4) + 0.0 AS tip_roll,
    ROUND(tip_pitch, 4) + 0.0 AS tip_pitch,
    ROUND(tip_yaw, 4) + 0.0 AS tip_yaw,
    ROUND(jaw, 4) + 0.0 AS jaw,
    ROUND(action_dx, 4) + 0.0 AS action_dx,
    ROUND(action_dy, 4) + 0.0 AS action_dy,
    ROUND(action_dz, 4) + 0.0 AS action_dz,
    ROUND(reward, 1) AS reward
FROM timesteps
WHERE episode_id = 1
ORDER BY t
LIMIT 10;