class RulesService:

    @staticmethod
    def get_rule_based_response(message: str) -> str | None:
        text = message.lower().strip()

        # 🔹 Greetings
        if any(word in text for word in ["hi", "hello", "hey"]):
            return "Hello! I am the AP RERA Assistant. How can I help you today?"

        # 🔹 PROJECT REGISTRATION
        if any(word in text for word in ["project registration", "register project", "project register"]):
            return (
                "To register a project:\n"
                "Go to Registration → Project Registration.\n"
                "Provide:\n"
                "- Promoter details\n"
                "- Project details\n"
                "- Required documents"
            )

        # 🔹 PROMOTER REGISTRATION
        if "promoter" in text:
            return "Go to Registration → Promoter Registration to register promoter details."

        # 🔹 AGENT REGISTRATION / CHANGE
        if "agent" in text:
            if "change" in text:
                return "To change agent: Go to Agent Registration → Change Request."
            return "To register agent: Go to Registration → Agent Registration."

        # 🔹 COMPLAINT REGISTRATION
        if "complaint" in text:
            return "To raise a complaint: Go to Registration → Complaint Registration."

        # 🔹 FEE / CALCULATOR
        if any(word in text for word in ["fee", "payment", "calculator"]):
            return "Use Registration → Fee Calculator to check project registration fee."

        # 🔹 LOGIN (ADMIN / PROMOTER / DEPARTMENT)
        if "login" in text:
            if "admin" in text:
                return "Go to Login → Admin Login."
            elif "promoter" in text:
                return "Go to Login → Promoter Login."
            elif "department" in text:
                return "Go to Login → Department Login."
            else:
                return "Use the Login menu to access your respective portal (Admin / Promoter / Department)."

        # 🔹 PASSWORD
        if "password" in text:
            return "Click on 'Forgot Password' on the login page to reset your password."

        # 🔹 STATUS TRACKING
        if "status" in text or "track" in text:
            return "Please provide your application number to check status."

        # 🔹 REGISTERED PROJECTS / AGENTS
        if "registered" in text:
            if "project" in text:
                return "Go to Registered → Projects to view registered projects."
            elif "agent" in text:
                return "Go to Registered → Agents to view registered agents."

        # 🔹 REPORTS
        if "report" in text:
            return "Go to Reports section to view project and registration reports."

        # 🔹 JUDGEMENTS / ORDERS
        if "judgement" in text or "order" in text:
            return "Go to Judgements/Orders section to view legal decisions."

        # 🔹 NOTIFICATIONS
        if "notification" in text or "news" in text:
            return "Go to Notifications section to view latest updates."

        # 🔹 KNOWLEDGE HUB
        if any(word in text for word in ["knowledge", "guidelines", "manual", "tutorial", "video"]):
            return (
                "Go to Knowledge Hub section for:\n"
                "- Guidelines\n"
                "- User Manuals\n"
                "- Video Tutorials\n"
                "- Forms Download"
            )

        # 🔹 FORMS DOWNLOAD
        if "form" in text:
            return "Go to Knowledge Hub → Forms Download."

        # 🔹 MOBILE APP
        if "mobile app" in text or "app" in text:
            return "Download the mobile app from Knowledge Hub → Mobile App."

        # 🔹 ABOUT RERA
        if "about" in text:
            return "AP RERA regulates real estate sector ensuring transparency and accountability."

        return None