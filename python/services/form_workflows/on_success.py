
from python.models.modelos import *
from sqlalchemy import String, Text, or_,func,Integer, Float, Numeric
from sqlalchemy.sql import case
from flask import session,flash
import re
import json
from datetime import date, datetime
from decimal import Decimal

#####
# funciones de formularios
#####

HANDLERS = {}

def on_success(*tables):
    def wrapper(fn):
        for t in tables:
            HANDLERS[t] = fn
        return fn
    return wrapper

def edit_on_success(table_name, id):
    handler = HANDLERS.get(table_name)
    if not handler:
        return
    return handler(id)

@on_success('negocios_apple_pay')
def eos_negocios_apple_pay(id):
    record = db.session.get(NegociosApplePay, id)
    if not record or record.id_categoria_de_gasto is None:
        return
    (Gastos.query
        .filter_by(id_usuario=session['id_usuario'], id_negocio_apple_pay=record.id)
        .update(
            {"id_categoria_de_gasto": record.id_categoria_de_gasto},
            synchronize_session=False
        )
    )
    db.session.commit()
