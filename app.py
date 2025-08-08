# app.py

import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, flash, g, redirect, session, url_for
from flask_migrate import Migrate
from sqlalchemy import event, inspect

from flask_session import Session
from python.services.logs_auditoria import *
from python.models.modelos import db
from python.services.authentication import *

# Cargar variables de entorno
load_dotenv()

# Inicializar la Monitor Financiero Flask
app = Flask(__name__)

# Configuración de la Monitor Financiero
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)


# Configuración de la sesión
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(weeks=1)
Session(app)


@app.before_request
def make_session_permanent():
    """Hacer que la sesión sea permanente y respetar el tiempo de expiración."""
    session.permanent = True


# Configuración de Base de Datos
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
Session(app)

# Eventos para auditoría
event.listen(db.session, "before_flush", registrar_logs_auditoria)
event.listen(db.session, "after_flush", registrar_logs_post_flush)
event.listen(db.session, "after_commit", limpiar_bandera_auditoria)

# Configuración del usuario en `g`
@app.before_request
def set_usuario_email():
    """Asigna el email del usuario autenticado a `g.usuario_email`."""
    g.usuario_email = session.get("correo", None)


# Configuración de Tests
@app.cli.command("test")
def run_tests():
    """Ejecuta los tests de la Monitor Financiero."""
    print("\033[94mIniciando pruebas...\033[0m")

    from python.tests.test_cases import test_db_connection, test_health
    from python.tests.test_config import run_all_tests

    tests = [test_health, test_db_connection]
    errors = run_all_tests(tests)

    if errors:
        print(f"\n\033[91m{len(errors)} pruebas fallaron:\033[0m")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n\033[92m¡Todas las pruebas pasaron exitosamente!\033[0m")

# Registro de Blueprints
from python.routes.system.dynamic_routes import dynamic_bp
from python.routes.system.errors import errors_bp
from python.routes.system.generar_archivos import generar_archivos_bp
from python.routes.system.home import home_bp
from python.services.authentication import auth_bp
from python.services.api import api_bp
from python.routes.queries import queries_bp

app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(generar_archivos_bp)
app.register_blueprint(dynamic_bp)
app.register_blueprint(api_bp)
app.register_blueprint(queries_bp)

from python.routes.tableros import tableros_bp
from python.routes.reportes import reportes_bp

app.register_blueprint(tableros_bp)
app.register_blueprint(reportes_bp)



from python.services.template_formats import *

# Almacenar los nombres de las tablas en caché
TABLES_CACHE = {}


# Definir tablas a omitir
OMITIR_TABLAS = [
    f"alembic_version",
    f"logs_auditoria",
    f"archivos",
    f"logs_auditoria",
    f"relacion_rutas_usuarios",
    f"relacion_rutas_roles"
]


def load_table_names():
    """Carga los nombres de las tablas disponibles, excluyendo las especificadas en OMITIR_TABLAS."""
    global TABLES_CACHE
    engine = db.engine
    inspector = db.inspect(engine)

    # Filtrar solo tablas de la app
    filtered_tables = [
        table
        for table in inspector.get_table_names()
        if table not in OMITIR_TABLAS
    ]

    # Formatear nombres y almacenar en caché
    TABLES_CACHE = {
        table: table.replace("_", " ").title()
        for table in sorted(filtered_tables)
    }


# Solo cuando se inicia la app
with app.app_context():
    load_table_names()

@app.context_processor
def inject_table_names():
    """Inyecta las tablas pre-cargadas en las plantillas."""
    return {"table_names": TABLES_CACHE}


if __name__ == "__main__":
    app.run(debug=True)
