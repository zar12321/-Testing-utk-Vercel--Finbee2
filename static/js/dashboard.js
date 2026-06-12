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
                
                // ========================
                // Financial Health 
                // ========================
                document.getElementById(
                    "health-status"
                ).innerText =
                    data.financial_health.icon +
                    " " +
                    data.financial_health.status;

                document.getElementById(
                    "health-saving-rate"
                ).innerText =
                    "Saving Rate: " +
                    Number(
                        data.financial_health.saving_rate
                    ).toFixed(2) +
                    "%";

                document.getElementById(
                    "health-expense-ratio"
                ).innerText =
                    "Expense Ratio: " +
                    Number(
                        data.financial_health.expense_ratio
                    ).toFixed(2) +
                    "%";

                document.getElementById(
                    "health-message"
                ).innerText =
                    data.financial_health.message;

                // ========================
                // Monthly Snapshot
                // ========================
                const snapshot =
                    data.monthly_snapshot;

                let snapshotHtml = "";

                if (snapshot.title) {

                    snapshotHtml = `
                        <div class="snapshot-empty">

                            <h4>
                                📊 ${snapshot.title}
                            </h4>

                            <p>
                                ${snapshot.message}
                            </p>

                        </div>
                    `;
                }
                else {

                    if (snapshot.top_income) {

                        snapshotHtml += `
                            <div class="snapshot-item">

                                <strong>
                                    Income Terbesar
                                </strong>

                                <p>
                                    ${snapshot.top_income.category}
                                </p>

                                <span>
                                    Rp ${Number(
                                        snapshot.top_income.amount
                                    ).toLocaleString()}
                                </span>

                            </div>
                        `;
                    }

                    if (snapshot.top_expense) {

                        snapshotHtml += `
                            <div class="snapshot-item">

                                <strong>
                                    Expense Terbesar
                                </strong>

                                <p>
                                    ${snapshot.top_expense.category}
                                </p>

                                <span>
                                    Rp ${Number(
                                        snapshot.top_expense.amount
                                    ).toLocaleString()}
                                </span>

                            </div>
                        `;
                    }

                    if (snapshot.top_topup) {

                        snapshotHtml += `
                            <div class="snapshot-item">

                                <strong>
                                    Topup Terbesar
                                </strong>

                                <p>
                                    ${snapshot.top_topup.tujuan_transaksi}
                                </p>

                                <span>
                                    Rp ${Number(
                                        snapshot.top_topup.amount
                                    ).toLocaleString()}
                                </span>

                            </div>
                        `;
                    }
                }

                document.getElementById(
                    "snapshot-content"
                ).innerHTML =
                    snapshotHtml;

                // ========================
                // Spending Alert
                // ========================
                let alertHtml = "";

                data.spending_alert.forEach(
                    (alert) => {

                        alertHtml += `
                            <div class="alert-item ${alert.status}">

                                <h4>
                                    ${alert.icon}
                                    ${alert.title}
                                </h4>

                                <p>
                                    ${alert.message}
                                </p>

                            </div>
                        `;
                    }
                );

                document.getElementById(
                    "spending-alert-container"
                ).innerHTML =
                    alertHtml;
            }
        );
    }
);