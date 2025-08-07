SELECT DISTINCT year
FROM (
    SELECT DISTINCT EXTRACT(YEAR FROM fecha) AS year
    FROM gastos
    WHERE id_usuario = :id_usuario

    UNION

    SELECT EXTRACT(YEAR FROM CURRENT_DATE) AS year
) years
ORDER BY year;