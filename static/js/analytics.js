Chart.register(
    ChartDataLabels
);

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await loadFilterOptions();

        await loadAnalytics();

        await loadPrediction();

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

        document
            .getElementById(
                "apply-prediction-btn"
            )
            ?.addEventListener(
                "click",
                loadPrediction
            );

        document
            .getElementById(
                "reset-prediction-btn"
            )
            ?.addEventListener(
                "click",
                resetPredictionFilters
            );
    }
);

let cashflowChart = null;
let breakdownChart = null;
let paymentBarChart = null;
let paymentDoughnutChart = null;
let predictionChart = null;

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

        const predictionSubCategorySelect = 
            document.getElementById(
                "prediction-subcategory"
            )
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
        if(data.subcategories){

            data.subcategories.forEach(
                sub => {

                    const option = `
                        <option value="${sub.category_id}">
                            ${sub.category_name}
                        </option>
                    `;

                    if(subcategorySelect){
                        subcategorySelect.innerHTML += option;
                    }

                    if(predictionSubCategorySelect){
                        predictionSubCategorySelect.innerHTML += option;
                    }

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

        console.log(
            "Cashflow:",
            data.cashflow_trend
        );

        console.log(
            "Breakdown:",
            data.breakdown_chart
        );

        console.log(
            "Payment:",
            data.payment_method_chart
        );
        renderCashflowChart(
            data.cashflow_trend
        );

        renderBreakdownChart(
            data.breakdown_chart
        );

        renderPaymentDoughnutChart (
            data.payment_method_chart
        );

        renderPaymentBarChart (
            data.payment_method_chart
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
// LOAD PREDICTION
// ======================================

async function loadPrediction(){

    try{

        const days =
            document.getElementById(
                "prediction-days"
            )?.value || "7";

        const subcategory =
            document.getElementById(
                "prediction-subcategory"
            )?.value;

        const params =
            new URLSearchParams();

        params.append(
            "days",
            days
        );

        if(subcategory){

            params.append(
                "category_id",
                subcategory
            );

        }

        const response =
            await fetch(
                `/analytics/prediction?${params}`
            );

        const result =
            await response.json();

        console.log(
            "Prediction:",
            result
        );

        if(
            result.success &&
            result.data &&
            result.data.history?.length
        ){

            toggleEmptyState(
                "prediction-chart",
                "prediction-empty",
                true
            );

            renderPredictionChart(
                result.data
            );

        }
        else{

            if(predictionChart){

                predictionChart.destroy();

                predictionChart = null;
            }

            toggleEmptyState(
                "prediction-chart",
                "prediction-empty",
                false
            );

        }

    }

    catch(error){

        console.error(
            "Prediction Error:",
            error
        );

        if(predictionChart){

            predictionChart.destroy();

            predictionChart = null;
        }

        toggleEmptyState(
            "prediction-chart",
            "prediction-empty",
            false
        );

    }

}

// ======================================
// RESET PREDICTION FILTER
// ======================================

async function resetPredictionFilters(){

    document.getElementById(
        "prediction-days"
    ).value = "7";

    document.getElementById(
        "prediction-subcategory"
    ).value = "";

    await loadPrediction();

}

// ======================================
// CASHFLOW TREND CHART
// ======================================

function renderCashflowChart(chartData){

    const canvas =
        document.getElementById(
            "cashflow-chart"
        );

    if(!canvas) return;

    if(cashflowChart){
        cashflowChart.destroy();
        cashflowChart = null;
    }

    if(
        !chartData ||
        chartData.length === 0
    ){

        toggleEmptyState(
            "cashflow-chart",
            "cashflow-empty",
            false
        );

        if(cashflowChart){

            cashflowChart.destroy();

            cashflowChart = null;
        }

        return;
    }

    toggleEmptyState(
        "cashflow-chart",
        "cashflow-empty",
        true
    );

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

                    animation: false,

                    animation: {
                        duration: 100
                    },

                    animations: {
                        x: {
                            type: 'number',
                            easing: 'linear',
                            duration: 0,
                            from: NaN,
                            delay(ctx) {

                                if(
                                    ctx.type !== 'data' ||
                                    ctx.xStarted
                                ){
                                    return 0;
                                }

                                ctx.xStarted = true;

                                return ctx.index * 40;
                            }
                        },

                        y: {
                            type: 'number',
                            easing: 'linear',
                            duration: 0,
                            from(ctx){

                                if(
                                    ctx.index === 0
                                ){
                                    return ctx.chart.scales.y.getPixelForValue(0);
                                }

                                return ctx.chart
                                    .getDatasetMeta(
                                        ctx.datasetIndex
                                    )
                                    .data[
                                        ctx.index - 1
                                    ]
                                    .getProps(
                                        ['y'],
                                        true
                                    ).y;
                            }
                        }
                    },

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
    
    if(
    !chartData ||
    chartData.length === 0
    ){

        toggleEmptyState(
            "breakdown-chart",
            "breakdown-empty",
            false
        );

        if(breakdownChart){

            breakdownChart.destroy();

            breakdownChart = null;
        }

        return;
    }

    toggleEmptyState(
        "breakdown-chart",
        "breakdown-empty",
        true
    );
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
                            label: "Nominal",

                            data:
                                chartData.map(
                                    item => item.total
                                ), 
                            borderRadius: 8
                        }
                    ]

                },

                options: {
                    animation:{
                        y:{

                            from: 0
                        }
                    },

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
                                    ? "#000000"
                                    : "#161616";

                            },

                            font: {
                                weight: "600",
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

// ======================================
// DOUGHNUT CHART
// ======================================
function renderPaymentDoughnutChart(
    chartData
){

    const canvas =
        document.getElementById(
            "payment-doughnut-chart"
        );

    if(!canvas) return;

    if(paymentDoughnutChart){
        paymentDoughnutChart.destroy();
    }

    if(
    !chartData ||
    chartData.length === 0
    ){

        toggleEmptyState(
            "payment-doughnut-chart",
            "payment-doughnut-empty",
            false
        );

        if(paymentDoughnutChart){

            paymentDoughnutChart.destroy();

            paymentDoughnutChart = null;
        }

        return;
    }

    toggleEmptyState(
        "payment-doughnut-chart",
        "payment-doughnut-empty",
        true
    );

    paymentDoughnutChart =
        new Chart(
            canvas,
            {
                type:"doughnut",

                data:{
                    labels:
                        chartData.map(
                            item => item.label
                        ),

                    datasets:[
                        {
                            data:
                                chartData.map(
                                    item => item.total
                                )
                        }
                    ]
                },

                options:{
                    responsive:true,

                    maintainAspectRatio:false,
                    animation:{
                        duration: 2000, 
                        easing: "easeOutQuart"
                    },

                    plugins:{

                        legend:{
                            position:"top"
                        },


                        datalabels:{

                            display:(context)=>{

                                const value =
                                    context.dataset.data[
                                        context.dataIndex
                                    ];

                                const total =
                                    context.dataset.data.reduce(
                                        (a,b)=>a+b,
                                        0
                                    );

                                const percent =
                                    (value / total) * 100;

                                return percent >= 5;
                            },

                            color: "#000000", 
                            font: {
                                weight:"600", 
                                size:11
                            },

                            formatter:(value, context)=>{

                                const total =
                                    context.dataset.data
                                    .reduce(
                                        (a,b)=>a+b,
                                        0
                                    );

                                const percent =
                                    (
                                        value / total
                                    ) * 100;

                                return percent.toFixed(1) + "%";
                            }

                        }, 

                        layout:{
                            padding:{
                                top:10,
                                right:20,
                                left:20,
                                bottom:10
                            }
                        }
                    }
                }
            }
        );


}

// ======================================
// HORIZONTAL BAR CHART
// ======================================
function renderPaymentBarChart(
    chartData
){

    const canvas =
        document.getElementById(
            "payment-bar-chart"
        );

    if(!canvas) return;

    if(paymentBarChart){
        paymentBarChart.destroy();
    }

    if(
    !chartData ||
    chartData.length === 0
    ){

        toggleEmptyState(
            "payment-bar-chart",
            "payment-bar-empty",
            false
        );

        if(paymentBarChart){

            paymentBarChart.destroy();

            paymentBarChart = null;
        }

        return;
    }

    toggleEmptyState(
        "payment-bar-chart",
        "payment-bar-empty",
        true
    );

    paymentBarChart =
        new Chart(
            canvas,
            {
                type:"bar",

                data:{

                    labels:
                        chartData.map(
                            item => item.label
                        ),

                    datasets:[
                        {
                            label:"Nominal",

                            data:
                                chartData.map(
                                    item => item.total
                                ),

                            borderRadius:10
                        }
                    ]
                },

                options:{

                    indexAxis:"y",

                    responsive:true,

                    maintainAspectRatio:false,

                    animation:{
                        duration: 2000, 
                        easing: "easeOutQuart"
                    },

                    plugins:{

                        datalabels:{

                            formatter:(value)=>{

                                return (
                                    "Rp " +
                                    Number(value)
                                    .toLocaleString(
                                        "id-ID"
                                    )
                                );

                            },

                            anchor:(context)=>{

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

                            align:(context)=>{

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
                                    : "right";
                            },

                            color:(context)=>{

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
                                    ? "#000000"
                                    : "#374151";
                            },

                            font:{
                                size:11,
                                weight:"600"
                            }
                        }, 
                        layout:{
                            padding:{
                                right:50
                            }
                        }

                    }

                }

            }
        );

}

// ======================================
// PREDICTION CHART
// ======================================

function renderPredictionChart(
    data
){

    const canvas =
        document.getElementById(
            "prediction-chart"
        );

    if(!canvas) return;

    if(predictionChart){

        predictionChart.destroy();

    }

    const history =
        data.history || [];

    const forecast =
        data.predictions || [];

    const labels = [

        ...history.map(
            x => x.date
        ),

        ...forecast.map(
            x => x.date
        )

    ];

    const historicalData = [

        ...history.map(
            x => x.amount
        ),

        ...Array(
            forecast.length
        ).fill(null)

    ];

    const forecastData = [

        ...Array(
            history.length - 1
        ).fill(null),

        history.length
            ? history[
                history.length - 1
              ].amount
            : null,

        ...forecast.map(
            x =>
                x.predicted_amount
        )

    ];

    predictionChart =
        new Chart(
            canvas,
            {
                type:"line",

                data:{

                    labels,

                    datasets:[

                        {
                            label:
                                "Histori Pengeluaran",

                            data:
                                historicalData,

                            tension:0.4
                        },

                        {
                            label:
                                "Prediksi",

                            data:
                                forecastData,

                            tension:0.4,

                            borderDash:[
                                8,
                                8
                            ]
                        }

                    ]

                },

                options:{

                    responsive:true,

                    maintainAspectRatio:false,

                    plugins:{

                        datalabels:false

                    },

                    scales:{

                        x:{
                            ticks:{
                                color:"#626161"
                            }
                        },

                        y:{
                            ticks:{
                                color:"#494848"
                            }
                        }

                    }

                }

            }
        );

}

function toggleEmptyState(
    chartId,
    emptyId,
    hasData
){

    const canvas =
        document.getElementById(
            chartId
        );

    const empty =
        document.getElementById(
            emptyId
        );

    if(
        !canvas ||
        !empty
    ){
        return;
    }

    if(hasData){

        canvas.style.display =
            "block";

        empty.classList.remove(
            "show"
        );

    }

    else{

        canvas.style.display =
            "none";

        empty.classList.add(
            "show"
        );

    }

}