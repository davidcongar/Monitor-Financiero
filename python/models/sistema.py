import uuid
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from python.models import db

class BaseMixin:
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_visualizacion = db.Column(db.Integer)
    fecha_de_creacion = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    fecha_de_actualizacion = db.Column(db.DateTime, onupdate=db.func.now())

class AuditMixin:
    id_usuario = db.Column(db.UUID, db.ForeignKey("usuarios.id"), nullable=True)

class Usuarios(db.Model,BaseMixin):
    __tablename__ = "usuarios"

    nombre = db.Column(db.String(1000), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    contrasena_api=db.Column(db.UUID(as_uuid=True), default=uuid.uuid4)
    id_usuario_conectado=db.Column(db.UUID, db.ForeignKey("usuarios.id"), nullable=True)
    estatus = db.Column(db.String(255),default="Activo")

    usuario_conectado = db.relationship(
        "Usuarios",
        foreign_keys=[id_usuario_conectado],
        remote_side="Usuarios.id",
        backref=db.backref("conectado_por", uselist=False, lazy="select"),
        lazy="select"
    )

    # Métodos
    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<usuarios(id={self.id}, nombre={self.nombre}, correo={self.correo_electronico})>"

class LogsAuditoria(db.Model):
    __tablename__ = "logs_auditoria"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tabla = db.Column(db.String(255), nullable=False)
    id_registro = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), nullable=True, server_default="Desconocido")
    accion = db.Column(db.String(1000), nullable=False)
    datos_anteriores = db.Column(db.Text, nullable=True)
    datos_nuevos = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<LogsAuditoria {self.accion} en {self.tabla} registro {self.id_registro}>"
        )

class CategoriasDeReportes(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

class Reportes(db.Model,BaseMixin,AuditMixin):
    nombre = db.Column(db.String(50), nullable=False)
    id_categoria_de_reporte = db.Column(db.UUID,db.ForeignKey('categorias_de_reportes.id'),nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    ruta_sql = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.String(255),default="Activo")

    categoria = db.relationship("CategoriasDeReportes", backref="reportes", lazy=True)
