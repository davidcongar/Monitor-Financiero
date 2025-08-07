with categories as (
  select * from categorias_de_gastos
  where id_usuario=:id_usuario
),
gastos_month as (
  SELECT 
      id_categoria_de_gasto,
      fecha,
      monthly_payments,
      EXTRACT(MONTH FROM age(:fecha,(fecha_trunc('month', fecha) - INTERVAL '1 month')))+EXTRACT(YEAR FROM age(:fecha,(fecha_trunc('month', fecha) - INTERVAL '1 month')))*12 as payed_months,
      importe AS total_importe,
      importe / monthly_payments AS monthly_importe,
      notes
  FROM gastos
  WHERE shared_expense = 'Si' 
  AND id_usuario = :id_usuario
)
select fecha,name,total_importe,monthly_payments,monthly_payments,notes,monthly_importe,payed_months
from gastos_month
left join categories
  on gastos_month.id_categoria_de_gasto=categories.id
where
  payed_months<=monthly_payments
  and payed_months>0
order by fecha desc