document.addEventListener(
    "DOMContentLoaded",
    () => {

        const input =
            document.getElementById(
                "chat-input"
            );

        const sendBtn =
            document.getElementById(
                "send-btn"
            );

        const chatMessages =
            document.getElementById(
                "chat-messages"
            );

        const providerSelect =
            document.getElementById(
                "provider"
            );

        const modelSelect =
            document.getElementById(
                "model"
            );

        const apiKeyInput =
            document.getElementById(
                "api-key"
            );
        const temperatureSlider =
            document.getElementById(
                "temperature"
            );

        const temperatureValue =
            document.getElementById(
                "temperature-value"
            );

        if(
            temperatureSlider &&
            temperatureValue
        ){

            temperatureValue.textContent =
                temperatureSlider.value;

            temperatureSlider.addEventListener(
                "input",
                function(){

                    temperatureValue.textContent =
                        this.value;

                }
            );

        };

        const testConnectionBtn =
            document.getElementById(
                "test-connection-btn"
            );

        // =====================
        // TEST CONNECTION
        // =====================
        async function testConnection(){

            const provider =
                document.getElementById(
                    "provider"
                ).value;

            const modelName =
                document.getElementById(
                    "model"
                ).value;

            const apiKey =
                document.getElementById(
                    "api-key"
                ).value.trim();

            const temperature = 
                document.getElementById(
                    "temperature"
                ).value;

            const missingFields = [];

            if(!provider){
                missingFields.push(
                    "Provider"
                );
            }

            if(!modelName){
                missingFields.push(
                    "Model"
                );
            }

            if(!apiKey){
                missingFields.push(
                    "API Key"
                );
            }

            if(missingFields.length > 0){

                window.showToast(
                    `Silakan lengkapi terlebih dahulu: ${missingFields.join(", ")}`,
                    true
                );

                return;
            }

            try{

                const response =
                    await fetch(
                        "/chatbot/test-connection",
                        {
                            method:"POST",

                            headers:{
                                "Content-Type":
                                "application/json"
                            },

                            body:JSON.stringify({
                                provider:provider,
                                model_name:modelName,
                                api_key:apiKey, 
                                temperature: temperature
                            })
                        }
                    );

                const result =
                    await response.json();

                if(!response.ok){

                    throw new Error(
                        result.detail ||
                        "Gagal melakukan koneksi."
                    );

                }

                window.showToast(
                    result.message
                );

            }
            catch(error){

                window.showToast(
                    error.message,
                    true
                );

            }

        };

        testConnectionBtn.addEventListener(
                "click",
                testConnection
            );

        // =====================
        // CLEAR CHAT
        // =====================
        const clearChatBtn =
            document.getElementById(
                "clear-chat-btn"
            );

        clearChatBtn.addEventListener(
            "click",
            () => {

                chatMessages.innerHTML = "";

                window.showToast(
                    "Riwayat chat berhasil dibersihkan."
                );

            }
        );

        // =====================
        // AUTO GROW TEXTAREA
        // =====================

        input.addEventListener(
            "input",
            () => {

                input.style.height =
                    "auto";

                input.style.height =
                    input.scrollHeight + "px";
            }
        );

        // =====================
        // SEND BUTTON
        // =====================

        sendBtn.addEventListener(
            "click",
            sendMessage
        );

        // =====================
        // ENTER TO SEND
        // =====================

        input.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter"
                    &&
                    !event.shiftKey
                ) {

                event.preventDefault();
                sendMessage(); // ← PANGGIL FUNCTION ASLI
                 }
            }
        );


        // =====================
        // SELECT PROVIDER
        // =====================
        providerSelect.addEventListener(
            "change", 
            loadModels
        )

        // =====================
        // LOAD MODEL SETELAH MILIH PROVIDER
        // =====================
        async function loadModels(){

            const provider =
                document.getElementById(
                    "provider"
                ).value;

            const response =
                await fetch(
                    "/chatbot/models"
                );

            const result =
                await response.json();

            const modelSelect =
                document.getElementById(
                    "model"
                );

            modelSelect.innerHTML =
                '<option value="">Pilih Model</option>';

            const models =
                result.models[provider] || [];

            models.forEach(
                model => {

                    modelSelect.innerHTML += `
                        <option value="${model.value}">
                            ${model.label}
                        </option>
                    `;

                }
            );
        }

        // =====================
        // SEND MESSAGE
        // =====================

        async function sendMessage(){

            const message =
                input.value.trim();

            const provider =
                providerSelect.value;

            const model_name =
                modelSelect.value;

            const api_key =
                apiKeyInput.value.trim();

            const missingFields = [];

            if(!provider){
                missingFields.push(
                    "Provider"
                );
            }

            if(!model_name){
                missingFields.push(
                    "Model"
                );
            }

            if(!api_key){
                missingFields.push(
                    "API Key"
                );
            }

            if(!message){
                missingFields.push(
                    "Pesan"
                );
            }

            if(missingFields.length > 0){

                window.showToast(
                    `Silakan lengkapi terlebih dahulu: ${missingFields.join(", ")}`,
                    true
                );

                return;
            }

            const temperature =
                parseFloat(
                    document.getElementById(
                        "temperature"
                    ).value
                );

            // =====================
            // USER MESSAGE
            // =====================

            appendUserMessage(
                message
            );

            input.value = "";

            input.style.height =
                "auto";

            // =====================
            // LOADING MESSAGE
            // =====================

            const loadingBubble =
                appendLoadingMessage();

            isLoading = true;

            // ubah icon jadi STOP
            sendBtn.innerHTML = `<i class="fas fa-square"></i>`;
            sendBtn.classList.add("stop-btn");

            try{

                const response =
                    await fetch(
                        "/chatbot/send-message",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                provider:
                                    provider,

                                model_name:
                                    model_name,

                                api_key:
                                    api_key,

                                message:
                                    message,

                                temperature:
                                    temperature
                            })
                        }
                    );

                const result =
                    await response.json();
                console.log(result);

                loadingBubble.remove();

                if(!result.success){

                    appendAIMessage(
                        result.message
                    );

                    isLoading = false;
                    sendBtn.innerHTML = `<i class="fas fa-arrow-up"></i>`;
                    sendBtn.classList.remove("stop-btn");

                    return;
                }

                appendAIMessage(
                    result.response
                );

                isLoading = false;
                sendBtn.innerHTML = `<i class="fas fa-arrow-up"></i>`;
                sendBtn.classList.remove("stop-btn");

            }
            catch(error){

                loadingBubble.remove();

                appendAIMessage(
                    "Maaf, terjadi kesalahan saat menghubungi server."
                );

                console.error(
                    error
                );

                isLoading = false;
                sendBtn.innerHTML = `<i class="fas fa-arrow-up"></i>`;
                sendBtn.classList.remove("stop-btn");
            }
        }
        

        // =====================
        // USER MESSAGE
        // =====================

        function appendUserMessage(
            text
        ){

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "user-message";

            div.textContent =
                text;

            chatMessages.appendChild(
                div
            );

            scrollBottom();
        }

        // =====================
        // AI MESSAGE
        // =====================

        function appendAIMessage(
            text
        ){

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "ai-message";

            div.textContent =
                text;

            chatMessages.appendChild(
                div
            );

            scrollBottom();
        }

        // =====================
        // LOADING MESSAGE
        // =====================

        function appendLoadingMessage(){

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "ai-message";

            div.textContent =
                "Tunggu sebentar ya...";

            chatMessages.appendChild(
                div
            );

            scrollBottom();

            return div;
        }

        // =====================
        // SCROLL
        // =====================

        function scrollBottom(){

            chatMessages.scrollTop =
                chatMessages.scrollHeight;
        }

    }
);