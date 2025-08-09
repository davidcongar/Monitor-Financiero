# python/routes/home.py

from flask import Blueprint, render_template, jsonify, request, Response, session
from sqlalchemy import or_, and_, cast, String, func, text
from python.models.modelos import *

from python.services.authentication import *

import io
from PIL import Image, ImageDraw, ImageFont
from python.services.helper_functions import *

report_queries_bp = Blueprint("report_queris", __name__, url_prefix="/report_queris")

SQL_QUERIES = {
    "movimientos_cuentas": "./static/sql/cuentas/movimientos.sql"
}

@report_queries_bp.route("/<string:sql_name>", methods=["GET"])
@login_required
def report_queris(sql_name):
    table_name=sql_name
    path = SQL_QUERIES.get(sql_name)
    base_query = open(path, "r", encoding="utf-8").read()
    variables_query = extract_param_names(base_query)
    variables_request = {k: v for k, v in request.values.items() if k in variables_query and v != ""}
    if "id_usuario" in variables_query:
        variables_request["id_usuario"] = session["id_usuario"]
    data=db.session.execute(text(base_query),variables_request)
    columns =  list(data.keys())
    return render_template(
        "dynamic_table.html",
        columns=columns,
        table_name=table_name,
        reporte=1
    )

@report_queries_bp.route("/<string:sql_name>/data", methods=["GET"])
@login_required
def data(sql_name):
    path = SQL_QUERIES.get(sql_name)
    with open(path, "r", encoding="utf-8") as f:
        base_query = f.read().strip()

    # build params from request + session
    variables_query = extract_param_names(base_query)
    variables_request = {k: v for k, v in request.values.items() if k in variables_query and v != ""}
    if "id_usuario" in variables_query:
        variables_request["id_usuario"] = session["id_usuario"]

    # --- dynamic table inputs ---
    view      = request.args.get("view", 50, type=int)
    search    = request.args.get("search", "", type=str)
    sortField = request.args.get("sortField", "fecha", type=str)
    sortRule  = request.args.get("sortRule", "desc", type=str)
    page      = request.args.get("page", 1, type=int)

    # 1) get columns from the base query (no rows)
    #    Postgres syntax for subquery alias; adjust alias quoting for other DBs if needed
    probe_sql = text(f"SELECT * FROM ({base_query}) AS base_q LIMIT 0")
    probe_res = db.session.execute(probe_sql, variables_request)
    columns = list(probe_res.keys())

    # validate sort field
    sortField = 'fecha'
    sortDir = "ASC" if sortRule.lower() == "asc" else "DESC"

    # 2) build WHERE for search (case-insensitive). For Postgres, use ILIKE + CAST.
    where_clause = ""
    params = dict(variables_request)
    if search:
        like_param = f"%{search}%"
        params["search"] = like_param
        # ILIKE for Postgres; if MySQL/SQLite, change to LIKE and maybe LOWER(...)
        ors = " OR ".join([f"CAST({col} AS TEXT) ILIKE :search" for col in columns])
        where_clause = f"WHERE ({ors})"

    # 3) total count
    count_sql = text(f"""
        SELECT COUNT(*) AS total
        FROM ({base_query}) AS base_q
        {where_clause}
    """)
    total = db.session.execute(count_sql, params).scalar() or 0

    # 4) data page
    params["limit"] = view
    params["offset"] = max(page - 1, 0) * view
    data_sql = text(f"""
        SELECT *
        FROM ({base_query}) AS base_q
        {where_clause}
        ORDER BY {sortField} {sortDir}
        LIMIT :limit OFFSET :offset
    """)
    result = db.session.execute(data_sql, params)
    items = [rowmapping_to_dict(rm) for rm in result.mappings().all()]

    return jsonify(
        {
            "items": items,
            "total": total,
            "pages": (total + view - 1) // view, 
        }
    )