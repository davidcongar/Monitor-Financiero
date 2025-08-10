# python/routes/files.py

from flask import (
    Blueprint,
    Response,
    flash,
    render_template,
    request,
)

from python.services.system.files import ExcelService, PDFService

files_bp = Blueprint("files", __name__, url_prefix="/files")

@files_bp.route("/excel/<string:kind>/<string:table>", methods=["GET"])
def excel(table,kind):
    """Ruta para generar y descargar un archivo Excel de una table específica."""
    try:
        excel_content, error = ExcelService.generate_excel(table,kind)


        if error:
            flash(f"No se pudo generar el archivo Excel: {error}", "danger")

        response = Response(
            excel_content,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={table}.xlsx"},
        )
        #flash(f"Se ha descargado el archivo: {table}.xlsx", "success")
        return response
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")


@files_bp.route("/download_pdf", methods=["Post"])
def pdf():
    """Generar y descargar un archivo PDF con los datos de un registro."""
    try:
        table = request.args.get("table")
        registro_id = request.args.get("id")
        logo= "./static/images/logo-dark.png"

        if not table or not registro_id:
            flash(
                "Error: No se proporcionó el nombre de la table o el ID del registro.",
                "danger",
            )
        
        pdf_content, error = PDFService.generate_pdf(table, registro_id, logo)

        if error:
            flash(f"No se pudo generar el archivo PDF: {error}", "danger")
        else:
            flash(
                f"El archivo PDF para el registro {registro_id} de {table} se generó correctamente.",
                "success",
            )

        response = Response(
            pdf_content,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={table}_{registro_id}.pdf"
            },
        )
        return response
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "danger")
