# python/routes/generar_archivos.py

from flask import (
    Blueprint,
    Response,
    flash,
    render_template,
    request,
)

from python.services.generar_archivos import GenerarExcelService, GenerarPDFService

generar_archivos_bp = Blueprint(
    "generar_archivos", __name__, url_prefix="/generar_archivos"
)


@generar_archivos_bp.route("/excel/<string:tabla>", methods=["GET"])
def descargar_excel(tabla):
    """Ruta para generar y descargar un archivo Excel de una tabla específica."""
    try:
        excel_content, error = GenerarExcelService.generar_excel(tabla)


        if error:
            flash(f"No se pudo generar el archivo Excel: {error}", "danger")

        response = Response(
            excel_content,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={tabla}.xlsx"},
        )
        #flash(f"Se ha descargado el archivo: {tabla}.xlsx", "success")
        return response
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")


@generar_archivos_bp.route("/descargar_pdf", methods=["Post"])
def descargar_pdf():
    """Generar y descargar un archivo PDF con los datos de un registro."""
    try:
        tabla = request.args.get("tabla")
        registro_id = request.args.get("id")
        logo= "./static/images/logo-dark.png"

        if not tabla or not registro_id:
            flash(
                "Error: No se proporcionó el nombre de la tabla o el ID del registro.",
                "danger",
            )
        
        pdf_content, error = GenerarPDFService.generar_pdf(tabla, registro_id, logo)

        if error:
            flash(f"No se pudo generar el archivo PDF: {error}", "danger")
        else:
            flash(
                f"El archivo PDF para el registro {registro_id} de {tabla} se generó correctamente.",
                "success",
            )

        response = Response(
            pdf_content,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={tabla}_{registro_id}.pdf"
            },
        )
        return response
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")
