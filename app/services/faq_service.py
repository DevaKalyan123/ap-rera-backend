from app.models.database import db
from app.models.faq_model import FAQ


class FaqService:

    # 🔥 Synonyms (better understanding)
    SYNONYMS = {
        "docs": "document",
        "documents": "document",
        "papers": "document",

        "needed": "require",
        "required": "require",

        "registration": "register",
        "register": "register",

        "fee": "fee",
        "payment": "fee",

        "status": "status",
        "track": "status",

        "login": "login",
        "password": "password",
    }

    STOPWORDS = {"the", "is", "for", "of", "to", "a", "in", "on", "and"}

    # ---------------- NORMALIZE ----------------
    @staticmethod
    def normalize_text(text: str):
        words = text.lower().split()

        result = []
        for w in words:
            if w in FaqService.STOPWORDS:
                continue
            result.append(FaqService.SYNONYMS.get(w, w))

        return result

    # ---------------- SEARCH ----------------
    @staticmethod
    def search_faq(user_message: str) -> str | None:

        words = FaqService.normalize_text(user_message)

        if not words:
            return None

        faqs = FAQ.query.all()

        best = None
        max_score = 0

        for faq in faqs:
            q = faq.question.lower()

            score = sum(3 for w in words if w in q)

            if " ".join(words) in q:
                score += 5

            if score > max_score:
                max_score = score
                best = faq

        print(f"[FAQ] {user_message} → score={max_score}")

        if max_score < 3:
            return None

        return best.answer if best else None

    # ---------------- 🔥 MAIN LLM CONTEXT ----------------
    @staticmethod
    def get_all_faqs_as_text():

        faqs = FAQ.query.all()

        context = """
AP RERA SYSTEM KNOWLEDGE:

AP RERA is a real estate regulatory system in Andhra Pradesh.

MAIN MODULES:
- Project Registration
- Promoter Registration
- Agent Registration
- Complaint Registration
- Fee Calculator
- Status Tracking

PROCESS DETAILS:

Project Registration:
- Requires promoter details, land documents, approvals
- Done through Registration → Project Registration

Promoter:
- Must be registered before project registration

Agent:
- Agents must register before operating

Fee:
- Depends on project size
- Use Fee Calculator

Status:
- Requires application number

Complaint:
- Available via Complaint Registration

Knowledge Hub:
- Forms, Manuals, Videos

Navigation:
- Registration menu → all modules
- Registered → projects, agents
"""

        for faq in faqs:
            context += f"\nQ: {faq.question}\nA: {faq.answer}\n"

        return context

    # ---------------- DATA INIT ----------------
    @staticmethod
    def initialize_sample_data():

        FAQ.__table__.create(db.engine, checkfirst=True)

        if FAQ.query.count() > 0:
            return "FAQ already exists."

        sample_faqs = [

            FAQ(
                question="documents required for project registration",
                answer="Promoter details, land documents, approvals, layout plans and financial details are required."
            ),

            FAQ(
                question="how to register project",
                answer="Go to Registration → Project Registration, fill details and upload documents."
            ),

            FAQ(
                question="project registration fee",
                answer="Fee depends on project size. Use Fee Calculator in the portal."
            ),

            FAQ(
                question="how to check application status",
                answer="Use your application number in Status Tracking section."
            ),

            FAQ(
                question="approval time for project",
                answer="Approval takes 15 to 30 working days after verification."
            ),

            FAQ(
                question="how to register promoter",
                answer="Go to Registration → Promoter Registration."
            ),

            FAQ(
                question="how to register agent",
                answer="Go to Registration → Agent Registration."
            ),

            FAQ(
                question="agent change request",
                answer="Go to Agent Registration → Change Request."
            ),

            FAQ(
                question="login problem",
                answer="Use Forgot Password or check credentials."
            ),

            FAQ(
                question="download forms",
                answer="Go to Knowledge Hub → Forms Download."
            ),

            FAQ(
                question="complaint registration",
                answer="Go to Registration → Complaint Registration."
            ),

            FAQ(
                question="registered projects",
                answer="Go to Registered → Projects."
            ),

            FAQ(
                question="registered agents",
                answer="Go to Registered → Agents."
            ),
        ]

        db.session.add_all(sample_faqs)
        db.session.commit()

        return "Sample FAQs inserted successfully."