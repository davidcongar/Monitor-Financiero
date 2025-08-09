select
    concat(EXTRACT(month FROM fecha),'/', RIGHT(cast(EXTRACT(YEAR FROM fecha) as text),2)) as year_month,
    sum(importe) as importe
from gastos
where 
    gastos.id_usuario = :id_usuario
