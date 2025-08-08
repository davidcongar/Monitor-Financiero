select
    concat(EXTRACT(month FROM fecha),'/', RIGHT(cast(EXTRACT(YEAR FROM fecha) as text),2)) as anio_mes,
    sum(importe) as importe
from ingresos
where 
    ingresos.id_usuario = :id_usuario