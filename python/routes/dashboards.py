# python/routes/automatizaciones.py

from flask import Blueprint, render_template,jsonify,request
from sqlalchemy import or_,and_,cast, String,func,text,extract
from python.models.modelos import *
from python.services.system.authentication import *
from datetime import datetime

dashboards_bp = Blueprint("dashboards", __name__,url_prefix="/dashboards")
@dashboards_bp.route("/home", methods=["GET","POST"])
@login_required
def home():
    data = {'activeMenu': 'inicio'}
    accounts_balance = db.session.execute(text(open('./static/sql/dashboard_queries/balances_de_cuentas.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    income = db.session.execute(text(open('./static/sql/dashboard_queries/ingreso_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    expenses = db.session.execute(text(open('./static/sql/dashboard_queries/gastos_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    balance = db.session.execute(text(open('./static/sql/dashboard_queries/balance_usuario.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    balance_chart_data=db.session.execute(text(open('./static/sql/dashboard_queries/balance_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).fetchall()
    balance_chart_data = [dict(row._mapping) for row in balance_chart_data]
    return render_template('main/dashboards/home.html', **data,accounts_balance=accounts_balance,balance=balance,income=income,expenses=expenses,balance_chart_data=balance_chart_data)

@dashboards_bp.route("/gastos", methods=["GET","POST"])
@login_required
def gastos():
    data = {"activeMenu": "gastos","activeItem":"tablero"}
    years=db.session.execute(text(open('./static/sql/dashboard_queries/years.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    gastos_mensuales=db.session.execute(text(open('./static/sql/dashboard_queries/gastos_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    gastos_anuales=db.session.execute(text(open('./static/sql/dashboard_queries/gastos_cambio_anual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    categorias = CategoriasDeGastos.query.filter(CategoriasDeGastos.id_usuario==session['id_usuario']).order_by(CategoriasDeGastos.nombre).all()
    return render_template("main/dashboards/gastos.html", **data,gastos_anuales=gastos_anuales,gastos_mensuales=gastos_mensuales,years=years,categorias=categorias)

@dashboards_bp.route("/ingresos", methods=["GET","POST"])
@login_required
def ingresos():
    data = {"activeMenu": "ingresos","activeItem":"tablero"}
    years=db.session.execute(text(open('./static/sql/dashboard_queries/years.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    ingreso_mensual=db.session.execute(text(open('./static/sql/dashboard_queries/ingreso_cambio_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    ingreso_anual=db.session.execute(text(open('./static/sql/dashboard_queries/ingreso_cambio_anual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).first()
    categorias = CategoriasDeIngresos.query.filter(CategoriasDeIngresos.id_usuario==session['id_usuario']).order_by(CategoriasDeIngresos.nombre).all()
    return render_template("main/dashboards/ingresos.html", **data,ingreso_anual=ingreso_anual,ingreso_mensual=ingreso_mensual,years=years,categorias=categorias)

@dashboards_bp.route("/gastos_compartidos", methods=["GET","POST"])
@login_required
def gastos_compartidos():
    usuario=Usuarios.query.filter_by(id=session['id_usuario']).first()
    nombre_usuario_compartido=Usuarios.query.filter_by(id=usuario.id_usuario_conectado).first()
    data = {"activeMenu": "gastos_compartidos","activeDefTab": "tablero"}
    years=db.session.execute(text(open('./static/sql/dashboard_queries/years.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario']}).all()
    categorias=db.session.execute(text(open('./static/sql/dashboard_queries/compartido_categorias.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado}).all()
    # dashboard data
    monthly_expenses=db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gasto_mensual_cambio.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado}).first()
    yearly_expenses=db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gasto_anual_cambio.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado}).first()
    if request.method == 'POST':
        month=request.form['month']
        year=request.form['year']
        fecha=year+'-'+month+'-01'
        fecha=datetime.strptime(fecha, "%Y-%m-%d")
        monthly_shared_expenses = db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gastos_resumen_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado,'fecha':fecha})
        remaining_shared_expenses = db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gasto_restante.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado,'fecha':fecha})
        return render_template('main/dashboards/gastos_compartidos.html', **data,shared_user=usuario.id_usuario_conectado,
                               monthly_shared_expenses=monthly_shared_expenses,month=month,year=year,remaining_shared_expenses=remaining_shared_expenses,
                               yearly_expenses=yearly_expenses,monthly_expenses=monthly_expenses,nombre_usuario_compartido=nombre_usuario_compartido.nombre)
    else:
        monthly_shared_expenses = db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gastos_resumen_mensual.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado,'fecha':datetime.now()})
        remaining_shared_expenses = db.session.execute(text(open('./static/sql/dashboard_queries/compartido_gasto_restante.sql','r',encoding='utf-8').read()), {'id_usuario': session['id_usuario'],'id_usuario_conectado': usuario.id_usuario_conectado,'fecha':datetime.now()})
        return render_template('main/dashboards/gastos_compartidos.html', **data,
                               monthly_shared_expenses=monthly_shared_expenses,remaining_shared_expenses=remaining_shared_expenses,
                               yearly_expenses=yearly_expenses,monthly_expenses=monthly_expenses,years=years,categories=categorias,nombre_usuario_compartido=nombre_usuario_compartido.nombre)

@dashboards_bp.route('/manual/gasto_mensual', methods=['GET'])
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

@dashboards_bp.route('/manual/ingreso_mensual', methods=['POST','GET'])
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
