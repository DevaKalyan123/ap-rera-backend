from app.services.faq_service import FaqService
from app.services.llm_service import LLMService


class ChatService:

    @staticmethod
    def process_message(message: str) -> str:

        print("\n==============================")

        # 🔹 STEP 1: VALIDATION
        if not message or not message.strip():
            return "Please enter a valid question."

        message = message.strip()

        print("📩 USER MESSAGE:", message)

        # 🔹 STEP 2: NORMALIZE INPUT (VERY IMPORTANT)
        normalized_message = message.lower()
        normalized_message = normalized_message.replace("reg", "registration")
        normalized_message = normalized_message.replace("aprera", "ap rera")

        print("🧹 NORMALIZED:", normalized_message)

        # 🔹 STEP 3: BUILD CONTEXT (FAQ + SYSTEM KNOWLEDGE)
        faq_context = FaqService.get_all_faqs_as_text()

        system_context = """
AP RERA SYSTEM (Andhra Pradesh Real Estate Regulatory Authority):

MAIN MODULES:
- Project Registration
- Promoter Registration
- Agent Registration
- Complaint Registration
- Fee Calculator
- Status Tracking

PROCESS FLOW:
- Promoter must register first
- Then project registration
- Agents must register separately

NAVIGATION:
- Registration → All registration modules
- Registered → Projects, Agents
- Knowledge Hub → Forms, Manuals, Videos

IMPORTANT RULES:
- Fee depends on project size (use Fee Calculator)
- Status requires application number
- Do NOT generate fake values or assumptions
"""

        full_context = system_context + "\n\n" + faq_context

        print("📚 CONTEXT LENGTH:", len(full_context))

        # 🔹 STEP 4: CALL LLM
        llm_response = LLMService.get_llm_response(normalized_message, full_context)

        if llm_response:
            print("✅ LLM RESPONSE SUCCESS")
            return llm_response

        # 🔹 STEP 5: FALLBACK
        print("❌ LLM FAILED")

        return (
            "I couldn't find the exact information.\n"
            "Please try asking more clearly or check the portal."
        )