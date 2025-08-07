// static/js/generar_excel.js

function generarExcel(tabla) {
    const url = `/generar_archivos/excel/${tabla}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al generar el archivo Excel");
            }
            return response.blob();
        })
        .then(blob => {
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = downloadUrl;
            a.download = `${tabla}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            message='Se ha descargado el archivo exitosamente.'
            window.dispatchEvent(new CustomEvent('show-success', { detail: message}));
        })
        .catch(error => {
            console.error("Error:", error);
            alert("No se pudo generar el archivo Excel.");
        });
}
