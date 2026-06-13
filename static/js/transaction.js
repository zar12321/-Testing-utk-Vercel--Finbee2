document.addEventListener(
    "DOMContentLoaded",
    () => {

        const inputFile =
            document.getElementById("import-file");

        const importModal =
            document.getElementById("import-modal");

        const closeModal =
            document.getElementById("close-modal");

        // ❗ INI YANG KAMU LUPA
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
            () => {

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

                reader.onload = function (e) {

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
                    // CLEANING (placeholder dulu)
                    // =====================

                    cleanPreview.innerHTML =
                        "<p>Belum ada proses cleaning (next step).</p>";

                    importSummary.innerHTML =
                        `<p>Total row: ${json.length}</p>`;

                };

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

    }   
);