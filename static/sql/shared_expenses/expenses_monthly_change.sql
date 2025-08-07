with current_month as (
  select sum(importe) as current_month
  from gastos  
  where 
    concat(EXTRACT(YEAR FROM fecha),EXTRACT(MONTH FROM fecha))=concat(EXTRACT(YEAR FROM current_date),EXTRACT(MONTH FROM current_date))
    and (id_usuario = :id_usuario or id_usuario=:id_shared_user)
    and shared_expense='Si'
),
previous_month as (
  SELECT SUM(importe) AS previous_month
  FROM gastos
  WHERE 
      -- Handle case where the current month is January
      (EXTRACT(MONTH FROM current_date) = 1 AND 
      CONCAT(EXTRACT(YEAR FROM fecha), EXTRACT(MONTH FROM fecha)) = 
      CONCAT(EXTRACT(YEAR FROM current_date) - 1, 12))
      OR
      -- Handle all other months
      (EXTRACT(MONTH FROM current_date) != 1 AND 
      CONCAT(EXTRACT(YEAR FROM fecha), EXTRACT(MONTH FROM fecha)) = 
      CONCAT(EXTRACT(YEAR FROM current_date), EXTRACT(MONTH FROM current_date) - 1))
    AND (id_usuario = :id_usuario or id_usuario=:id_shared_user)
    and shared_expense='Si'
),
previous_two_month as (
  SELECT SUM(importe) AS previous_two_month
  FROM gastos
  WHERE 
      -- Handle case where the current month is January
      (EXTRACT(MONTH FROM current_date) = 1 AND 
      CONCAT(EXTRACT(YEAR FROM fecha), EXTRACT(MONTH FROM fecha)) = 
      CONCAT(EXTRACT(YEAR FROM current_date) - 2, 12))
      OR
      -- Handle all other months
      (EXTRACT(MONTH FROM current_date) != 1 AND 
      CONCAT(EXTRACT(YEAR FROM fecha), EXTRACT(MONTH FROM fecha)) = 
      CONCAT(EXTRACT(YEAR FROM current_date), EXTRACT(MONTH FROM current_date) - 2))
      AND (id_usuario = :id_usuario or id_usuario=:id_shared_user)
      and shared_expense='Si'
)
select
  coalesce(previous_two_month,0) as previous_two_month,
  coalesce(previous_month,0) as previous_month,
  coalesce(current_month,0) as current_month,
  (coalesce(previous_month,0)-coalesce(previous_two_month,0))*100/coalesce(previous_two_month,1) as change_two,
  (coalesce(current_month,0)-coalesce(previous_month,0))*100/coalesce(previous_month,1) as change
from current_month
left join previous_month on TRUE
left join previous_two_month on TRUE