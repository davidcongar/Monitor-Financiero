// static/js/dynamic_table_init.js

document.addEventListener("alpine:init", () => {
    // Obtener el elemento que contiene la data
    const tableDataElement = document.getElementById("table-data");
    const tableName = tableDataElement ? tableDataElement.getAttribute("data-table") : "";
    // Leer el array de columnas (en formato JSON)
    const tableColumns = tableDataElement ? JSON.parse(tableDataElement.getAttribute("data-columns")) : [];
    // Inicializar el componente Alpine para la tabla de datos
    Alpine.data("tabla", () => {
        return createDataTable({
            apiEndpoint: `${tableName}`, // Asegúrate de que este endpoint esté implementado en Flask
            view: 50,
            offset: 5,
            defaultSortField: "fecha_de_creacion",
            defaultSortRule: "desc",
            searchKeys: tableColumns,
            columns: tableColumns,
        });
    });
});

document.addEventListener("alpine:init", () => {
    // Obtener el elemento que contiene la data
    const tableDataElement = document.getElementById("table-data2");
    if (!tableDataElement) {
        return; // Salir si el elemento no existe
    }
    const tableName = tableDataElement ? tableDataElement.getAttribute("data-table") : "";
    // Leer el array de columnas (en formato JSON)
    const tableColumns = tableDataElement ? JSON.parse(tableDataElement.getAttribute("data-columns")) : [];
    // Inicializar el componente Alpine para la tabla de datos
    Alpine.data("tabla2", () => {
        return createDataTable({
            apiEndpoint: `${tableName}`, // Asegúrate de que este endpoint esté implementado en Flask
            view: 50,
            offset: 5,
            defaultSortField: "fecha_de_creacion",
            defaultSortRule: "desc",
            searchKeys: tableColumns,
            columns: tableColumns,
        });
    });
});