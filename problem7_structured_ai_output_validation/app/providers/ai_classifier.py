class AIClassifier:
    async def classify(self, text: str) -> dict:
        return {
            "category": "technical",
            "priority": "medium",
            "summary": f"Technical issue: {text}",
        }
