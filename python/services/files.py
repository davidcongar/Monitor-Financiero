# python/services/files.py

import io

import pandas as pd
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from svglib.svglib import svg2rlg
import os
from python.models import db
from static.Tablas.tablas import tabla_uno, tabla_dos


class ExcelService:
    @staticmethod
    def generate_excel(table_name):
        """Exporta los datos de una tabla a un archivo Excel."""
        try:
            query = text(f"SELECT * FROM {table_name}")
            result = db.session.execute(query)

            rows = [dict(row) for row in result.mappings()]

            if not rows:
                return None, "La tabla no contiene datos."

            df = pd.DataFrame(rows)

            # Exportar a excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name=table_name)

            output.seek(0)
            return output.getvalue(), None
        except Exception as e:
            return None, str(e)


class PDFService:
    @staticmethod
    def generate_pdf(table_name, id_record, logo):
        try:
            # Procesar nombre de tabla
            table_name = f"{table_name.split('/')[-1]}"
            if not table_name.isidentifier():
                return None, f"Nombre de tabla '{table_name}' inválido."

            # Consultar record
            query = text(f"SELECT * FROM {table_name} WHERE id = :id")
            record = db.session.execute(query, {"id": id_record}).mappings().first()
            if not record:
                return None, f"Registro con ID {id_record} no encontrado en {table_name}."
            
            record = dict(record)

            # Crear PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(name="Title", fontSize=16, alignment=TA_LEFT)
            cell_style = ParagraphStyle(name="Cell", fontSize=10, alignment=TA_LEFT, wordWrap='CJK')
            # Crear tabla
            data = [["Campo", "Valor"]] + [
                [Paragraph(k, cell_style), Paragraph(str(v) if v else "N/A", cell_style)]
                for k, v in record.items()
            ]
            tabla = tabla_dos.Tabla_dos(data)
            def encabezado(canvas, doc):
                tabla_dos.draw_header(canvas, doc, logo, table_name)

            # Generar PDF
            try:
                doc.build([Spacer(1, 100), tabla], onFirstPage=encabezado)
            except Exception as e:
                print("Error dentro de doc.build:")
                import traceback
                traceback.print_exc()
                return None, f"Error al construir PDF: {str(e)}"

            buffer.seek(0)
            return buffer.getvalue(), None

        except SQLAlchemyError as e:
            return None, f"Error de base de datos: {e}"
        except Exception as e:
            return None, str(e)
        