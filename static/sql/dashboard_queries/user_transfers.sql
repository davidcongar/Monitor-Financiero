with accounts_user as (
  select * from cuentas 
  where id_usuario=:id_usuario
)
select transferencias.id,id_transfer,input.name as input_name,output.name as output_name, fecha,importe,notes  
from transferencias
left join accounts_user as input
  on transferencias.id_cuenta_entrada=input.id
left join accounts_user as output
  on transferencias.id_cuenta_salida=output.id
where transferencias.id_usuario=:id_usuario
order by cast(SUBSTRING(id_transfer, 3) as int) desc