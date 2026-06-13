document.addEventListener(
    "DOMContentLoaded",
    () => {

        const inputFile =
            document.getElementById(
                "import-file"
            );

        const importModal =
            document.getElementById(
                "import-modal"
            );

        const closeModal =
            document.getElementById(
                "close-modal"
            );

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

                    const json =
                        XLSX.utils.sheet_to_json(sheet, {
                            header: 1
                        });

                    // ambil 10 baris pertama
                    const previewData =
                        json.slice(0, 10);

                    // =====================
                    // RENDER TABLE
                    // =====================

                    let html = `<table border="1" style="width:100%;border-collapse:collapse;">`;

                    previewData.forEach((row, i) => {

                        html += "<tr>";

                        row.forEach(cell => {

                            if (i === 0) {
                                html += `<th style="padding:6px;background:#eee;">${cell ?? ""}</th>`;
                            } else {
                                html += `<td style="padding:6px;">${cell ?? ""}</td>`;
                            }

                        });

                        html += "</tr>";

                    });

                    html += "</table>";

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