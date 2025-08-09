import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db
from python.models.sistema import *


class Ingresos(db.Model,BaseMixin,AuditMixin):
    id_cuenta = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    id_categoria_de_ingreso = db.Column(db.UUID,db.ForeignKey('categorias_de_ingresos.id'),nullable=False)
    fecha = db.Column(db.Date,nullable=False)
    importe = db.Column(db.Float,nullable=False)
    notas = db.Column(db.String(500))

    cuenta = db.relationship("Cuentas", backref="ingreso", lazy=True)
    categoria = db.relationship("CategoriasDeIngresos", backref="ingreso", lazy=True)

# Recurring income model
class IngresosRecurrentes(db.Model,BaseMixin,AuditMixin):
    id_cuenta = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    id_categoria_de_ingreso = db.Column(db.UUID,db.ForeignKey('categorias_de_ingresos.id'),nullable=False)
    importe = db.Column(db.Float,nullable=False)
    notas = db.Column(db.String(500))

    cuenta = db.relationship("Cuentas", backref="ingreso_recurrente", lazy=True)
    categoria = db.relationship("CategoriasDeIngresos", backref="ingreso_recurrente", lazy=True)

# gastos model
class Gastos(db.Model,BaseMixin,AuditMixin):
    id_cuenta = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    id_categoria_de_gasto = db.Column(db.UUID,db.ForeignKey('categorias_de_gastos.id'),nullable=False)
    id_negocio_apple_pay = db.Column(db.UUID,db.ForeignKey('negocios_apple_pay.id'),nullable=True)
    gasto_compartido = db.Column(db.String(255))
    categoria_apple_pay=db.Column(db.String(255))
    pagos_mensuales=db.Column(db.Integer,default=1)
    fecha = db.Column(db.Date,nullable=False)
    importe = db.Column(db.Float,nullable=False)
    notas = db.Column(db.String(500))

    cuenta = db.relationship("Cuentas", backref="gastos", lazy=True)
    categoria = db.relationship("CategoriasDeGastos", backref="gastos", lazy=True)
    negocio = db.relationship("NegociosApplePay", backref="gastos", lazy=True)

# Recurring gastos model
class GastosRecurrentes(db.Model,BaseMixin,AuditMixin):
    id_cuenta = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    id_categoria_de_gasto = db.Column(db.UUID,db.ForeignKey('categorias_de_gastos.id'),nullable=False)
    gasto_compartido = db.Column(db.String(50))
    importe = db.Column(db.Float,nullable=False)
    notas = db.Column(db.String(500))

    cuenta = db.relationship("Cuentas", backref="gastos_recurrentes", lazy=True)
    categoria = db.relationship("CategoriasDeGastos", backref="gastos_recurrentes", lazy=True)

class Transferencias(db.Model,BaseMixin,AuditMixin):
    id_cuenta_entrada = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    id_cuenta_salida = db.Column(db.UUID,db.ForeignKey('cuentas.id'),nullable=False)
    fecha = db.Column(db.Date,nullable=False)
    importe = db.Column(db.Float,nullable=False)
    notas = db.Column(db.String(500))

    cuenta_entrada = db.relationship(
        "Cuentas",
        foreign_keys=[id_cuenta_entrada],
        backref="transferencias_entrada",
        lazy=True
    )

    cuenta_salida = db.relationship(
        "Cuentas",
        foreign_keys=[id_cuenta_salida],
        backref="transferencias_salida",
        lazy=True
    )