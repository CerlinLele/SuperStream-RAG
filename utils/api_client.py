"""API Client Module - Centralized OpenAI client initialization and configuration"""

import os
from typing import Optional
from openai import OpenAI


class APIClientConfig:
    """
    Centralized configuration for API clients.
    Manages OpenAI API initialization with support for custom base URLs.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
    ):
        """
        Initialize API client configuration.

        Args:
            api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
            api_base: OpenAI API base URL. Defaults to OPENAI_API_BASE env var.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE")

    def create_client(self) -> OpenAI:
        """
        Create and return an initialized OpenAI client.

        Returns:
            OpenAI: Configured OpenAI client instance.

        Raises:
            ValueError: If API key is not configured.
        """
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured. Please set it in .env file or pass it explicitly.")

        client_kwargs = {"api_key": self.api_key}
        if self.api_base:
            client_kwargs["base_url"] = self.api_base

        return OpenAI(**client_kwargs)

    def get_api_key(self) -> str:
        """Get the configured API key."""
        return self.api_key

    def get_api_base(self) -> Optional[str]:
        """Get the configured API base URL."""
        return self.api_base

    def is_configured(self) -> bool:
        """Check if API is properly configured."""
        return bool(self.api_key)


def create_openai_client(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
) -> OpenAI:
    """
    Convenience function to create an OpenAI client.

    Args:
        api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
        api_base: OpenAI API base URL. Defaults to OPENAI_API_BASE env var.

    Returns:
        OpenAI: Configured OpenAI client instance.

    Raises:
        ValueError: If API key is not configured.
    """
    config = APIClientConfig(api_key=api_key, api_base=api_base)
    return config.create_client()
