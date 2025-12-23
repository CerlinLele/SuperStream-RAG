"""
Example 2: Translation with Mixed Professional Vocabulary

Demonstrates how to handle Chinese queries that contain professional terms and acronyms.
The translator preserves technical terms while translating natural language parts.
"""

from query import QueryTranslator


def main():
    """Run translation example with mixed terminology"""
    translator = QueryTranslator()

    examples = [
        "什么是KYC要求？",
        "SuperStream的ESG评估是什么？",
        "如何通过AML审查？",
        "APRA对金融机构有什么要求？",
        "SIS Act如何影响澳大利亚银行？"
    ]

    for query in examples:
        print(f"Chinese: {query}")
        translation = translator.translate(query)
        print(f"English: {translation}")
        print()


if __name__ == "__main__":
    print("=" * 60)
    print("Example 2: Translation with Mixed Professional Vocabulary")
    print("=" * 60)
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure .env is configured with OPENAI_API_KEY")
