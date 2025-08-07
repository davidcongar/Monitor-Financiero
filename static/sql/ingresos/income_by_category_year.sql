select
    name,
    sum(importe) as importe
from ingresos
left join ingresos_categories
  on ingresos.id_ingresos_category=ingresos_categories.id
where 
    ingresos.id_usuario=:id_usuario
    and EXTRACT(year from fecha)=:year_sel
group by name
order by importe desc