with ingresos as (
  select id_cuenta, sum(importe) as ingresos 
  from ingresos
  where id_usuario = :id_usuario
  group by id_cuenta
),
gastos as (
  select id_cuenta, sum(importe) as gastos 
  from gastos
  where id_usuario = :id_usuario
  group by id_cuenta
),
transferencias_output as (
  select id_cuenta_salida as id_cuenta, sum(importe) as transferencias_output 
  from transferencias
  where id_usuario = :id_usuario
  group by id_cuenta
),
transferencias_input as (
  select id_cuenta_entrada as id_cuenta, sum(importe) as transferencias_input 
  from transferencias
  where id_usuario = :id_usuario
  group by id_cuenta
),
join_table as (
  select 
    coalesce(i.id_cuenta, e.id_cuenta, tro.id_cuenta, ti.id_cuenta) as id_cuenta,
    coalesce(i.ingresos, 0) as ingresos,
    coalesce(e.gastos, 0) as gastos,
    coalesce(tro.transferencias_output, 0) as transferencias_output,
    coalesce(ti.transferencias_input, 0) as transferencias_input
  from ingresos i
  full outer join gastos e on i.id_cuenta = e.id_cuenta
  full outer join transferencias_output tro on coalesce(i.id_cuenta, e.id_cuenta) = tro.id_cuenta
  full outer join transferencias_input ti on coalesce(i.id_cuenta, e.id_cuenta, tro.id_cuenta) = ti.id_cuenta
),
cuentas as (
  select id as id_cuenta,monto_credito,tipo,nombre,estatus from cuentas
  where id_usuario = :id_usuario
)
select nombre,tipo,coalesce(ingresos+transferencias_input-transferencias_output-gastos,0) as balance, 
case when tipo='Crédito' then monto_credito+(ingresos+transferencias_input-transferencias_output-gastos) else 0  end as available_credit
from join_table
left join cuentas
  on join_table.id_cuenta=cuentas.id_cuenta
where estatus='Activo'
order by nombre
