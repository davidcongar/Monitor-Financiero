with categories as (
  select * from categorias_de_gastos
  where id_usuario=:id_usuario or id_usuario=:id_shared_user
),
all_gastos as (
  SELECT 
      users.name,
      id_categoria_de_gasto,
      fecha,
      monthly_payments,
      EXTRACT(MONTH FROM age(:fecha,(fecha_trunc('month', fecha) - INTERVAL '1 month')))+EXTRACT(YEAR FROM age(:fecha,(fecha_trunc('month', fecha) - INTERVAL '1 month')))*12 as payed_months,
      importe AS total_importe,
      importe / monthly_payments AS monthly_importe,
      notes
  FROM gastos
  left join users
    on gastos.id_usuario=users.id_usuario
  WHERE shared_expense = 'Si' 
  AND (gastos.id_usuario = :id_usuario or gastos.id_usuario=:id_shared_user)
),
borrow_gastos as (
  select concat('4Préstamos hechos por ',all_gastos.name) as variable,coalesce(sum(monthly_importe),0) as value
  from all_gastos
  left join categories
    on all_gastos.id_categoria_de_gasto=categories.id
  where categories.name='Préstamos'
    and payed_months<=monthly_payments
    and payed_months>0
  group by all_gastos.name
),
general_gastos as (
  select concat('1',all_gastos.name) as variable,coalesce(sum(monthly_importe),0) as value
  from all_gastos
  left join categories
    on all_gastos.id_categoria_de_gasto=categories.id
  where categories.name!='Préstamos'
    and payed_months<=monthly_payments
    and payed_months>0
  group by all_gastos.name
),
total as (
  select '2Gasto total del mes' as variable, coalesce(sum(value),0) as value from general_gastos
),
divided as (
  select '3Gasto dividido del mes' as variable, coalesce(sum(value)/2,0) as value from general_gastos
),
debt as (
  SELECT variable, value
  FROM general_gastos
  ORDER BY value
  LIMIT 1
),
debt2 as (
  select concat('5Deuda mes (',variable,')') as variable,gasto-value as debt 
  from debt
  cross join (select value as gasto from divided) as div
)
select * from general_gastos
union
select * from total
union
select * from divided
union
select * from borrow_gastos
union
select * from debt2
order by variable