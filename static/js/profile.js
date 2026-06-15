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

        const settingsBtn =
            document.getElementById(
                "settings-btn"
            );

        const settingsPanel =
            document.getElementById(
                "settings-panel"
            );

        const resetPasswordBtn =
            document.getElementById(
                "reset-password-btn"
            );

        const resetPasswordModal =
            document.getElementById(
                "reset-password-modal"
            );

        const closeResetPasswordModal =
            document.getElementById(
                "close-reset-password-modal"
            );

        const toggleNewPassword =
            document.getElementById(
                "toggle-new-password"
            );

        const toggleConfirmPassword =
            document.getElementById(
                "toggle-confirm-password"
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

        const usernameMsg =
            document.getElementById(
                "profile-username-msg"
            );
                
        const pekerjaanInput =
            document.getElementById(
                "profile-pekerjaan"
            );

        const pekerjaanMsg =
            document.getElementById(
                "pekerjaan-msg"
            );

        const settingsWrapper =
            document.querySelector(
                ".settings-wrapper"
            );

        const settingsTrigger =
            document.getElementById(
                "settings-trigger"
            );

        const saveResetPasswordBtn =
            document.getElementById(
                "save-reset-password"
            );

        const newPasswordInput =
            document.getElementById(
                "new-password"
            );

        const confirmPasswordInput =
            document.getElementById(
                "confirm-password"
            );

        const resetPasswordMsg =
            document.getElementById(
                "reset-password-msg"
            );

        const resetConfirmMsg =
            document.getElementById(
                "reset-confirm-msg"
            );

        let settingsPinned = false;
        let profilePinned = false;

        

        let usernameAvailable = true;
        let usernameTimer;
        let namaValid = true;
        let pekerjaanValid = true;

        let originalNama = "";
        let originalUsername = "";
        let originalPekerjaan = "";

        let selectedPhotoFile = null;

        let originalPhotoHtml = "";


        const namaInput =
            document.getElementById(
                "profile-nama"
            );
        
        const namaMsg = 
            document.getElementById(
                "profile-nama-msg"
            )

        function validateProfileForm(){

            const isValid =
                usernameAvailable &&
                namaValid &&
                pekerjaanValid;

            saveProfileBtn.disabled =
                !isValid;

            saveProfileBtn.classList.toggle(
                "disabled",
                !isValid
            );

        };

        function validateResetPassword(){

            if(
                !newPasswordInput ||
                !confirmPasswordInput
            ){
                return false;
            }

            const password =
                newPasswordInput.value.trim();

            const confirm =
                confirmPasswordInput.value.trim();

            let valid = true;

            // PASSWORD

            if(password === ""){

                resetPasswordMsg.innerHTML = "";

                valid = false;

            }
            else if(password.length < 8){

                resetPasswordMsg.style.color =
                    "red";

                resetPasswordMsg.innerHTML =
                    "✗ Password minimal 8 karakter";

                valid = false;

            }
            else{

                resetPasswordMsg.style.color =
                    "green";

                resetPasswordMsg.innerHTML =
                    "✓ Password memenuhi syarat";

            }

            // KONFIRMASI

            if(confirm === ""){

                resetConfirmMsg.innerHTML = "";

                valid = false;

            }
            else if(password !== confirm){

                resetConfirmMsg.style.color =
                    "red";

                resetConfirmMsg.innerHTML =
                    "✗ Password tidak sama";

                valid = false;

            }
            else{

                resetConfirmMsg.style.color =
                    "green";

                resetConfirmMsg.innerHTML =
                    "✓ Password sesuai";

            }

            return valid;

        };

        newPasswordInput?.addEventListener(
            "input",
            validateResetPassword
        );

        confirmPasswordInput?.addEventListener(
            "input",
            validateResetPassword
        );

        settingsTrigger?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                settingsPinned =
                    !settingsPinned;

                settingsWrapper.classList.toggle(
                    "pinned",
                    settingsPinned
                );

                if(settingsPinned){

                    profilePinned = true;

                    dropdown.classList.add(
                        "show"
                    );

                };

            }
        );


        profileSettingsBtn?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                profilePinned = true;

                settingsPinned = true;

                dropdown.classList.add(
                    "show"
                );

                settingsWrapper?.classList.add(
                    "pinned"
                );

                originalNama =
                    namaInput?.value || "";

                originalUsername =
                    usernameInput?.value || "";

                originalPekerjaan =
                    pekerjaanInput?.value || "";

                originalPhotoHtml =
                    profilePreview.innerHTML;

                profileSettingsModal.classList.add(
                    "show"
                );

            }
        );

        resetPasswordBtn?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                newPasswordInput.value = "";
                confirmPasswordInput.value = "";

                resetPasswordMsg.innerHTML = "";
                resetConfirmMsg.innerHTML = "";

                profilePinned = true;
                settingsPinned = true;

                dropdown.classList.add(
                    "show"
                );

                settingsWrapper?.classList.add(
                    "pinned"
                );

                resetPasswordModal.classList.add(
                    "show"
                );

            }
);

        closeProfileModal?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                namaInput.value =
                    originalNama;

                usernameInput.value =
                    originalUsername;

                pekerjaanInput.value =
                    originalPekerjaan;

                selectedPhotoFile = null;

                profilePreview.innerHTML =
                    originalPhotoHtml;

                profileSettingsModal.classList.remove(
                    "show"
                );

                dropdown.classList.add(
                    "show"
                );

                settingsWrapper?.classList.add(
                    "pinned"
                );

                profilePinned = true;

                settingsPinned = true;

            }
        );

        closeResetPasswordModal?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                resetPasswordModal.classList.remove(
                    "show"
                );

                dropdown.classList.add(
                    "show"
                );

                settingsWrapper?.classList.add(
                    "pinned"
                );

                profilePinned = true;
                settingsPinned = true;

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

                selectedPhotoFile = file;

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

                profilePinned =
                    !profilePinned;

                dropdown.classList.toggle(
                    "show",
                    profilePinned
                );

            }
        );

        document.addEventListener(
            "click",
            (e) => {

                if(
                    profileSettingsModal.classList.contains("show") ||
                    resetPasswordModal.classList.contains("show")
                ){
                    return;
                }

                if(
                    !e.target.closest(".profile-wrapper")
                ){

                    profilePinned = false;

                    settingsPinned = false;

                    dropdown.classList.remove(
                        "show"
                    );

                    settingsWrapper?.classList.remove(
                        "pinned"
                    );

                }

            }
        );

        resetBtn?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                settingsPinned = false;

                settingsWrapper?.classList.remove(
                    "pinned"
                );

                profilePinned = true;

                dropdown.classList.add(
                    "show"
                );

                modal.classList.add(
                    "show"
                );

            }
        );

        cancelBtn?.addEventListener(
            "click",
            (e) => {

                e.stopPropagation();

                modal.classList.remove(
                    "show"
                );

                profilePinned = true;

                dropdown.classList.add(
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

                    profilePinned = true;

                    dropdown.classList.add(
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

                    profilePinned = true;

                    dropdown.classList.add(
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

        namaInput?.addEventListener(
            "input",
            () => {

                const nama =
                    namaInput.value.trim();

                if(nama.length < 3){

                    namaValid = false;

                    namaMsg.style.color =
                        "red";

                    namaMsg.innerHTML =
                        "✗ Nama minimal 3 karakter";

                }
                else{

                    namaValid = true;

                    namaMsg.style.color =
                        "green";

                    namaMsg.innerHTML =
                        "✓ Nama valid";

                }

                validateProfileForm();

            }
        );

        usernameInput?.addEventListener(
            "input",
            () => {

                clearTimeout(
                    usernameTimer
                );

                usernameTimer =
                    setTimeout(
                        async () => {

                            const username =
                                usernameInput.value.trim();

                            if(username.length < 3){

                                usernameAvailable = false;

                                usernameMsg.style.color = "red";

                                usernameMsg.innerHTML =
                                    "✗ Username minimal 3 karakter";

                                validateProfileForm();

                                return;
                            }

                            const response =
                                await fetch(
                                    `/auth/check-username?login_identifier=${encodeURIComponent(username)}`
                                );

                            const data =
                                await response.json();

                            if(data.available){

                                usernameAvailable = true;

                                validateProfileForm();

                                usernameMsg.style.color =
                                    "green";

                                usernameMsg.innerHTML =
                                    "✓ Username dapat digunakan";

                            }
                            else{

                                usernameAvailable = false;

                                validateProfileForm();

                                usernameMsg.style.color =
                                    "red";

                                usernameMsg.innerHTML =
                                    "✗ Username sudah digunakan";

                            }

                        },
                        400
                    );

            }
        );

        pekerjaanInput?.addEventListener(
            "input",
            () => {

                const pekerjaan =
                    pekerjaanInput.value.trim();

                if(
                    pekerjaan.length > 0 &&
                    !/^[A-Za-z\s]+$/.test(
                        pekerjaan
                    )
                ){

                    pekerjaanValid = false;

                    pekerjaanMsg.style.color =
                        "red";

                    pekerjaanMsg.innerHTML =
                        "✗ Hanya huruf yang diperbolehkan";

                }
                else{

                    pekerjaanValid = true;

                    pekerjaanMsg.style.color =
                        "green";

                    pekerjaanMsg.innerHTML =
                        pekerjaan.length
                            ? "✓ Pekerjaan valid"
                            : "";

                }

                validateProfileForm();

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

                    };

                    if(selectedPhotoFile){

                        const formData =
                            new FormData();

                        formData.append(
                            "file",
                            selectedPhotoFile
                        );

                        const photoResponse =
                            await fetch(
                                "/profile/upload-photo",
                                {
                                    method:"POST",
                                    body:formData
                                }
                            );

                        const photoResult =
                            await photoResponse.json();

                        if(!photoResponse.ok){

                            throw new Error(
                                photoResult.detail ||
                                photoResult.message ||
                                "Gagal upload foto"
                            );
                        }

                        const navbarAvatar =
                            document.querySelector(
                                ".profile-avatar"
                            );

                        if(navbarAvatar){

                            navbarAvatar.innerHTML = `
                                <img
                                    src="${photoResult.profile_photo}"
                                    alt="Profile Photo"
                                >
                            `;
                        }

                        selectedPhotoFile = null;
                    };

                    showToast(
                        result.message ||
                        "Profile berhasil diperbarui."
                    );

                    const heroTitle =
                        document.getElementById(
                            "hero-title"
                        );

                    if(heroTitle){

                        heroTitle.textContent =
                            `Halo, ${username}`;
                    };

                    const profileName =
                        document.querySelector(
                            ".profile-name"
                        );

                    if(profileName){
                        profileName.textContent =
                            username;
                    };

                    profileSettingsModal
                        ?.classList
                        .remove(
                            "show"
                        );

                    dropdown.classList.add(
                            "show"
                        );

                        settingsWrapper?.classList.add(
                            "pinned"
                        );

                        profilePinned = true;

                        settingsPinned = true;

                }
                catch(error){

                    showToast(
                        error.message,
                        true
                    );

                }

            }
        );

        saveResetPasswordBtn?.addEventListener(
            "click",
            async () => {

                if(
                    !validateResetPassword()
                ){

                    showToast(
                        "Periksa kembali password.",
                        true
                    );

                    return;
                }

                try{

                    const response =
                        await fetch(
                            "/profile/update",
                            {
                                method: "PUT",

                                headers:{
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({

                                    nama:
                                        document
                                        .getElementById(
                                            "profile-nama"
                                        )?.value,

                                    login_identifier:
                                        document
                                        .getElementById(
                                            "profile-username"
                                        )?.value,

                                    pekerjaan:
                                        document
                                        .getElementById(
                                            "profile-pekerjaan"
                                        )?.value,

                                    umur: null,

                                    password:
                                        newPasswordInput.value,

                                    confirm_password:
                                        confirmPasswordInput.value

                                })

                            }
                        );

                    const result =
                        await response.json();

                    if(!response.ok){

                        throw new Error(
                            result.message ||
                            "Gagal reset password."
                        );

                    }

                    resetPasswordModal.classList.remove(
                        "show"
                    );

                    dropdown.classList.add(
                        "show"
                    );

                    settingsWrapper?.classList.add(
                        "pinned"
                    );

                    profilePinned = true;
                    settingsPinned = true;

                    showToast(
                        "Password berhasil diubah."
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

        function setupPasswordToggle(
            button,
            input
        ){

            if(
                !button ||
                !input
            ){
                return;
            }

            button.addEventListener(
                "click",
                () => {

                    const isPassword =
                        input.type ===
                        "password";

                    input.type =
                        isPassword
                            ? "text"
                            : "password";

                    const icon =
                        button.querySelector(
                            "i"
                        );

                    if(!icon){
                        return;
                    }

                    icon.className =
                        isPassword
                            ? "fa-solid fa-eye-slash"
                            : "fa-solid fa-eye";

                }
            );

        }

        setupPasswordToggle(
            toggleNewPassword,
            newPasswordInput
        );

        setupPasswordToggle(
            toggleConfirmPassword,
            confirmPasswordInput
        );

    }
);