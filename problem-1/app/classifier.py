class TicketClassifier:
    def classify(self, message: str) -> tuple[str, float]:
        text = message.lower()

        if "fraud" in text or "stolen" in text:
            return "security", 0.96

        if "charged twice" in text or "duplicate charge" in text:
            return "billing", 0.91

        if "password" in text or "login" in text:
            return "account", 0.87

        return "general", 0.58