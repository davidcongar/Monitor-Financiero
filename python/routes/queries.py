# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *

from python.services.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont


queries_bp = Blueprint("queries", __name__, url_prefix="/queries")

SQL_QUERIES = {
    "noticas_hoy": "./static/sql/noticias_hoy.sql",
    "noticas_hoy_categoria": "./static/sql/noticias_hoy_categoria.sql",
    "noticias_semana": "./static/sql/noticias_semana.sql",
    "noticias_semana_categoria": "./static/sql/noticias_semana_categoria.sql",
    "noticias_totales": "./static/sql/noticias_totales.sql",
    "noticias_totales_categoria": "./static/sql/noticias_totales_categoria.sql",
}


@queries_bp.route("/<string:nombre_sql>", methods=["GET"])
@login_required
def data_sql(nombre_sql):
    path = SQL_QUERIES.get(nombre_sql)
    base_query = open(path, "r", encoding="utf-8").read()
    data = db.session.execute(text(base_query)).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)