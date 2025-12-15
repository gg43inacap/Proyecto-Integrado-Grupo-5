document.addEventListener('DOMContentLoaded', function () {
    // Inicializar AOS
    AOS.init({
        duration: 800,
        easing: 'ease-in-out-cubic',
        once: false,
        mirror: true
    });

    // Datos
    const dataD1 = window.REM24.d1;
    const dataD2 = window.REM24.d2;
    const dataD3 = window.REM24.d3;

    const colors = {
        primary: '#2563eb',
        secondary: '#1e40af',
        accent: '#7c3aed',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444'
    };

    // Gráfico 1 - Barras
    new ApexCharts(document.querySelector('#chart1'), {
        series: [{ name: dataD1.title, data: dataD1.values }],
        chart: { type: 'bar', height: 350, toolbar: { show: true } },
        plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
        colors: [colors.primary],
        dataLabels: { enabled: true },
        xaxis: {
            categories: dataD1.labels,
            labels: { rotate: -45 },
            title: {
                text: 'Rangos de peso al nacer (en gramos)',
                style: { fontSize: '14px', fontWeight: 500, color: '#333' }
            }
        },
        tooltip: { y: { formatter: val => val + " casos" } }
    }).render();

    // --- Reordenar etiquetas y valores de D2 ---
    const pairsD2 = dataD2.labels.map((label, i) => ({
        label,
        value: dataD2.values[i]
    }));

    // Mueve "Cesárea" al inicio y deja el resto en su orden original
    const reorderedD2 = [
        ...pairsD2.filter(p => p.label === "Cesárea"),
        ...pairsD2.filter(p => p.label !== "Cesárea")
    ];

    const dataD2Reordered = {
        title: dataD2.title,
        labels: reorderedD2.map(p => p.label),
        values: reorderedD2.map(p => p.value)
    };

    // Gráfico 2 - Barras
    new ApexCharts(document.querySelector('#chart2'), {
        series: [{ name: dataD2Reordered.title, data: dataD2Reordered.values }],
        chart: {
            type: 'bar',
            height: 420,
            toolbar: { show: true },
            parentHeightOffset: 0
        },
        plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
        colors: [colors.success],
        dataLabels: {
            enabled: true,
            style: { fontSize: '12px', fontWeight: 'bold', colors: ['#333'] }
        },
        xaxis: {
            categories: dataD2Reordered.labels,
            labels: {
                rotate: -45,
                trim: false,
                style: { fontSize: '12px', fontWeight: 400, colors: '#333' }
            },
            title: {
                text: 'Indicadores de atención inmediata del recién nacido',
                offsetY: 20,
                style: { fontSize: '14px', fontWeight: 500, color: '#333' }
            }
        },
        grid: { padding: { bottom: 20 } },
        tooltip: { y: { formatter: val => `${val} atenciones registradas` } }
    }).render();

    // Gráfico 3 - Barras
    new ApexCharts(document.querySelector('#chart3'), {
        series: [{ name: dataD3.title, data: dataD3.values }],
        chart: { type: 'bar', height: 350, toolbar: { show: true } },
        plotOptions: { bar: { borderRadius: 4, columnWidth: '55%' } },
        colors: [colors.warning],
        dataLabels: { enabled: true },
        xaxis: {
            categories: dataD3.labels,
            labels: { rotate: -45 },
            title: {
                text: 'RN ≥ 2500 g con lactancia materna en los primeros 60 minutos',
                style: { fontSize: '14px', fontWeight: 500, color: '#333' }
            }
        },
            yaxis: {
            labels: {
                formatter: function (val) {
                    return Math.round(val); //  fuerza a enteros
                }
            }
        },

        tooltip: { y: { formatter: val => `${val} RN con LM ≤ 60 min` } }
    }).render();

    // DataTables
    $('#table1, #table2, #table3').DataTable({
        language: { url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' },
        pageLength: 100,
        dom: '<"top">rt<"bottom">',
        searching: false,
        paging: false,
        info: false
    });

    // Funciones globales
    window.fullscreen = function (btn) {
        const card = btn.closest('.card-enterprise');
        if (card.requestFullscreen) card.requestFullscreen();
    };

    window.drilldown = function (section, item) {
        alert(`Drill-down: ${section} - ${item}`);
    };

    window.resetDrilldown = function () {
        location.reload();
    };

    window.downloadData = function (tableId) {
        alert(`Descargando datos de ${tableId}`);
    };

    window.exportJSON = function () {
        const data = {
            titulo: window.REM24.titulo,
            periodo: window.REM24.periodo,
            seccion_d1: dataD1,
            seccion_d2: dataD2,
            seccion_d3: dataD3
        };
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reporte_rem_a24.json';
        a.click();
    };

    window.exportPowerBI = function () {
        const data = {
            titulo: window.REM24.titulo,
            periodo: window.REM24.periodo,
            timestamp: new Date().toISOString(),
            secciones: [
                { nombre: 'Sección D1', datos: dataD1.labels.map((l, i) => ({ indicador: l, cantidad: dataD1.values[i] })) },
                { nombre: 'Sección D2', datos: dataD2.labels.map((l, i) => ({ indicador: l, cantidad: dataD2.values[i] })) },
                { nombre: 'Sección D3', datos: dataD3.labels.map((l, i) => ({ indicador: l, cantidad: dataD3.values[i] })) }
            ]
        };

        let csv = 'Sección,Indicador,Cantidad,Período\n';
        data.secciones.forEach(sec => {
            sec.datos.forEach(item => {
                csv += `"${sec.nombre}","${item.indicador}",${item.cantidad},"${data.periodo}"\n`;
            });
        });

        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reporte_rem_a24_powerbi_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
    };

    window.applyFilters = function () {
        const mes = document.getElementById('mes').value;
        const anio = document.getElementById('anio').value;
        window.location.href = `?mes=${mes}&anio=${anio}`;
    };

    // Comparativa
    function updateComparison() {
        const totalD1 = dataD1.values.reduce((a, b) => a + b, 0);
        const totalD2 = dataD2.values.reduce((a, b) => a + b, 0);
        const totalD3 = dataD3.values.reduce((a, b) => a + b, 0);

        document.getElementById('compD1').textContent = totalD1;
        document.getElementById('compD2').textContent = totalD2;
        document.getElementById('compD3').textContent = totalD3;
        document.getElementById('totalRecords').textContent = (totalD1 + totalD2 + totalD3).toLocaleString();
        document.getElementById('avgValue').textContent = Math.round((totalD1 + totalD2 + totalD3) / (dataD1.labels.length + dataD2.labels.length + dataD3.labels.length));
    }
    window.addEventListener('load', updateComparison);
});