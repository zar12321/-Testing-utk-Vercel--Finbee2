Chart.register(
    ChartDataLabels
);

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await loadFilterOptions();

        await loadAnalytics();

        document
            .getElementById(
                "apply-filter-btn"
            )
            ?.addEventListener(
                "click",
                applyFilters
            );

        document
            .getElementById(
                "reset-filter-btn"
            )
            ?.addEventListener(
                "click",
                resetFilters
            );

    }
);

let cashflowChart = null;
let breakdownChart = null;

let breakdownPreviewData = {};


// ======================================
// LOAD FILTER OPTIONS
// ======================================

async function loadFilterOptions() {

    try {

        const response =
            await fetch(
                "/transactions/filter-options"
            );

        const data =
            await response.json();
        
        breakdownPreviewData = 
            data.breakdown_preview || {};

        const yearSelect =
            document.getElementById(
                "filter-year"
            );

        const subcategorySelect =
            document.getElementById(
                "filter-subcategory"
            );

        // =====================
        // YEAR
        // =====================

        if (
            yearSelect &&
            data.years
        ) {

            data.years.forEach(
                year => {

                    yearSelect.innerHTML += `
                        <option value="${year}">
                            ${year}
                        </option>
                    `;

                }
            );

        }

        // =====================
        // SUBCATEGORY
        // =====================

        if (
            subcategorySelect &&
            data.subcategories
        ) {

            data.subcategories.forEach(
                sub => {

                    subcategorySelect.innerHTML += `
                        <option value="${sub.category_id}">
                            ${sub.category_name}
                        </option>
                    `;

                }
            );

        }

    }

    catch(error){

        console.error(
            "Load Filter Error:",
            error
        );

    }

}


// ======================================
// BUILD QUERY PARAMS
// ======================================

function buildParams() {

    const params =
        new URLSearchParams();

    const month =
        document.getElementById(
            "filter-month"
        )?.value;

    const year =
        document.getElementById(
            "filter-year"
        )?.value;

    const period =
        document.getElementById(
            "filter-period"
        )?.value;

    const category =
        document.getElementById(
            "filter-category"
        )?.value;

    const subcategory =
        document.getElementById(
            "filter-subcategory"
        )?.value;

    if(month)
        params.append(
            "month",
            month
        );

    if(year)
        params.append(
            "year",
            year
        );

    if(period)
        params.append(
            "period",
            period
        );

    if(category)
        params.append(
            "category",
            category
        );

    if(subcategory)
        params.append(
            "subcategory_id",
            subcategory
        );

    return params;

}


// ======================================
// APPLY FILTER
// ======================================

async function applyFilters() {

    const params =
        buildParams();

    await loadAnalytics(
        params.toString()
    );

}


// ======================================
// RESET FILTER
// ======================================

async function resetFilters() {

    document.getElementById(
        "filter-month"
    ).value = "";

    document.getElementById(
        "filter-year"
    ).value = "";

    document.getElementById(
        "filter-period"
    ).value = "";

    document.getElementById(
        "filter-category"
    ).value = "";

    document.getElementById(
        "filter-subcategory"
    ).value = "";

    await loadAnalytics();

}


// ======================================
// LOAD ANALYTICS DATA
// ======================================

async function loadAnalytics(
    queryString = ""
) {

    try {

        const response =
            await fetch(
                `/analytics/chart-data?${queryString}`
            );

        const data =
            await response.json();

        console.log(
            "Analytics Data:",
            data
        );

        renderCashflowChart(
            data.cashflow_trend
        );

        renderBreakdownChart(
            data.breakdown_chart
        );

        breakdownPreviewData = 
            data.breakdown_preview || {};

        console.log(
            "Preview Data", 
            breakdownPreviewData
        )

    }

    catch(error){

        console.error(
            "Analytics Error:",
            error
        );

    }

}


// ======================================
// CASHFLOW TREND CHART
// ======================================

function renderCashflowChart(
    chartData
){

    const canvas =
        document.getElementById(
            "cashflow-chart"
        );

    if(
        !canvas
    ) return;

    if(
        cashflowChart
    ){
        cashflowChart.destroy();
    }

    cashflowChart =
        new Chart(
            canvas,
            {
                type: "line",

                data: {

                    labels:
                        chartData.map(
                            item => item.date
                        ),

                    datasets: [

                        {
                            label: "Pemasukan",

                            data:
                                chartData.map(
                                    item => item.income
                                ),

                            tension: 0.4
                        },

                        {
                            label: "Pengeluaran",

                            data:
                                chartData.map(
                                    item => item.expense
                                ),

                            tension: 0.4
                        },

                        {
                            label: "Topup",

                            data:
                                chartData.map(
                                    item => item.topup
                                ),

                            tension: 0.4
                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        datalabels: false,

                        legend: {

                            labels: {

                                color: "#787878",

                                font: {
                                    size: 12,
                                    family:"Arial"
                                }

                            }

                        }

                    },

                    scales: {

                        x: {

                            ticks: {

                                color: "#626161",

                                font: {
                                    size: 12,
                                    weight: "600", 
                                    family:"inherit"
                                }

                            }

                        },

                        y: {

                            ticks: {

                                color: "#494848",

                                font: {
                                    size: 12,
                                    weight: "600", 
                                    family:"inherit"
                                }

                            }

                        }

                    }

                }

            }
        );

}



// ======================================
// BREAKDOWN CHART
// ======================================

function renderBreakdownChart(
    chartData
){

    const canvas =
        document.getElementById(
            "breakdown-chart"
        );

    if(
        !canvas
    ) return;

    if(
        breakdownChart
    ){
        breakdownChart.destroy();
    }

    breakdownChart =
        new Chart(
            canvas,
            {
                type: "bar",

                data: {

                    labels:
                        chartData.map(
                            item => item.label
                        ),

                    datasets: [
                        {
                            label: "Total",

                            data:
                                chartData.map(
                                    item => item.total
                                ), 
                            borderRadius: 8
                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        datalabels: {

                            formatter: value =>
                                "Rp " +
                                Number(value)
                                .toLocaleString("id-ID"),

                            anchor: context => {

                                const value =
                                    context.dataset.data[
                                        context.dataIndex
                                    ];

                                const maxValue =
                                    Math.max(
                                        ...context.dataset.data
                                    );

                                return value >
                                    maxValue * 0.75
                                    ? "center"
                                    : "end";

                            },

                            align: context => {

                                const value =
                                    context.dataset.data[
                                        context.dataIndex
                                    ];

                                const maxValue =
                                    Math.max(
                                        ...context.dataset.data
                                    );

                                return value >
                                    maxValue * 0.75
                                    ? "center"
                                    : "top";

                            },

                            color: context => {

                                const value =
                                    context.dataset.data[
                                        context.dataIndex
                                    ];

                                const maxValue =
                                    Math.max(
                                        ...context.dataset.data
                                    );

                                return value >
                                    maxValue * 0.75
                                    ? "#151515"
                                    : "#161616";

                            },

                            font: {
                                weight: "bold",
                                size: 11, 
                                family: "inherit"
                            }

                        }

                    }, 

                    scales: {
                        x: {
                            ticks:{
                                color:"#626161", 
                                font: {
                                    size:12, 
                                    family:"inherit"
                                }
                            }
                        }, 
                        y: {
                            ticks:{
                                color:"#494848", 
                                font:{
                                    size:12, 
                                    family:"inherit"
                                }
                            }
                        }
                    }

                }

            }
        );

}