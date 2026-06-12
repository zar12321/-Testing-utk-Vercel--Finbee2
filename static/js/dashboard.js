document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log("JS LOADED");

        const form =
            document.getElementById(
                "dashboard-filter-form"
            );

        if (!form) return;

        form.addEventListener(
            "submit",
            async (e) => {

                console.log("TOMBOL DIKLIK");

                e.preventDefault();

                const month =
                    document.getElementById(
                        "filter-month"
                    ).value;

                const year =
                    document.getElementById(
                        "filter-year"
                    ).value;

                const response =
                    await fetch(
                        `/dashboard/data?month=${month}&year=${year}`
                    );

                console.log(
                    "STATUS:",
                    response.status
                );

                const data =
                    await response.json();

                console.log(data);

                // ========================
                // UPDATE METRICS
                // ========================

                document.querySelector(
                    "#metric-balance .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.balance
                    ).toLocaleString();

                document.querySelector(
                    "#metric-total-income .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.total_income
                    ).toLocaleString();

                document.querySelector(
                    "#metric-total-expense .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.total_expense
                    ).toLocaleString();

                document.querySelector(
                    "#metric-total-topup .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.total_topup
                    ).toLocaleString();

                document.querySelector(
                    "#metric-total-transaction .metric-value"
                ).innerText =
                    Number(
                        data.metrics.total_transaction
                    ).toLocaleString();

                document.querySelector(
                    "#metric-avg-transaction .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.avg_transaction
                    ).toLocaleString();

                document.querySelector(
                    "#metric-avg-daily .metric-value"
                ).innerText =
                    "Rp " +
                    Number(
                        data.metrics.avg_daily
                    ).toLocaleString();

                document.querySelector(
                    "#metric-saving-rate .metric-value"
                ).innerText =
                    Number(
                        data.metrics.saving_rate
                    ).toFixed(2) + "%";
            }
        );
    }
);