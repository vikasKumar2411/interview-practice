class PrimaryAIProvider:
    async def generate_description(
        self,
        product_name: str,
        features: list[str],
    ) -> str:
        return (
            f"{product_name}: "
            + ", ".join(features)
        )
