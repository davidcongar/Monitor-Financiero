with categories as (
  select * from categorias_de_gastos
  where id_usuario=:id_usuario
),
gastos_month as (
  SELECT 
      id_categoria_de_gasto,
      fecha,
      pagos_mensuales,
      EXTRACT(MONTH FROM age(:fecha,(date_trunc('month', fecha) - INTERVAL '1 month')))+EXTRACT(YEAR FROM age(:fecha,(date_trunc('month', fecha) - INTERVAL '1 month')))*12 as meses_pagados,
      importe AS importe_total,
      importe / pagos_mensuales AS importe_mensual,
      notas
  FROM gastos
  WHERE gasto_compartido = 'Si' 
  AND id_usuario = :id_usuario
)
select fecha,nombre,importe_total,pagos_mensuales,notas,importe_mensual,meses_pagados
from gastos_month
left join categories
  on gastos_month.id_categoria_de_gasto=categories.id
where
  meses_pagados<=pagos_mensuales
  and meses_pagados>0
order by fecha desc