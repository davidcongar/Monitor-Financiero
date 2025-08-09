document.addEventListener('alpine:init', () => {
    Alpine.store('modalData', { record: {} });
});
function redirectActions(url) {
        if (url.includes("delete")) {
            // Para eliminación se confirma y se envía por POST
            if (confirm('¿Quieres eliminar el registro seleccionado?')) {
                const form = document.getElementById('action_buttons');
                form.action = url;
                form.method = "POST";
                form.submit();
            }
        } else if (url.includes("download_pdf")) {
            // Para descargar PDF se utiliza fetch y se procesa la descarga
            fetch(url, { method: "POST" })
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    } else {
                        throw new Error("No se pudo descargar el archivo.");
                    }
                })
                .then(blob => {
                    const downloadUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = downloadUrl;
                    a.download = `${url.split("=")[2]}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.location.reload();
                })
                .catch(error => {
                    alert("Error al descargar el archivo: " + error.message);
                });
        } else {
            window.location.href = url;
        }
}
function formatKey(key) {
        return key
            .replace(/_/g, ' ')
            .split(' ')
            .map(word => word.toLowerCase() === 'id' ? 'ID' : word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
}
function formatCurrency(value) {
        // Ensure it's a valid number, then format it as currency
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
}
function formatNumber(value) {
        // Format number with commas as thousands separators
        return new Intl.NumberFormat('en-US').format(value);
}
async function openActions(form, recordId,estatus) {
        showLoader();
        document.getElementById('id_registro').textContent=recordId;
        document.getElementById('estatus').textContent=estatus;

        const updateButton = document.querySelector('button[data-action="actualizar"]');
        const deleteButton = document.querySelector('button[data-action="delete"]');
        const downloadButton = document.querySelector('button[data-action="descargar"]');

        updateButton.setAttribute('onclick', `redirectActions('/${form}/form?id=${recordId}')`);
        deleteButton.setAttribute('onclick', `redirectActions('/${form}/delete?id=${recordId}')`);
        downloadButton.setAttribute('onclick', `redirectActions('/files/download_pdf?tabla=${form}&id=${recordId}')`);
        const data = await get_record(form, recordId);
        const popupActions = document.getElementById('modal');
        console.log("data =", data);
        Alpine.store('modalData').record = data;
        popupActions.classList.remove('hidden');
        hideLoader();
}
function closeActions() {
        const popupActions = document.getElementById('modal');
        const container = document.getElementById('contenido_modal');
        container.innerHTML = ''; 
        popupActions.classList.add('hidden');
}
async function get_record(form, recordId) {
        try {
            const path = `/${form}/data/${recordId}`;
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const data = await response.json();
            const record = data[0]; // first record
            const recordObj = Object.fromEntries(record);

            const container = document.getElementById('contenido_modal');
            container.innerHTML = '';

            for (const [key, rawValue] of Object.entries(recordObj)) {
                let value = rawValue;
                if(key==='id_visualizacion'){
                    document.getElementById('id_registro').textContent=value;
                }

                if (/(importe|monto|precio)/i.test(key) && !isNaN(value)) {
                    value = formatCurrency(value);
                } else if (!isNaN(value)) {
                    value = formatNumber(value);
                }

                const p = document.createElement('p');
                p.innerHTML = `<strong>${formatKey(key)}:</strong> <span id="modal${key}">${value}</span>`;
                container.appendChild(p);
            }
            return recordObj;
        } catch (error) {
            console.error("Error fetching or processing data:", error);
            return null; 
        }
}