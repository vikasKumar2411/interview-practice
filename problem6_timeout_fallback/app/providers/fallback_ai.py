class FallbackAIProvider:
    async def generate_description(
        self,
        product_name: str,
        features: list[str],
    ) -> str:
        return (
            f"{product_name} is a dependable product with "
            + ", ".join(features)
        )
