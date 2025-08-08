select
    nombre as categoria,
    sum(importe) as importe
from gastos
left join categorias_de_gastos
  on gastos.id_categoria_de_gasto=categorias_de_gastos.id
where 
    gastos.id_usuario=:id_usuario
    and EXTRACT(year from fecha)=:anio
    and EXTRACT(month from fecha)=:mes
group by nombre
order by importe desc