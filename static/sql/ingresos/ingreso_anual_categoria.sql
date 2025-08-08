select
    nombre as categoria,
    sum(importe) as importe
from ingresos
left join categorias_de_ingresos
  on ingresos.id_categoria_de_ingreso=categorias_de_ingresos.id
where 
    ingresos.id_usuario=:id_usuario
    and EXTRACT(year from fecha)=:anio
group by nombre
order by importe desc