import asyncio

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
        try:
            return await asyncio.wait_for(
                self.primary_provider.generate_description(
                    product_name,
                    features,
                ),
                timeout=0.2,
            )
        except TimeoutError:
            return await self.fallback_provider.generate_description(
                product_name,
                features,
            )
