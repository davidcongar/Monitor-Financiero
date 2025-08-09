select 
    distinct categorias_de_gastos.nombre
from gastos
left join categorias_de_gastos
    on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    (gastos.id_usuario=:id_usuario or gastos.id_usuario=:id_usuario_conectado)
    and gasto_compartido='Si'
order by categorias_de_gastos.nombre