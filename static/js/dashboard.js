async function loadDashboardData() {

    try {

        const month =
            document.getElementById(
                "filter-month"
            )?.value || "";

        const year =
            document.getElementById(
                "filter-year"
            )?.value || "";

        const response =
            await fetch(
                `/dashboard/data?month=${month}&year=${year}`
            );

        if (!response.ok) {

            throw new Error(
                "Gagal memuat dashboard"
            );

        }

        const data =
            await response.json();

        const metrics =
            data.metrics || {};

        const financialHealth =
            data.financial_health || {};

        const snapshot =
            data.monthly_snapshot || {};

        const alerts =
            data.spending_alert || [];

        // ========================
        // METRICS
        // ========================

        document.querySelector(
            "#metric-balance .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.balance || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-total-income .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.total_income || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-total-expense .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.total_expense || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-total-topup .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.total_topup || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-total-transaction .metric-value"
        ).innerText =
            Number(
                metrics.total_transaction || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-avg-transaction .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.avg_transaction || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-avg-daily .metric-value"
        ).innerText =
            "Rp " +
            Number(
                metrics.avg_daily || 0
            ).toLocaleString("id-ID");

        document.querySelector(
            "#metric-saving-rate .metric-value"
        ).innerText =
            Number(
                metrics.saving_rate || 0
            ).toFixed(2) + "%";

        // ========================
        // FINANCIAL HEALTH
        // ========================

        document.getElementById(
            "health-status"
        ).innerText =
            `${financialHealth.icon || "📊"} ${financialHealth.status || "Belum Ada Data"}`;

        document.getElementById(
            "health-saving-rate"
        ).innerText =
            `Saving Rate: ${
                Number(
                    financialHealth.saving_rate || 0
                ).toFixed(2)
            }%`;

        document.getElementById(
            "health-expense-ratio"
        ).innerText =
            `Expense Ratio: ${
                Number(
                    financialHealth.expense_ratio || 0
                ).toFixed(2)
            }%`;

        document.getElementById(
            "health-message"
        ).innerText =
            financialHealth.message ||
            "Belum ada transaksi untuk dianalisis.";

        // ========================
        // MONTHLY SNAPSHOT
        // ========================

        let snapshotHtml = "";

        if (snapshot.title) {

            snapshotHtml = `
                <div class="snapshot-empty">
                    <h4>📊 ${snapshot.title}</h4>
                    <p>${snapshot.message || ""}</p>
                </div>
            `;

        } else {

            if (snapshot.top_income) {

                snapshotHtml += `
                    <div class="snapshot-item">
                        <strong>Income Terbesar</strong>
                        <p>${snapshot.top_income.category}</p>
                        <span>
                            Rp ${Number(
                                snapshot.top_income.amount || 0
                            ).toLocaleString("id-ID")}
                        </span>
                    </div>
                `;
            }

            if (snapshot.top_expense) {

                snapshotHtml += `
                    <div class="snapshot-item">
                        <strong>Expense Terbesar</strong>
                        <p>${snapshot.top_expense.category}</p>
                        <span>
                            Rp ${Number(
                                snapshot.top_expense.amount || 0
                            ).toLocaleString("id-ID")}
                        </span>
                    </div>
                `;
            }

            if (snapshot.top_topup) {

                snapshotHtml += `
                    <div class="snapshot-item">
                        <strong>Topup Terbesar</strong>
                        <p>${snapshot.top_topup.tujuan_transaksi}</p>
                        <span>
                            Rp ${Number(
                                snapshot.top_topup.amount || 0
                            ).toLocaleString("id-ID")}
                        </span>
                    </div>
                `;
            }

            if (!snapshotHtml) {

                snapshotHtml = `
                    <div class="snapshot-empty">
                        <h4>📊 Belum Ada Data</h4>
                        <p>
                            Tambahkan transaksi untuk melihat snapshot bulanan.
                        </p>
                    </div>
                `;
            }

        }

        document.getElementById(
            "snapshot-content"
        ).innerHTML =
            snapshotHtml;

        // ========================
        // ALERT
        // ========================

        let alertHtml = "";

        alerts.forEach(alert => {

            alertHtml += `
                <div class="alert-item ${alert.status || ""}">
                    <h4>
                        ${alert.icon || "📊"}
                        ${alert.title || ""}
                    </h4>
                    <p>
                        ${alert.message || ""}
                    </p>
                </div>
            `;

        });

        if (!alertHtml) {

            alertHtml = `
                <div class="alert-item">
                    <p>
                        Belum ada alert yang tersedia.
                    </p>
                </div>
            `;
        }

        document.getElementById(
            "spending-alert-container"
        ).innerHTML =
            alertHtml;

    }

    catch (error) {

        console.error(
            "Dashboard Error:",
            error
        );

    }

}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "dashboard-filter-form"
            );

        if (form) {

            form.addEventListener(
                "submit",
                async (e) => {

                    e.preventDefault();

                    await loadDashboardData();

                }
            );

        }

        loadDashboardData();

    }
);

window.reloadDashboardData =
    loadDashboardData;