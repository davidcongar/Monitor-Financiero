select 
    distinct categorias_de_gastos.name
from gastos
left join categorias_de_gastos
    on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    (gastos.id_usuario=:id_usuario or gastos.id_usuario=:id_shared_user)
    and shared_expense='Si'
order by categorias_de_gastos.name