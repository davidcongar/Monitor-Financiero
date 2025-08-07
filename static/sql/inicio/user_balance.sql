WITH ingresos AS (
  SELECT 
    SUM(importe) AS ingresos,
    EXTRACT(MONTH FROM fecha) AS month,
    EXTRACT(YEAR FROM fecha) AS year
  FROM ingresos
  WHERE id_usuario = :id_usuario
  GROUP BY EXTRACT(MONTH FROM fecha), EXTRACT(YEAR FROM fecha)
),
gastos AS (
  SELECT 
    SUM(importe) AS gastos,
    EXTRACT(MONTH FROM fecha) AS month,
    EXTRACT(YEAR FROM fecha) AS year
  FROM gastos
  WHERE id_usuario = :id_usuario
  GROUP BY  EXTRACT(MONTH FROM fecha), EXTRACT(YEAR FROM fecha)
),
join_table AS (
  SELECT 
    coalesce(i.year, e.year) AS year,
    coalesce(i.month, e.month) AS month,
    coalesce(i.ingresos, 0) AS ingresos,
    coalesce(e.gastos, 0) AS gastos
  FROM ingresos i
  FULL OUTER JOIN gastos e ON i.month = e.month AND i.year = e.year
),
balance_three_months_ago as (
  select sum(ingresos)-sum(gastos) as three_months_ago_balance
  from join_table
  WHERE 
    (year < EXTRACT(YEAR FROM current_date - INTERVAL '3 month')) 
    OR (year = EXTRACT(YEAR FROM current_date - INTERVAL '3 month') AND month <= EXTRACT(MONTH FROM current_date - INTERVAL '3 month'))
),
balance_two_months_ago as (
  select coalesce(sum(ingresos)-sum(gastos),0) as two_months_ago_balance
  from join_table
  WHERE 
    (year < EXTRACT(YEAR FROM current_date - INTERVAL '2 month')) 
    OR (year = EXTRACT(YEAR FROM current_date - INTERVAL '2 month') AND month <= EXTRACT(MONTH FROM current_date - INTERVAL '2 month'))
),
balance_previous_month as (
  select coalesce(sum(ingresos)-sum(gastos),0) as last_month_balance
  from join_table
  WHERE 
    (year < EXTRACT(YEAR FROM current_date - INTERVAL '1 month')) 
    OR (year = EXTRACT(YEAR FROM current_date - INTERVAL '1 month') AND month <= EXTRACT(MONTH FROM current_date - INTERVAL '1 month'))
),
balance_current_month as (
  select coalesce(sum(ingresos)-sum(gastos),0) as current_balance
  from join_table
)
select 
    *,
    case when last_month_balance > 0 then (current_balance - last_month_balance) * 100 / coalesce(last_month_balance,1) else 0 end as change_percentage,
    case when two_months_ago_balance > 0 then(last_month_balance - two_months_ago_balance) * 100 / coalesce(two_months_ago_balance,1) else 0 end AS change_percentage2,
    case when three_months_ago_balance > 0 then (two_months_ago_balance - three_months_ago_balance) * 100 / coalesce(three_months_ago_balance,1) else 0 end AS change_percentage3
from balance_previous_month
full join balance_current_month ON true
full join balance_two_months_ago ON true
full join balance_three_months_ago ON true
