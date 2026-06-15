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
        
        const profileSettingsBtn =
            document.getElementById(
                "profile-settings-btn"
            );

        const profileSettingsModal =
            document.getElementById(
                "profile-settings-modal"
            );

        const closeProfileModal =
            document.getElementById(
                "close-profile-modal"
            );

        const uploadPhotoBtn =
            document.getElementById(
                "upload-photo-btn"
            );

        const photoInput =
            document.getElementById(
                "profile-photo-input"
            );

        const profilePreview =
            document.getElementById(
                "profile-picture-preview"
            );

        const saveProfileBtn =
            document.getElementById(
                "save-profile-btn"
            );

        const usernameInput =
            document.getElementById(
                "profile-username"
            );

        const namaInput =
            document.getElementById(
                "profile-nama"
            )?.value?.trim();


        profileSettingsBtn?.addEventListener(
            "click",
            () => {

                profileSettingsModal.classList.add(
                    "show"
                );

                dropdown.classList.remove(
                    "show"
                );

            }
        );

        closeProfileModal?.addEventListener(
            "click",
            () => {

                profileSettingsModal.classList.remove(
                    "show"
                );

            }
        );

        uploadPhotoBtn?.addEventListener(
            "click",
            () => {

                photoInput?.click();

            }
        );

        profilePreview?.addEventListener(
            "click",
            () => {

                photoInput?.click();

            }
        );

        photoInput?.addEventListener(
            "change",
            (event) => {

                const file =
                    event.target.files?.[0];

                if(!file){
                    return;
                }

                const reader =
                    new FileReader();

                reader.onload =
                    function(e){

                        profilePreview.innerHTML =
                            `
                            <img
                                src="${e.target.result}"
                                alt="Profile Photo"
                            >
                            `;

                    };

                reader.readAsDataURL(
                    file
                );

            }
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

        saveProfileBtn?.addEventListener(
            "click",
            async () => {

                const nama = 
                    namaInput?.value?.trim();

                const username =
                    usernameInput?.value?.trim();

                const pekerjaan =
                    document.getElementById(
                        "profile-pekerjaan"
                    )?.value?.trim();

                console.log({
                    nama,
                    login_identifier: username,
                    umur: null,
                    pekerjaan
                });


                if(!username){

                    showToast(
                        "Username wajib diisi.",
                        true
                    );

                    return;
                }

                try{

                    const response =
                        await fetch(
                            "/profile/update",
                            {
                                method:"PUT",

                                headers:{
                                    "Content-Type":
                                        "application/json"
                                },

                                body:JSON.stringify({
                                    
                                    nama:nama,
                                    login_identifier:username,
                                    umur:null,
                                    pekerjaan:pekerjaan

                                })

                            }
                        );

                    const result =
                        await response.json();

                    if(!response.ok){

                        throw new Error(
                            result.message ||
                            "Gagal menyimpan profile."
                        );

                    }

                    showToast(
                        result.message ||
                        "Profile berhasil diperbarui."
                    );

                    profileSettingsModal
                        ?.classList
                        .remove(
                            "show"
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