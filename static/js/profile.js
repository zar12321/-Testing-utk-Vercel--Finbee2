document.addEventListener(
    "DOMContentLoaded",
    () => {

        const profileMenu =
            document.querySelector(
                ".profile-menu"
            );

        const dropdown =
            document.querySelector(
                ".profile-dropdown"
            );

        const resetBtn =
            document.getElementById(
                "reset-data-btn"
            );

        const modal =
            document.getElementById(
                "reset-modal"
            );

        const cancelBtn =
            document.getElementById(
                "cancel-reset"
            );

        const confirmBtn =
            document.getElementById(
                "confirm-reset"
            );

        // paksa hidden saat load

        dropdown.classList.remove(
            "show"
        );

        modal.classList.remove(
            "show"
        );

        profileMenu?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                dropdown.classList.toggle(
                    "show"
                );
            }
        );

        document.addEventListener(
            "click",
            () => {

                dropdown.classList.remove(
                    "show"
                );
            }
        );

        resetBtn?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                dropdown.classList.remove(
                    "show"
                );

                modal.classList.add(
                    "show"
                );
            }
        );

        cancelBtn?.addEventListener(
            "click",
            () => {

                modal.classList.remove(
                    "show"
                );
            }
        );

        modal?.addEventListener(
            "click",
            (e) => {

                if(
                    e.target === modal
                ){

                    modal.classList.remove(
                        "show"
                    );
                }
            }
        );

       window.showToast = function(
            message,
            isError = false
        ){

            const toast =
                document.getElementById(
                    "success-toast"
                );

            const text =
                document.getElementById(
                    "toast-message"
                );

            if(!toast || !text){
                return;
            }

            text.textContent =
                message;

            toast.classList.remove(
                "error"
            );

            if(isError){

                toast.classList.add(
                    "error"
                );
            }

            toast.classList.add(
                "show"
            );

            setTimeout(
                () => {

                    toast.classList.remove(
                        "show"
                    );

                },
                3000
            );
        };

        confirmBtn?.addEventListener(
            "click",
            async () => {

                try {

                    const response =
                        await fetch(
                            "/transactions/reset",
                            {
                                method: "DELETE"
                            }
                        );

                    const result =
                        await response.json();

                    if (!response.ok) {

                        throw new Error(
                            result.message ||
                            "Gagal menghapus data."
                        );
                    }

                    modal.classList.remove(
                        "show"
                    );

                    // refresh transaksi
                    if (
                        typeof loadTransactions ===
                        "function"
                    ){
                        await loadTransactions();
                    }

                    // refresh dashboard
                    if (
                        typeof window.reloadDashboardData ===
                        "function"
                    ){
                        await window.reloadDashboardData();
                    }

                    showToast(
                        result.message
                    );

                }
                catch(error){

                    showToast(
                        error.message,
                        true
                    );
                }

            }
        );

    }
);