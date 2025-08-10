# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *

from python.services.system.authentication import *
from python.services.system.helper_functions import *

import io
from PIL import Image, ImageDraw, ImageFont


dashboard_queries_bp = Blueprint("dashboard_queries", __name__, url_prefix="/dashboard_queries")

@dashboard_queries_bp.route("/<string:sql_name>", methods=["GET"])
@login_required
def sql_data(sql_name):
    path = './static/sql/dashboard_queries/'+sql_name+'.sql'
    base_query = open(path, "r", encoding="utf-8").read()
    variables_query = extract_param_names(base_query)
    variables_request = {k: v for k, v in request.values.items() if k in variables_query and v != ""}
    if "id_usuario" in variables_query:
        variables_request["id_usuario"] = session["id_usuario"]
    data=db.session.execute(text(base_query),variables_request).fetchall()
    data = [dict(row._mapping) for row in data]
    return jsonify(data)

