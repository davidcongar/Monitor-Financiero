select
    name,
    sum(importe) as importe
from gastos
left join categorias_de_gastos
  on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    (gastos.id_usuario=:id_usuario or gastos.id_usuario=:id_usuario_conectado)
    and EXTRACT(year from fecha)=:year_sel
    and gasto_compartido='Si'
group by name
order by importe desc