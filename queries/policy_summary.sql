SELECT
    task,
    policy_type,
    noise_scale,
    COUNT(*) AS episodes,
    ROUND(AVG(success::INTEGER), 3) AS success_rate,
    ROUND(AVG(steps_to_success), 1) AS mean_steps_to_success
FROM episodes
GROUP BY task, policy_type, noise_scale
ORDER BY task, policy_type, noise_scale;
