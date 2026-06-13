document.addEventListener(
    "DOMContentLoaded",
    () => {

        const inputFile =
            document.getElementById("import-file");

        const importModal =
            document.getElementById("import-modal");

        const closeModal =
            document.getElementById("close-modal");

        const metadataPreview =
            document.getElementById("metadata-preview");

        const rawPreview =
            document.getElementById("raw-preview");

        const cleanPreview =
            document.getElementById("clean-preview");

        const importSummary =
            document.getElementById("import-summary");

        // =====================
        // FUNCTION CLOSE MODAL
        // =====================

        function closeImportModal() {

            importModal.classList.add(
                "closing"
            );

            setTimeout(() => {

                importModal.classList.remove(
                    "show",
                    "closing"
                );

            }, 300);

        }

        // =====================
        // FILE DIPILIH
        // =====================

        inputFile?.addEventListener(
            "change",
            async () => {

                const file = inputFile.files[0];

                if (!file) return;

                importModal.classList.add("show");

                // =====================
                // METADATA
                // =====================

                metadataPreview.innerHTML = `
                    <div style="display:grid;gap:12px;">

                        <div>
                            <strong>Nama File</strong><br>
                            ${file.name}
                        </div>

                        <div>
                            <strong>Ukuran</strong><br>
                            ${(file.size / 1024).toFixed(2)} KB
                        </div>

                        <div>
                            <strong>Tipe</strong><br>
                            ${file.type || "-"}
                        </div>

                    </div>
                `;

                // =====================
                // BACA FILE (CSV / XLSX)
                // =====================

                const reader = new FileReader();

                reader.onload = async function (e) {

                    const data = new Uint8Array(e.target.result);

                    const workbook = XLSX.read(data, {
                        type: "array"
                    });

                    const sheetName =
                        workbook.SheetNames[0];

                    const sheet =
                        workbook.Sheets[sheetName];

                    const json = XLSX.utils.sheet_to_json(
                        sheet,
                        {
                            header: 1,
                            raw: false,
                            dateNF: "dd/mm/yyyy"
                        }
                    );
                    // ambil 10 baris pertama
                    const previewData =
                        json.slice(0, 10);

                    // =====================
                    // RENDER TABLE
                    // =====================

                    const headers = previewData[0] || [];

                    let html = `
                    <div
                        style="
                            overflow-x:auto;
                            border-radius:16px;
                        "
                    >
                        <table
                            style="
                                width:100%;
                                border-collapse:collapse;
                                white-space:nowrap;
                                font-size:14px;
                            "
                        >
                    `;

                    previewData.forEach((row, i) => {

                        html += "<tr>";

                        for (
                            let j = 0;
                            j < headers.length;
                            j++
                        ) {

                            const cell =
                                row[j] ?? "";

                            if (i === 0) {

                                html += `
                                    <th
                                        style="
                                            padding:14px 16px;
                                            text-align:left;
                                            font-weight:600;
                                            color:#121314;
                                            border-bottom:1px solid #e2e8f0;
                                            background:transparent;
                                        "
                                    >
                                        ${cell}
                                    </th>
                                `;

                            } else {

                                html += `
                                    <td
                                        style="
                                            padding:14px 16px;
                                            border-bottom:1px solid #f1f5f9;
                                            color:#334155;
                                        "
                                    >
                                        ${cell}
                                    </td>
                                `;

                            }

                        }

                        html += "</tr>";

                    });

                    html += `
                        </table>
                    </div>
                    `;

                    rawPreview.innerHTML = html;
                    // =====================
                    // CLEANING 
                    // =====================
                    rawPreview.innerHTML = html;

                    try {

                        const formData =
                            new FormData();

                        formData.append(
                            "file",
                            file
                        );

                        const response =
                            await fetch(
                                "/transactions/import-preview",
                                {
                                    method: "POST",
                                    body: formData
                                }
                            );

                        const result =
                            await response.json();

                        console.log(
                            "IMPORT PREVIEW",
                            result
                        );

                        const cleanData =
                            result.clean_preview || [];

                        if (!cleanData.length) {

                            cleanPreview.innerHTML =
                                "<p>Tidak ada data hasil cleaning.</p>";

                        } else {
                            const columnAliases = {
                                tanggal_transaksi:
                                    "Tanggal",

                                raw_category:
                                    "Kategori",

                                category_name:
                                    "Subkategori",

                                transaction_type:
                                    "Tipe Transaksi",

                                tujuan_transaksi:
                                    "Tujuan Transaksi",

                                keterangan:
                                    "Keterangan",

                                payment_method:
                                    "Metode Pembayaran",

                                amount:
                                    "Nominal"
                            };

                            const headers =
                                Object.keys(cleanData[0]).
                                    filter(
                                        header =>
                                            header != 'transaction_type'
                                    )
                                ;

                            let cleanHtml = `
                                <div
                                    style="
                                        overflow-x:auto;
                                        border-radius:16px;
                                    "
                                >
                                    <table
                                        style="
                                            width:100%;
                                            border-collapse:collapse;
                                            white-space:nowrap;
                                            font-size:14px;
                                        "
                                    >
                            `;

                            cleanHtml += "<tr>";

                            headers.forEach(header => {

                                cleanHtml += `
                                    <th
                                        style="
                                            padding:14px 16px;
                                            text-align:left;
                                            font-weight:600;
                                            color:#121314;
                                            border-bottom:1px solid #e2e8f0;
                                        "
                                    >
                                        ${columnAliases[header] || header}
                                    </th>
                                `;

                            });

                            cleanHtml += "</tr>";

                            cleanData.forEach(row => {

                                cleanHtml += "<tr>";

                                headers.forEach(header => {

                                    cleanHtml += `
                                        <td
                                            style="
                                                padding:14px 16px;
                                                border-bottom:1px solid #f1f5f9;
                                                color:#334155;
                                            "
                                        >
                                                                      ${
                                        header === "amount"
                                            ? Number(
                                                row[header]
                                            ).toLocaleString(
                                                "id-ID",
                                                {
                                                    style: "currency",
                                                    currency: "IDR",
                                                    minimumFractionDigits: 0
                                                }
                                            )
                                            : (row[header] ?? "")
                                    }
                                        </td>
                                    `;

                                });

                                cleanHtml += "</tr>";

                            });

                            cleanHtml += `
                                    </table>
                                </div>
                            `;

                            cleanPreview.innerHTML =
                                cleanHtml;
                        }

                        importSummary.innerHTML = `
                            <div style="display:grid;gap:8px;">
                                <div>
                                    Total Raw:
                                    ${result.summary.total_raw_rows}
                                </div>

                                <div>
                                    Total Clean:
                                    ${result.summary.total_clean_rows}
                                </div>

                                <div>
                                    Removed:
                                    ${result.summary.removed_rows}
                                </div>
                            </div>
                        `;

                    } catch (error) {

                        console.error(error);

                        cleanPreview.innerHTML = `
                            <p>
                                Gagal memuat preview cleaning.
                            </p>
                        `;

                    }
                }

                reader.readAsArrayBuffer(file);
            }
        );

        // =====================
        // CLOSE MODAL (TOMBOL X)
        // =====================

        closeModal?.addEventListener(
            "click",
            (e) => {

                e.preventDefault();
                e.stopPropagation();

                closeImportModal();

            }
        );

        // =====================
        // CLOSE SAAT KLIK BACKDROP
        // =====================

        importModal?.addEventListener(
            "click",
            (e) => {

                if (e.target === importModal) {

                    closeImportModal();

                }

            }
        );

        // =====================
        // FILTER TRANSAKSI
        // =====================
        loadTransactions();
        loadFilterOptions();

        document
            .getElementById(
                "apply-filter-btn"
            )
            ?.addEventListener(
                "click",
                applyFilters
            );

    }   
);

