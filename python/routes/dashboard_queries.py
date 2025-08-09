# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *

from python.services.authentication import *
from python.services.helper_functions import *

import io
from PIL import Image, ImageDraw, ImageFont


dashboard_queries_bp = Blueprint("dashboard_queries", __name__, url_prefix="/dashboard_queries")

@dashboard_queries_bp.route("/<string:nombre_sql>", methods=["GET"])
@login_required
def sql_data(nombre_sql):
    path = './static/sql/dashboard_queries/'+nombre_sql+'.sql'
    base_query = open(path, "r", encoding="utf-8").read()
    variables_query = extract_param_names(base_query)
    variables_request = {k: v for k, v in request.values.items() if k in variables_query and v != ""}
    if "id_usuario" in variables_query:
        variables_request["id_usuario"] = session["id_usuario"]
    data=db.session.execute(text(base_query),variables_request).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)

@dashboard_queries_bp.route('/manual/gasto_mensual', methods=['GET'])
@login_required
def expenses_by_month():
    year = request.args.get("year")
    category=request.args.get("category")
    params = {}
    params['id_usuario'] = session['id_usuario']
    base_query=open('./static/sql/dashboard_queries/gasto_mensual.sql','r',encoding='utf-8').read()
    if year!='historico':
        base_query += " and extract(year from fecha)=:year"
        params['year'] = year
    if category!='todas':
        base_query += " and id_categoria_de_gasto=:category"
        params['category'] = category
    base_query += """
    GROUP BY EXTRACT(month FROM fecha), EXTRACT(YEAR FROM fecha)
    ORDER BY EXTRACT(YEAR FROM fecha), EXTRACT(month FROM fecha)
    """
    data=db.session.execute(text(base_query),params).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)

@dashboard_queries_bp.route('/manual/ingreso_mensual', methods=['POST','GET'])
@login_required
def ingreso_mensual():
    year = request.args.get("year")
    category=request.args.get("category")
    params = {}
    params['id_usuario'] = session['id_usuario']
    base_query=open('./static/sql/dashboard_queries/ingreso_mensual.sql','r',encoding='utf-8').read()
    if year!='historico':
        base_query += " and extract(year from fecha)=:year"
        params['year'] = year
    if category!='todas':
        base_query += " and id_categoria_de_ingreso=:category"
        params['category'] = category
    base_query += """
    GROUP BY EXTRACT(month FROM fecha), EXTRACT(YEAR FROM fecha)
    ORDER BY EXTRACT(YEAR FROM fecha), EXTRACT(month FROM fecha)
    """
    data=db.session.execute(text(base_query),params).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)
