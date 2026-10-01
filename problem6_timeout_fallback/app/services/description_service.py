from app.providers.primary_ai import PrimaryAIProvider
from app.providers.fallback_ai import FallbackAIProvider


class DescriptionService:
    def __init__(
        self,
        primary_provider: PrimaryAIProvider,
        fallback_provider: FallbackAIProvider,
    ) -> None:
        self.primary_provider = primary_provider
        self.fallback_provider = fallback_provider

    async def generate_description(
        self,
        product_name: str,
        features: list[str],
    ) -> str:
        return await self.primary_provider.generate_description(
            product_name,
            features,
        )
