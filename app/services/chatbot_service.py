# app/services/chatbot_service.py

from sqlalchemy.orm import Session

from core.ai_provider import (
    generate_ai_response
)

from core.ai_model import (
    is_valid_model
)

from app.repositories.chatbot_repository import (
    save_chat_history
)

from app.services.rag_services import (
    RAGService
)


class ChatbotService:

    # ==========================================
    # TEST CONNECTION
    # ==========================================

    @staticmethod
    def test_connection(
        provider: str,
        model_name: str,
        api_key: str
    ):

        if not provider:
            raise ValueError(
                "Provider AI wajib dipilih."
            )

        if not model_name:
            raise ValueError(
                "Model AI wajib dipilih."
            )

        if provider != "Ollama Local":

            if not api_key:
                raise ValueError(
                    "API Key wajib diisi."
                )

        if not is_valid_model(
            provider=provider,
            model_name=model_name
        ):
            raise ValueError(
                "Model tidak valid."
            )

        try:

            generate_ai_response(
                provider=provider,
                api_key=api_key,
                model_name=model_name,
                prompt="Balas dengan kata: OK"
            )

            return True

        except Exception as e:
            print("Service Error", repr(e)) 

            raise ValueError(
                ChatbotService.get_friendly_error(
                    str(e)
                )
            )

    # ==========================================
    # SEND MESSAGE
    # ==========================================
    @staticmethod
    def send_message(
        db: Session,
        user_id: int,
        provider: str,
        model_name: str,
        api_key: str,
        message: str,
        temperature: float = 0.7
    ):

        if not message.strip():

            raise ValueError(
                "Pesan tidak boleh kosong."
            )

        if not is_valid_model(
            provider=provider,
            model_name=model_name
        ):
            raise ValueError(
                "Model tidak valid."
            )

        try:

            # ==================================
            # SAVE USER MESSAGE
            # ==================================
            print("STEP 1")
            save_chat_history(
                db=db,
                user_id=user_id,
                role="user",
                message=message,
                provider=provider,
                model_name=model_name
            )

            # ==================================
            # BUILD RAG CONTEXT
            # ==================================
            print("STEP 2")
            context = (
                RAGService.build_financial_context(
                    db=db,
                    user_id=user_id
                )
            )

            # ==================================
            # FINAL PROMPT
            # ==================================

            final_prompt = f"""
                {context}

                PERTANYAAN USER:
                {message}
                """

            # ==================================
            # CALL MODEL
            # ==================================


            print("STEP 3")

            final_prompt = f"""
            {context}

            PERTANYAAN USER:
            {message}
            """

            print("STEP 4")

            print("PROVIDER =", provider)
            print("MODEL =", model_name)
            print("TEMP =", temperature)
            print("PROMPT LENGTH =", len(final_prompt))
            print("SEBELUM GENERATE")

            ai_response = generate_ai_response(
                provider=provider,
                api_key=api_key,
                model_name=model_name,
                prompt=final_prompt,
                temperature=temperature
            )

            # ==================================
            # SAVE AI RESPONSE
            # ==================================

            save_chat_history(
                db=db,
                user_id=user_id,
                role="assistant",
                message=ai_response,
                provider=provider,
                model_name=model_name
            )

            return ai_response

        except Exception as e:

            raise ValueError(
                ChatbotService.get_friendly_error(
                    str(e)
                )
            )

    # ==========================================
    # FRIENDLY ERROR
    # ==========================================

    @staticmethod
    def get_friendly_error(
        error_message: str
    ) -> str:

        error_text = (
            error_message.lower()
        )

        if (
            "resource_exhausted"
            in error_text
        ):
            return (
                "Kuota API Key telah habis. "
                "Silakan gunakan API Key lain "
                "atau coba kembali nanti."
            )

        if (
            "quota"
            in error_text
        ):
            return (
                "Kuota API telah habis."
            )

        if (
            "invalid"
            in error_text
        ):
            return (
                "API Key tidak valid."
            )

        if (
            "unauthorized"
            in error_text
        ):
            return (
                "API Key tidak memiliki akses."
            )

        if (
            "timeout"
            in error_text
        ):
            return (
                "Permintaan terlalu lama diproses. "
                "Silakan coba kembali."
            )

        if (
            "connection"
            in error_text
        ):
            return (
                "Gagal terhubung ke layanan AI."
            )

        if "429" in error_text:
            return (
                "Terlalu banyak permintaan. "
                "Silakan coba beberapa saat lagi."
            )

        if "api key" in error_text:
            return (
                "API Key tidak valid atau belum diisi."
            )

        if "model" in error_text:
            return (
                "Model AI yang dipilih tidak tersedia."
            )

        if "rate limit" in error_text:
            return (
                "Batas penggunaan API telah tercapai."
            )

        return (
            "Terjadi kesalahan saat "
            "menghubungi layanan AI."
        )