WITH moves AS (
    SELECT
        episode_id,
        sqrt(
            power(tip_x - lag(tip_x) OVER w, 2)
            + power(tip_y - lag(tip_y) OVER w, 2)
            + power(tip_z - lag(tip_z) OVER w, 2)
        ) AS step_distance
    FROM timesteps
    WINDOW w AS (PARTITION BY episode_id ORDER BY t)
)
SELECT
    e.episode_id,
    e.task,
    e.policy_type,
    e.success,
    ROUND(SUM(m.step_distance), 4) AS path_length_m
FROM moves m
JOIN episodes e USING (episode_id)
GROUP BY e.episode_id, e.task, e.policy_type, e.success
ORDER BY e.episode_id;
