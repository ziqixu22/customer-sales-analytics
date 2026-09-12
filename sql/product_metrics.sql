-- Product analytics reference queries.
-- Assumed warehouse tables:
-- users(user_id, signup_ts, acquisition_channel)
-- events(user_id, event_ts, event_name, session_id)
-- orders(order_id, user_id, order_ts, revenue)
-- experiment_assignments(user_id, experiment_name, variant, assigned_ts)

-- 1) Activation funnel by signup cohort
WITH user_funnel AS (
    SELECT
        u.user_id,
        DATE_TRUNC('week', u.signup_ts) AS signup_week,
        MAX(CASE WHEN e.event_name = 'view_product' THEN 1 ELSE 0 END) AS viewed_product,
        MAX(CASE WHEN e.event_name = 'add_to_cart' THEN 1 ELSE 0 END) AS added_to_cart,
        MAX(CASE WHEN e.event_name = 'checkout_started' THEN 1 ELSE 0 END) AS started_checkout,
        MAX(CASE WHEN e.event_name = 'purchase' THEN 1 ELSE 0 END) AS purchased
    FROM users u
    LEFT JOIN events e
      ON u.user_id = e.user_id
     AND e.event_ts >= u.signup_ts
     AND e.event_ts < u.signup_ts + INTERVAL '7 day'
    GROUP BY 1,2
)
SELECT
    signup_week,
    COUNT(*) AS users,
    AVG(viewed_product::FLOAT) AS view_rate,
    AVG(added_to_cart::FLOAT) AS cart_rate,
    AVG(started_checkout::FLOAT) AS checkout_start_rate,
    AVG(purchased::FLOAT) AS seven_day_conversion
FROM user_funnel
GROUP BY 1
ORDER BY 1;

-- 2) 30-day retention matrix
WITH activity AS (
    SELECT DISTINCT
        e.user_id,
        DATE_TRUNC('month', u.signup_ts) AS cohort_month,
        DATE_TRUNC('month', e.event_ts) AS activity_month
    FROM events e
    JOIN users u USING (user_id)
), indexed AS (
    SELECT
        user_id,
        cohort_month,
        activity_month,
        (EXTRACT(YEAR FROM AGE(activity_month, cohort_month)) * 12
         + EXTRACT(MONTH FROM AGE(activity_month, cohort_month)))::INT AS month_index
    FROM activity
), sizes AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size
    FROM indexed
    WHERE month_index = 0
    GROUP BY 1
)
SELECT
    i.cohort_month,
    i.month_index,
    COUNT(DISTINCT i.user_id) AS retained_users,
    COUNT(DISTINCT i.user_id)::FLOAT / s.cohort_size AS retention_rate
FROM indexed i
JOIN sizes s USING (cohort_month)
WHERE i.month_index BETWEEN 0 AND 6
GROUP BY 1,2,s.cohort_size
ORDER BY 1,2;

-- 3) Experiment analysis table with pre-period covariates for CUPED
WITH pre AS (
    SELECT
        a.user_id,
        COUNT(*) FILTER (
            WHERE e.event_ts >= a.assigned_ts - INTERVAL '14 day'
              AND e.event_ts < a.assigned_ts
        ) AS pre_events,
        COUNT(*) FILTER (
            WHERE e.event_name = 'purchase'
              AND e.event_ts >= a.assigned_ts - INTERVAL '14 day'
              AND e.event_ts < a.assigned_ts
        ) AS pre_purchases
    FROM experiment_assignments a
    LEFT JOIN events e USING (user_id)
    WHERE a.experiment_name = 'onboarding_redesign'
    GROUP BY 1
), post AS (
    SELECT
        a.user_id,
        a.variant,
        MAX(CASE WHEN e.event_name = 'purchase' THEN 1 ELSE 0 END) AS converted_7d,
        COUNT(*) AS post_events
    FROM experiment_assignments a
    LEFT JOIN events e
      ON a.user_id = e.user_id
     AND e.event_ts >= a.assigned_ts
     AND e.event_ts < a.assigned_ts + INTERVAL '7 day'
    WHERE a.experiment_name = 'onboarding_redesign'
    GROUP BY 1,2
)
SELECT p.*, pre.pre_events, pre.pre_purchases
FROM post p
JOIN pre USING (user_id);
