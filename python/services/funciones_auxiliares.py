
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func
from sqlalchemy.sql import case
from flask import session,flash
from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, Numeric, or_
import re
import re
import json
from datetime import date, datetime
from decimal import Decimal

#####
# funciones auxiliares
#####

def get_all_models():
    """
    Retorna una lista de todos los modelos registrados en SQLAlchemy
    que tienen asignado el atributo __tablename__.
    """
    models = []
    for model in db.Model.registry._class_registry.values():
        if hasattr(model, "__tablename__"):
            models.append(model)
    return models

def get_model_by_name(table_name):
    """
    Retorna el modelo que corresponde al nombre de la tabla proporcionado.
    Si no se encuentra, retorna None.
    """
    for model in get_all_models():
        if model.__tablename__ == table_name:
            return model
    return None

def sanitize_data(model, data):
    """
    Convierte valores vacíos en el formulario a None o al valor por defecto según el tipo de columna.
    Si un campo tiene una lista con un solo valor, se guarda como el valor en sí.
    """
    for col in model.__table__.columns:
        if col.name in data:
            # Convert single-value lists to their actual value
            if isinstance(data[col.name], list) and len(data[col.name]) == 1:
                data[col.name] = data[col.name][0]
            # Convert empty strings to appropriate default values
            if data[col.name] == "":
                col_type_str = str(col.type).lower()
                if "boolean" in col_type_str:
                    data[col.name] = False
                elif "date" in col_type_str or "time" in col_type_str:
                    data[col.name] = None
                elif "json" in col_type_str:
                    data[col.name] = None
    return data

# Función auxiliar para convertir cada registro a diccionario
def record_to_dict(record):
    return {
        col: (
            getattr(record, col).isoformat()
            if hasattr(getattr(record, col), "isoformat")
            else getattr(record, col)
        )
        for col in record.__table__.columns.keys()
    }


# Filtro para formatear fechas
def date_format(value):
    if value:
        return value.strftime("%Y-%m-%d")
    else:
        return value
    
# Filtro para formatear moneda
def money_format(value):
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return value 

def hour_format(value):
    if 'pm' in value.lower() or 'am' in value.lower():
        new_value= datetime.strptime(value.strip().lower(), "%I:%M %p").strftime("%H:%M")
    else:
        try:
            parts = value.strip().split(":")
            new_value=":".join(parts[:2])    
        except:
            new_value=value
    return new_value


def search_table(query, model, search, joins):
    filters = []
    extra_filters = []

    # Detectar si es número (int o float)
    try:
        if '.' in search:
            search_number = float(search)
        else:
            search_number = int(search)
    except ValueError:
        search_number = None

    # Filtros sobre columnas del modelo principal
    for col in model.__table__.columns:
        col_attr = getattr(model, col.name)
        if isinstance(col.type, (String, Text)):
            filters.append(col_attr.ilike(f"%{search}%"))
        elif search_number is not None and isinstance(col.type, (Integer, Float, Numeric)):
            filters.append(col_attr == search_number)

    # Filtros sobre columnas relacionadas (joins)
    for _, (_, _, name_column) in joins.items():
        if isinstance(name_column.type, (String, Text)):
            extra_filters.append(name_column.ilike(f"%{search}%"))
        elif search_number is not None and isinstance(name_column.type, (Integer, Float, Numeric)):
            extra_filters.append(name_column == search_number)

    return query.filter(or_(*(filters + extra_filters)))

def get_id_visualizacion(table_name):
    modelo = get_model_by_name(table_name)
    if table_name!='usuarios':
        max_id = modelo.query.filter_by(id_usuario=session['id_usuario']).with_entities(func.max(modelo.id_visualizacion)).scalar()
    else:
        max_id = modelo.query.with_entities(func.max(modelo.id_visualizacion)).scalar()
    return (max_id or 0) + 1

# queries con variables dinamicas
PARAM_REGEX = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*)")

def extract_param_names(sql: str) -> set[str]:
    # Find :param placeholders in the SQL
    return set(PARAM_REGEX.findall(sql))

def to_jsonable(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)  # or str(v) if you prefer exact representation
    return v

def rowmapping_to_dict(rm):
    # rm is a RowMapping
    return {k: to_jsonable(v) for k, v in rm.items()}

from decimal import Decimal, InvalidOperation
import re

def parse_money(value):
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        return Decimal(str(value))
    if isinstance(value, str):
        s = value.strip()
        # remove everything except digits, decimal separators, minus sign
        s = re.sub(r'[^0-9,.\-]', '', s)

        # Handle common formats:
        # If there's a comma but no dot, treat comma as decimal sep (e.g., "45,50")
        if ',' in s and '.' not in s:
            s = s.replace('.', '').replace(',', '.')
        else:
            # Otherwise drop thousands commas (e.g., "1,234.56" -> "1234.56")
            s = s.replace(',', '')

        try:
            return Decimal(s)
        except InvalidOperation:
            raise ValueError(f"importe value '{value}' is not a valid number")
