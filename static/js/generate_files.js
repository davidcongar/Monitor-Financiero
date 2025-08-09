// static/js/generate_excel.js

function generate_excel(table,kind) {
    const baseUrl = `/files/excel/${kind}/${table}`;
    const currentParams = window.location.search; // includes the "?" if present
    const url = currentParams ? `${baseUrl}${currentParams}` : baseUrl;

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
            a.download = `${table}.xlsx`;
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
