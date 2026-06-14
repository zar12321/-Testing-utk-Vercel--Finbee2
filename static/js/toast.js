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

    text.textContent = message;

    toast.classList.remove("error");

    if(isError){
        toast.classList.add("error");
    }

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}