async function loadFilterOptions() {

    const response =
        await fetch(
            "/transactions/filter-options"
        );

    const data =
        await response.json();

    const paymentSelect =
        document.getElementById(
            "filter-payment"
        );
    
    const categorySelect =
        document.getElementById(
            "filter-category"
        );

    const subcategorySelect =
        document.getElementById(
            "filter-subcategory"
        );
    
    const monthSelect = 
        document.getElementById(
            "filter-month"
        );
    
    const yearSelect = 
        document.getElementById(
            "filter-year"
        );

    data.payment_methods.forEach(
        method => {

            paymentSelect.innerHTML += `
                <option value="${method}">
                    ${method}
                </option>
            `;
        }
    );

    const categoryAlias = {

        expense: "Pengeluaran",

        income: "Pemasukan",

        topup: "Topup"

    };

    data.categories.forEach(
        category => {

            categorySelect.innerHTML += `
                <option value="${category}">
                    ${categoryAlias[category] || category}
                </option>
            `;

        }
    );

    data.subcategories.forEach(
        category => {

            subcategorySelect.innerHTML += `
                <option value="${category.category_id}">
                    ${category.category_name}
                </option>
            `;
        }
    );

    data.month.forEach(
        month => {
            monthSelect.innerHTML += `
                <option value="${month}">
                    ${month}
                </option>
            `
        }
    );

    data.years.forEach(
        year => {
            yearSelect.innerHTML += `
                <option value="${year}">
                    ${year}
                </option>
            `
        }
    );

}

