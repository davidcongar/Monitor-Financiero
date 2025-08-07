SELECT DISTINCT year
FROM (
    SELECT DISTINCT EXTRACT(YEAR FROM fecha) AS year
    FROM ingresos
    WHERE id_usuario = :id_usuario

    UNION

    SELECT EXTRACT(YEAR FROM current_date) AS year
) years
ORDER BY year;