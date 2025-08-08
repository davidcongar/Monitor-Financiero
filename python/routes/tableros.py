# python/routes/automatizaciones.py

from flask import Blueprint, render_template,jsonify,request
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.authentication import *
from datetime import datetime

tableros_bp = Blueprint("tableros", __name__,url_prefix="/tableros")
@tableros_bp.route("/inicio", methods=["GET","POST"])
@login_required
def inicio():
    data = {'activeMenu': 'inicio'}
    accounts_balance = db.session.execute(text(open('./static/sql/inicio/account_balance.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    income = db.session.execute(text(open('./static/sql/inicio/ingreso_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    expenses = db.session.execute(text(open('./static/sql/gastos/gastos_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    balance = db.session.execute(text(open('./static/sql/inicio/user_balance.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    balance_chart_data=db.session.execute(text(open('./static/sql/inicio/balance_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).fetchall()
    balance_chart_data = [dict(row._mapping) for row in balance_chart_data]
    return render_template('main/tableros/inicio.html', **data,accounts_balance=accounts_balance,balance=balance,income=income,expenses=expenses,balance_chart_data=balance_chart_data)

@tableros_bp.route("/gastos", methods=["GET","POST"])
@login_required
def gastos():
    data = {"activeMenu": "gastos","activeItem":"tablero"}
    anios=db.session.execute(text(open('./static/sql/gastos/anios.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    gastos_mensuales=db.session.execute(text(open('./static/sql/gastos/gastos_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    gastos_anuales=db.session.execute(text(open('./static/sql/gastos/gastos_cambio_anual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    categorias = CategoriasDeGastos.query.filter(CategoriasDeGastos.id_usuario==session['id_usuario']).order_by(CategoriasDeGastos.nombre).all()
    return render_template("main/tableros/gastos.html", **data,gastos_anuales=gastos_anuales,gastos_mensuales=gastos_mensuales,anios=anios,categorias=categorias)

@tableros_bp.route("/ingresos", methods=["GET","POST"])
@login_required
def ingresos():
    data = {"activeMenu": "ingresos","activeItem":"tablero"}
    anios=db.session.execute(text(open('./static/sql/gastos/anios.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    ingreso_mensual=db.session.execute(text(open('./static/sql/inicio/ingreso_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    ingreso_anual=db.session.execute(text(open('./static/sql/ingresos/ingreso_cambio_anual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    categorias = CategoriasDeIngresos.query.filter(CategoriasDeIngresos.id_usuario==session['id_usuario']).order_by(CategoriasDeIngresos.nombre).all()
    return render_template("main/tableros/ingresos.html", **data,ingreso_anual=ingreso_anual,ingreso_mensual=ingreso_mensual,anios=anios,categorias=categorias)