async function applyFilters() {

    const params = new URLSearchParams();

    const period =
        document.getElementById(
            "filter-period"
        ).value;

    const month =
        document.getElementById(
            "filter-month"
        ).value;

    const year =
        document.getElementById(
            "filter-year"
        ).value;

    const category =
        document.getElementById(
            "filter-category"
        ).value;

    const subcategoryId =
        document.getElementById(
            "filter-subcategory"
        ).value;

    if (period)
        params.append("period", period);

    if (month)
        params.append("month", month);

    if (year)
        params.append("year", year);

    if (category)
        params.append("category", category);

    if (subcategoryId)
        params.append(
            "subcategory_id",
            subcategoryId
        );

    console.log(
        `/transactions/filter?${params}`
    );

    const response =
        await fetch(
            `/transactions/filter?${params}`
        );

    const transactions =
        await response.json();

    renderTransactionTable(
        transactions
    );

}

function renderTransactionTable(
    transactions
) {

    const tableBody =
        document.getElementById(
            "transaction-table-body"
        );

    tableBody.innerHTML = "";

    if (!transactions.length) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="8">
                    Tidak ada transaksi ditemukan
                </td>
            </tr>
        `;

        return;
    }

    transactions.forEach(
        transaction => {

            tableBody.innerHTML += `
                <tr>

                    <td>
                        ${
                            new Date(
                                transaction.tanggal_transaksi
                            )
                            .toLocaleDateString(
                                "id-ID"
                            )
                        }
                    </td>

                    <td>
                        ${transaction.raw_category || "-"}
                    </td>

                    <td>
                        ${transaction.category_name || "-"}
                    </td>

                    <td>
                        ${transaction.tujuan_transaksi || "-"}
                    </td>

                    <td>
                        ${transaction.payment_method || "-"}
                    </td>

                    <td>
                        ${Number(
                            transaction.amount
                        ).toLocaleString(
                            "id-ID",
                            {
                                style: "currency",
                                currency: "IDR",
                                minimumFractionDigits: 0
                            }
                        )}
                    </td>

                    <td>
                        ${transaction.keterangan || "-"}
                    </td>

                    <td>

                        <button
                            class="delete-btn"
                            data-id="${transaction.transaction_id}"
                        >
                            Hapus
                        </button>

                    </td>

                </tr>
            `;
        }
    );
}

async function loadTransactions() {

    const response =
        await fetch(
            "/transactions/filter"
        );

    const transactions =
        await response.json();

    renderTransactionTable(
        transactions
    );
}