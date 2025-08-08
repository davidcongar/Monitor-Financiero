# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *

from python.services.authentication import *
from python.services.funciones_auxiliares import *

import io
from PIL import Image, ImageDraw, ImageFont


queries_bp = Blueprint("queries", __name__, url_prefix="/queries")

SQL_QUERIES = {
    "balance_mensual": "./static/sql/inicio/balance_mensual.sql",
    "gasto_mensual_categoria":"./static/sql/gastos/gasto_mensual_categoria.sql",
    "gasto_anual_categoria":"./static/sql/gastos/gasto_anual_categoria.sql",
    "ingreso_mensual_categoria":"./static/sql/ingresos/ingreso_mensual_categoria.sql",
    "ingreso_anual_categoria":"./static/sql/ingresos/ingreso_anual_categoria.sql",
}

@queries_bp.route("/<string:nombre_sql>", methods=["GET"])
@login_required
def data_sql(nombre_sql):
    path = SQL_QUERIES.get(nombre_sql)
    base_query = open(path, "r", encoding="utf-8").read()
    variables_query = extract_param_names(base_query)
    variables_request = {k: v for k, v in request.values.items() if k in variables_query and v != ""}
    if "id_usuario" in variables_query:
        variables_request["id_usuario"] = session["id_usuario"]
    data=db.session.execute(text(base_query),variables_request).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)