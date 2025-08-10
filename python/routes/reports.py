# python/routes/automatizaciones.py

from flask import Blueprint, render_template,jsonify,request
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.authentication import *
from datetime import datetime

reports_bp = Blueprint("reports", __name__,url_prefix="/reports")
@reports_bp.route("/gastos_compartidos", methods=["GET","POST"])
@login_required
def gastos_compartidos():
    data = {'activeMenu': 'gastos_compartidos',"activeItem":"reportes"}
    return render_template('main/reports/gastos_compartidos.html', **data)
