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
join_table as(
  SELECT 
    concat(coalesce(i.year, e.year)) AS year,
    coalesce(i.month, e.month) AS month,
    coalesce(i.ingresos, 0) AS ingresos,
    coalesce(e.gastos, 0) AS gastos,
    coalesce(i.ingresos, 0)- coalesce(e.gastos, 0) as net
  FROM ingresos i
  FULL OUTER JOIN gastos e ON i.month = e.month AND i.year = e.year
  order by year, month
)
select
  concat(month,'/',RIGHT(year,2)) as year_month,
  sum(net) OVER (ORDER BY year,month) AS balance
from join_table