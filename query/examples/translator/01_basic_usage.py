"""
Example 1: Basic Usage

Demonstrates basic usage of QueryTranslator:
- Initializing the translator
- Translating Chinese queries to English
"""

from query import QueryTranslator


def main():
    """Run basic usage example"""
    translator = QueryTranslator()

    # Example 1: Simple query
    query1 = "SuperStream如何进行AML合规检查？"
    result1 = translator.translate(query1)
    print(f"Original (Chinese): {query1}")
    print(f"Translated (English): {result1}")
    print()

    # Example 2: Query with technical terms
    query2 = "APRA对SIS Act的要求是什么？"
    result2 = translator.translate(query2)
    print(f"Original (Chinese): {query2}")
    print(f"Translated (English): {result2}")


if __name__ == "__main__":
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure .env is configured with OPENAI_API_KEY")
