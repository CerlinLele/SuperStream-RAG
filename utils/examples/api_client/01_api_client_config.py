"""
Example 1: Direct API Client Configuration

Demonstrates using APIClientConfig for fine-grained control over API settings.
This approach is useful when you need to manage multiple configurations
or verify settings before creating the client.
"""

from utils import APIClientConfig


def main():
    """Run API client configuration example"""
    config = APIClientConfig(
        api_key="sk-...",  # Your actual API key
        api_base="https://api.openai.com/v1"  # Or custom base
    )

    # Verify configuration
    if config.is_configured():
        print("Configuration Status: Valid")
        print(f"API Base: {config.get_api_base() or 'default (OpenAI)'}")

        try:
            client = config.create_client()
            print("OpenAI client created successfully!")
        except Exception as e:
            print(f"Note: {e}")
            print("This example needs valid API credentials to create client")
    else:
        print("Configuration Status: Incomplete")
        print("Please provide api_key and optionally api_base")


if __name__ == "__main__":
    print("=" * 60)
    print("Example 3: Direct API Client Configuration")
    print("=" * 60)
    main()
