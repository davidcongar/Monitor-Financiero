select
    concat(EXTRACT(month FROM fecha),'/', RIGHT(cast(EXTRACT(YEAR FROM fecha) as text),2)) as year_month,
    sum(importe) as importe
from gastos
left join categorias_de_gastos
    on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    (gastos.id_usuario = :id_usuario or gastos.id_usuario=:id_shared_user)
    and shared_expense='Si'