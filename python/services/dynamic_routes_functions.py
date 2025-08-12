from python.models.modelos import *
from sqlalchemy import func
from python.services.system.helper_functions import *
from flask import  jsonify

def get_joins():
    joins = {
        "id_usuario": (Usuarios, Usuarios.id, Usuarios.nombre),
        "id_categoria_de_reporte":(CategoriasDeReportes, CategoriasDeReportes.id, CategoriasDeReportes.nombre),
        "id_usuario_conectado": (Usuarios, Usuarios.id, Usuarios.nombre),
        "id_cuenta": (Cuentas, Cuentas.id, Cuentas.nombre),
        "id_cuenta_salida": (Cuentas, Cuentas.id, Cuentas.nombre),
        "id_cuenta_entrada": (Cuentas, Cuentas.id, Cuentas.nombre),
        "id_categoria_de_gasto": (CategoriasDeGastos, CategoriasDeGastos.id, CategoriasDeGastos.nombre),
        "id_categoria_de_ingreso": (CategoriasDeIngresos, CategoriasDeIngresos.id, CategoriasDeIngresos.nombre),
        "id_negocio_apple_pay": (NegociosApplePay, NegociosApplePay.id, NegociosApplePay.nombre),
    }
    return joins

def get_tabs():
    tabs = {
        "ejemplo": "estatus"
    }
    return tabs

def get_foreign_options():
    foreign_options = {
        "id_categoria_de_reporte":CategoriasDeReportes.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "id_cuenta": Cuentas.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "id_cuenta_salida": Cuentas.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "id_cuenta_entrada": Cuentas.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "id_categoria_de_gasto": CategoriasDeGastos.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "id_categoria_de_ingreso": CategoriasDeIngresos.query.filter_by(estatus="Activo",id_usuario=session['id_usuario']),
        "gasto_compartido":{"Si","No"},
        "tipo":{"Débito","Crédito","Inversión","Inversión - Rendimientos"}
    }
    return foreign_options

def get_multiple_choice_data():
    multiple_choice_data = {}
    options = {
        "ejemplo": [""]
    }      
    for i in options:
        multiple_choice_data[i] = {
            "selected": options[i],
            "options": options[i]
        }
    return multiple_choice_data

def get_table_columns():
    columns = {
        "usuarios":['id_visualizacion','nombre','correo_electronico','id_usuario_conectado','estatus'],
        "categorias_de_reportes":['id_visualizacion','nombre','estatus'],
        "reportes":['id_visualizacion','id_categoria_de_reporte','nombre','descripcion'],
        "cuentas":['id_visualizacion','nombre','nombre_apple_pay','tipo','monto_credito','estatus'],
        "categorias_de_gastos":['id_visualizacion','nombre','estatus'],
        "categorias_de_ingresos":['id_visualizacion','nombre','estatus'],
        "negocios_apple_pay":['id_visualizacion','nombre','id_categoria_de_gasto'],
        "gastos":['id_visualizacion','id_cuenta','id_categoria_de_gasto','id_negocio_apple_pay','gasto_compartido','pagos_mensuales','fecha','importe'],
        "ingresos":['id_visualizacion','id_cuenta','id_categoria_de_ingreso','fecha','importe'],
        "gastos_recurrentes":['id_visualizacion','id_cuenta','id_categoria_de_gasto','gasto_compartido','importe'],
        "ingresos_recurrentes":['id_visualizacion','id_cuenta','id_categoria_de_ingreso','importe'],
        "transferencias":['id_visualizacion','id_cuenta_salida','id_cuenta_entrada','fecha','importe'],

    }
    return columns

def get_table_buttons():
    buttons = {
        "reportes":1,
    }
    return buttons

