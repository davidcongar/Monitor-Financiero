
// funcion para hacer graficas con mas de una categoria
function generar_grafica_categorias(nombre_grafica, tipo_grafica,x_key,y_key,z_key, path,options) {
    fetch(path)
        .then(response => {
            if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) throw new Error("Fetched data is not an array.");
            const xValues = [...new Set(data.map(item => item[x_key]))];
            const zValues = [...new Set(data.map(item => item[z_key]))];
            const series = zValues.map(z => {
                return {
                    name: (typeof z === 'number' || (!isNaN(z) && z.trim && z.trim() !== ''))
                        ? String(z)
                        : capitalizeWords(z),
                    data: xValues.map(x => {
                        const match = data.find(d => d[x_key] === x && d[z_key] === z);
                        return match ? match[y_key] : null; // or 0 if you prefer
                    })
                };
            });
            renderizar_grafica(nombre_grafica, tipo_grafica, series, xValues, options);
        })
        .catch(error => {
            console.error("Error fetching or processing data:", error);
        });
}
function generar_grafica(nombre_grafica, tipo_grafica,dataXKey, dataYKey,path,options) {
    fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Check if data is an array
            if (!Array.isArray(data)) {
                throw new Error("Fetched data is not an array.");
            }
            const y = data.map(item => Number(item[dataYKey]));
            const x = data.map(item => item[dataXKey]);
            
            if(tipo_grafica==='pie'){
                renderizar_pie(nombre_grafica,y,x);
            }else if(tipo_grafica==='avance'){
                y.push(1 - y[0]);  // Converts the result to a string before pushing
                renderizar_avance(nombre_grafica, "bar", y, x, {valueType: valor_tipo});
            }else{
                renderizar_grafica(nombre_grafica, tipo_grafica, y, x,options);
            }
        })
        .catch(error => {
            console.error("Error fetching or processing data:", error);
        });
}

// funcion para generar grafica general
function renderizar_grafica(selector, chartType, data_y, data_x, options = {}) {
    if (!selector || !document.querySelector(selector)) {
        console.error("Invalid selector or element not found:", selector);
        return;
    }

    const valueType = options.valueType || "normal"; // "percent", "currency", or "normal"

    // Define custom formatter based on valueType
    const yAxisFormatter = value => {
        switch (valueType) {
            case "percent":
                return `${(value * 100).toFixed(1)}%`; // assumes value is in 0–1 range
            case "currency":
                return `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
            case "normal":
            default:
                return value.toLocaleString();
        }
    };
    const defaultOptions = {
        series: 
            Array.isArray(data_y) && data_y.length && typeof data_y[0] === "object" && "data" in data_y[0]
            ? data_y
            : [{ name: options.seriesName || "", data: data_y }],
        chart: {
            height: 280,
            type: chartType || "bar",
            events: options.events || {},
            toolbar: {
                show: false,
            },
            fontFamily: "Inter, sans-serif",
        },
        stroke: {
            width: 2,
            curve: 'smooth',
        },
        colors: options.colors || [
            "#267DFF","#7B6AFE","#FF51A4","#FF7C51","#00D085","#FFC41F","#FF3232",
        ],
        plotOptions: {
            bar: {
                columnWidth: "60%",
                distributed: true,
                borderRadius: 5,
                ...options.plotOptions?.bar,
            },
        },
        dataLabels: {
            enabled: false,
            ...options.dataLabels,
        },
        legend: {
            show: true,
            ...options.legend,
        },
        yaxis: {
            axisBorder: { show: false },
            axisTicks: { show: false },
            tickAmount: 5,
            labels: {
                formatter: yAxisFormatter,
                offsetX: -10,
                offsetY: 0,
                style: {
                    fontSize: "12px",
                    fontWeight: "600",
                    colors: "#7780A1",
                    cssClass: "apexcharts-xaxis-title",
                },
            },
            opposite: false,
            ...options.yaxis,
        },
        xaxis: {
            tickAmount: 7,
            axisBorder: { show: false },
            axisTicks: { show: false },
            categories: data_x,
            labels: {
                style: {
                    fontSize: "12px",
                    fontWeight: "600",
                    colors: "#7780A1",
                    cssClass: "apexcharts-xaxis-title",
                },
            },
            ...options.xaxis,
        },
        grid: {
            borderColor: "#e0e6ed",
            strokeDashArray: 2,
            xaxis: { lines: { show: false } },
            yaxis: { lines: { show: true } },
            padding: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 25,
            },
            ...options.grid,
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    const chartKey = selector.replace(/[^a-zA-Z0-9]/g, "");
    if (window[chartKey]) { window[chartKey].destroy() }
    window[chartKey] = new ApexCharts(document.querySelector(selector), mergedOptions);
    window[chartKey].render();
}
function renderizar_pie(selector, data_y, data_x, options = {}) {
    if (!selector || !document.querySelector(selector)) {
        console.error("Invalid selector or element not found:", selector);
        return;
    }

    // Ensure data_y is numeric
    const numericData_y = data_y.map(value => {
        const parsedValue = parseInt(value, 10);
        return isNaN(parsedValue) ? 0 : parsedValue; // Fallback to 0 if parsing fails
    });

    // Calculate the total sum of the values for percentage calculation
    const total = numericData_y.reduce((sum, val) => sum + val, 0);

    // Basic options for the pie chart
    const simpleOptions = {
        series: numericData_y,  // The series holds the values for the pie chart
        chart: {
            height: 280,
            type: "pie",  // Pie chart
            toolbar: { show: false },  // Disable toolbar
        },
        labels: data_x,  // Labels for pie chart slices
        colors: options.colors || [
            "#267DFF","#7B6AFE","#FF51A4","#FF7C51","#00D085","#FFC41F","#FF3232",
        ],
        dataLabels: {
            enabled: true,  // Enable data labels for pie charts
            formatter: (val, opts) => {
                // Calculate the percentage for each slice
                // Format the value with commas and add percentage
                const formattedValue = `${val.toFixed(1).toLocaleString()}%`;
                return formattedValue;
            },
        },
        tooltip: {
            enabled: true,
            y: {
                formatter: (val) => {
                    // Format the tooltip value with commas
                    return `${val.toLocaleString()}`; // You can also add percentage here if desired
                },
            },
            style: {
                fontSize: '14px',
                color: '#ffffff'  // 👈 This sets the tooltip text color to white
            },
                theme: "dark", // 👈 Use dark theme so white text is readable

        },
        legend: {
            show: true,  // Show legend
        },
    };

    // Merge options with simple options
    const mergedOptions = { ...simpleOptions, ...options };

    // Log the merged options to check everything is set correctly

    // Clean selector to make a valid chart key (remove invalid characters)
    const chartKey = selector.replace(/[^a-zA-Z0-9]/g, "");

    try {
        // Create and render the chart
        window[chartKey] = new ApexCharts(document.querySelector(selector), mergedOptions);
        window[chartKey].render();
    } catch (e) {
        console.error('Error rendering chart:', e);
    }
}



