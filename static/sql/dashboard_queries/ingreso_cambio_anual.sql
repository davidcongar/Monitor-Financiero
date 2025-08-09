with current_year as (
  select 
    sum(importe) as current_year
  from ingresos  
  where 
    EXTRACT(YEAR FROM fecha)=EXTRACT(YEAR FROM current_date)
    and id_usuario = :id_usuario
),
previous_year as (
  SELECT 
    SUM(importe) AS previous_year
  FROM ingresos
  WHERE 
    EXTRACT(YEAR FROM fecha)=EXTRACT(YEAR FROM current_date)-1
    AND id_usuario = :id_usuario
),
monthly_average as (
  select 
    EXTRACT(month FROM fecha) as month, 
    sum(importe) as month_importe
  from ingresos  
  where 
    EXTRACT(YEAR FROM fecha)=EXTRACT(YEAR FROM current_date)
    and id_usuario = :id_usuario
   group by EXTRACT(month FROM fecha)
),
monthly_average2 as (
  select 
    avg(month_importe) as monthly_average
  from monthly_average 

)
select
  coalesce(previous_year,0) as previous_year,
  coalesce(current_year,0) as current_year,
  (coalesce(current_year,0)-coalesce(previous_year,0))*100/coalesce(previous_year,1) as change,
  coalesce(monthly_average,0) as monthly_average
from current_year
left join previous_year on TRUE
left join monthly_average2 on TRUE