def get_columns_order():
    columns = {
        "usuarios":['id','id_visualizacion','nombre','correo_electronico','id_usuario_conectado','contrasena_api','estatus','fecha_de_creacion'],
        "categorias_de_reportes":['id','id_visualizacion','nombre','estatus'],
        "reportes":['id_visualizacion','id_categoria_de_reporte','nombre','descripcion','ruta_sql'],
        "cuentas":['id','id_visualizacion','nombre','nombre_apple_pay','tipo','monto_credito','estatus','fecha_de_creacion','fecha_de_actualizacion'],
        "categorias_de_gastos":['id','id_visualizacion','nombre','estatus','fecha_de_creacion','fecha_de_actualizacion'],
        "categorias_de_ingresos":['id','id_visualizacion','nombre','estatus','fecha_de_creacion','fecha_de_actualizacion'],
        "negocios_apple_pay":['id','id_visualizacion','nombre','id_categoria_de_gasto','estatus','fecha_de_creacion','fecha_de_actualizacion'],
        "gastos":['id','id_visualizacion','id_cuenta','id_categoria_de_gasto','categoria_apple_pay','id_negocio_apple_pay','gasto_compartido','pagos_mensuales','fecha','importe','notas','fecha_de_creacion','fecha_de_actualizacion'],
        "ingresos":['id','id_visualizacion','id_cuenta','id_categoria_de_ingreso','fecha','importe','notas','fecha_de_creacion','fecha_de_actualizacion'],
        "gastos_recurrentes":['id','id_visualizacion','id_cuenta','id_categoria_de_gasto','gasto_compartido','importe','fecha_de_creacion','fecha_de_actualizacion'],
        "ingresos_recurrentes":['id','id_visualizacion','id_cuenta','id_categoria_de_ingreso','importe','fecha_de_creacion','fecha_de_actualizacion'],
        "transferencias":['id','id_visualizacion','id_cuenta_salida','id_cuenta_entrada','fecha','importe','notas','fecha_de_creacion','fecha_de_actualizacion']
    }
    return columns

def get_estatus_options():
    estatus_options = {
        'prueba': {"a", "b"}
    }
    return estatus_options

def get_breadcrumbs(table_name):
    # [modulo,active_menu]
    breadcrumbs={
        "usuarios":['Permisos','permisos'],
        "roles":['Permisos','permisos'],
        "logs_auditoria":['Auditoría','auditoria'],
        "cuentas":['Cátalogos','catalogos'],
        "categorias_de_gastos":['Cátalogos','catalogos'],
        "categorias_de_ingresos":['Cátalogos','catalogos'],
        "negocios_apple_pay":['Cátalogos','catalogos'],
        "gastos":['Gastos','gastos'],
        "gastos_recurrentes":['Gastos','gastos'],
        "ingresos":['Ingresos','ingresos'],
        "ingresos_recurrentes":['Ingresos','ingresos'],
        "transferencias":['Transferencias','transferencias'],
        "reportes":['Reportes','reportes']
    }
    breadcrumbs=breadcrumbs.get(table_name,{'Bases de datos','bases_de_datos'})
    return breadcrumbs[0],breadcrumbs[1]


def get_ignored_columns(table_name):
    columnas_generales = {'fecha_de_creacion', 'estatus', 'id_usuario', 'id_visualizacion', 'fecha_de_actualizacion','contrasena','contrasena_api'}
    columns = {
        "gastos": {'id_negocio_apple_pay'} | columnas_generales,
        "negocios_apple_pay": {'nombre'} | columnas_generales,
    }
    columns=columns.get(table_name)
    if columns==None:
        columns=columnas_generales
    return columns

def get_non_mandatory_columns(table_name):
    columnas_generales = {'descripcion','notas'}
    columns = {
        "cuentas": {'dia_de_corte','dia_de_pago','monto_credito'} | columnas_generales,
    }
    columns=columns.get(table_name)
    if columns==None:
        columns=columnas_generales
    return columns

def get_data_tabs(table_name):
    column_tabs=get_tabs()
    column_tabs=column_tabs.get(table_name)
    model = get_model_by_name(table_name)
    column = getattr(model, column_tabs, None)
    results = (
        db.session.query(column, func.count().label('count'))
        .group_by(column)
        .order_by(func.count().desc())
        .all()
    )
    results = {
        (estatus if estatus else 'Sin estatus'): count
        for estatus, count in results
    }
    return results

def get_calendar_date_variable(table_name):
    date_variable={
        "ejemplo":"fecha_de_creacion"
    }
    date_variable=date_variable.get(table_name,'')
    return date_variable

def get_table_relationships(table_name):
    relationships={
        "ejemplo":['registros_relacionados_a_ejemplo'],
    }
    relationships=relationships.get(table_name,'')
    return relationships
