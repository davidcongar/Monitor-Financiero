# python/routes/authentication.py


from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from python.models import db
from python.models.modelos import *
from python.services.email import *
from functools import wraps 
import secrets
import string
from sqlalchemy import or_,and_,cast, String,func,text

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_usuario' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def routes_accessible_by_user(id_user, id_role):
    """
    Preload all routes the user and their role have access to.
    """
    query = """
    SELECT DISTINCT r.ruta
    FROM rutas r
    LEFT JOIN relacion_rutas_usuarios u ON r.id = u.id_ruta AND u.id_usuario = :id_usuario
    LEFT JOIN relacion_rutas_roles ro ON r.id = ro.id_ruta AND ro.id_rol = :id_rol
    WHERE u.id_usuario IS NOT NULL OR ro.id_rol IS NOT NULL
    """
    result = db.session.execute(text(query), {'id_usuario': id_user, 'id_rol': id_role}).fetchall()
    session['accessible_routes'] = {row[0] for row in result} 

def access_control(path):
    """
    Check if the current user has access to the given path using cached routes.
    """
    id_user = session.get('id_usuario')
    id_role = session.get('id_rol')
    accessible_routes = session.get('accessible_routes')

    if not id_user or not id_role or not accessible_routes:
        return False

    if path in accessible_routes:
        return True
    # Check parent paths
    while path:
        path = path.rsplit('/', 1)[0]  # Remove the last segment
        if path in accessible_routes:
            return True
    # Check root route
    return '/' in accessible_routes

def roles_required():
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            path = request.path
            if not access_control(path):
                flash("No tienes permiso para acceder al módulo/funcionalidad seleccionada.", "danger")
                return redirect(request.referrer or '/')
            return func(*args, **kwargs)
        return wrapped_function
    return decorator

auth_bp = Blueprint("auth", __name__, url_prefix="/authentication")

@auth_bp.route("/login")
def login():
    return render_template("authentication/login.html")

@auth_bp.route("/signin")
def signin():
    return render_template("authentication/signin.html")

@auth_bp.route('/login_submit', methods=['POST'])
def login_submit():
    correo_electronico = request.form['correo_electronico']
    contrasena = request.form['contrasena']
    usuario = Usuarios.query.filter(Usuarios.correo_electronico==correo_electronico).first()
    if usuario!=None:
        if check_password_hash(usuario.contrasena, contrasena):
            session['id_usuario'] = usuario.id
            session['nombre'] = usuario.nombre
            session['correo'] = usuario.correo_electronico
            flash(f"¡Bienvenido, {usuario.nombre}!", "success")
            return redirect(url_for("home.inicio"))
        else:
            flash("Información incorrecta. Inténtalo nuevamente.", "warning")
            return redirect(url_for("auth.login"))
    else:
        flash("Información incorrecta. Inténtalo nuevamente.", "warning")
        return redirect(url_for("auth.login"))

@auth_bp.route("/forgotpassword")
def forgot_password():
    return render_template("authentication/forgotpassword.html")

@auth_bp.route('/forgotpassword_submit', methods=['POST'])
def forgotpassword_submit():
    correo_electronico = request.form['correo_electronico']
    usuario = Usuarios.query.filter(Usuarios.correo_electronico==correo_electronico).first()
    if usuario!=None:
        # envia correo
        alphabet = string.ascii_letters + string.digits
        contrasena = ''.join(secrets.choice(alphabet) for i in range(20))
        forgot_password_email(correo_electronico,contrasena)
        usuario.contrasena=generate_password_hash(contrasena)
        db.session.commit()
        flash("Se ha enviado un correo electrónico con tu nueva contraseña.", "success")
        return redirect(url_for('auth.login'))
    else:
        flash("Correo electrónico es incorrecto. Inténtalo nuevamente.", "danger")
        return redirect(url_for('auth.forgot_password'))


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))