with account_gastos as (
    select
        'Gasto' as Tipo,
        nombre as Categoria,
        fecha,
        importe*-1 as importe,
        notas
    from gastos
    left join categorias_de_gastos
        on gastos.id_categoria_de_gasto=categorias_de_gastos.id
    where 
        gastos.id_usuario=:id_usuario
        and gastos.id_cuenta=:id_cuenta
),
account_ingresos as (
    select
        'Ingreso' as Tipo,
        nombre as Categoria,
        fecha,
        importe,
        notas
    from ingresos
    left join categorias_de_ingresos
        on ingresos.id_categoria_de_ingreso=categorias_de_ingresos.id
    where 
        ingresos.id_usuario=:id_usuario
        and ingresos.id_cuenta=:id_cuenta
),
account_transferencias_input as (
    select
        'Transferencias - Entrada' as Tipo,
        '' as Categoria,
        fecha,
        importe,
        notas
    from transferencias
    where 
        transferencias.id_usuario=:id_usuario
        and transferencias.id_cuenta_entrada=:id_cuenta
),
account_transferencias_output as (
    select
        'Transferencias - Salida' as Tipo,
        '' as Categoria,
        fecha,
        importe*-1 as importe,
        notas
    from transferencias
    where 
        transferencias.id_usuario=:id_usuario
        and transferencias.id_cuenta_salida=:id_cuenta
)
select * from account_gastos
union
select * from account_ingresos
union
select * from account_transferencias_input
union
select * from account_transferencias_output
order by fecha desc
