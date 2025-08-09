# python/routes/files.py

from flask import (
    Blueprint,
    Response,
    flash,
    render_template,
    request,
)

from python.services.files import ExcelService, PDFService

files_bp = Blueprint("files", __name__, url_prefix="/files")

@files_bp.route("/excel/<string:tabla>", methods=["GET"])
def excel(tabla):
    """Ruta para generar y descargar un archivo Excel de una tabla específica."""
    try:
        excel_content, error = ExcelService.generate_excel(tabla)


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


@files_bp.route("/download_pdf", methods=["Post"])
def pdf():
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
        
        pdf_content, error = PDFService.generate_pdf(tabla, registro_id, logo)

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
