import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *

class Cuentas(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    monto_credito = db.Column(db.Integer)
    dia_de_corte = db.Column(db.Integer)
    dia_de_pago = db.Column(db.Integer)
    estatus = db.Column(db.String(255),default="Activo")

class CategoriasDeIngresos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50),nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

class CategoriasDeGastos(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50),nullable=False)
    estatus = db.Column(db.String(255),default="Activo")
