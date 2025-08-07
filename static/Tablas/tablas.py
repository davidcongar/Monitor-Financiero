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
from reportlab.platypus import Image

from python.models import db

class tabla_uno:
    
    def draw_header(canvas, _, logo, nombre_tabla):
                canvas.saveState()
                renderPDF.draw(svg2rlg(logo), canvas, 50, 720)
                canvas.setFont("Helvetica-Bold", 16)
                canvas.drawString(50, 660, f"Datos de la tabla: {nombre_tabla.replace('_', ' ')}")
                canvas.restoreState()

    def Tabla_uno(data):
        table = Table(data, colWidths=[150, 350])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        return table
    
class tabla_dos:
    
    def draw_header(canvas, _, logo, nombre_tabla):
        canvas.saveState()
        try:
            img = Image(logo, width=80, height=80)  # ajusta tamaño si es necesario
            img.drawOn(canvas, 50, 720)
        except Exception as e:
            canvas.setFont("Helvetica-Bold", 12)
            canvas.drawString(50, 750, f"Error al cargar logo: {str(e)}")

        canvas.setFont("Helvetica-Bold", 16)
        canvas.drawString(50, 660, f"Datos de la tabla: {nombre_tabla.replace('_', ' ')}")
        canvas.restoreState()


    def Tabla_dos(data):
        # Crear tabla con un diseño más dinámico
        table = Table(data, colWidths=[100, 250, 200])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, 1), colors.lightblue),
                ("TEXTCOLOR", (0, 1), (-1, 1), colors.black),
                ("ALIGN", (0, 1), (-1, 1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
                ("FONTNAME", (0, 2), (-1, -1), "Helvetica"),
            ])
        )
        return table
