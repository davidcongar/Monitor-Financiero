select
    name,
    sum(importe) as importe
from gastos
left join categorias_de_gastos
  on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    (gastos.id_usuario=:id_usuario or gastos.id_usuario=:id_shared_user)
    and EXTRACT(year from fecha)=:year_sel
    and shared_expense='Si'
group by name
order by importe desc