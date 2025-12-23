"""Query Translation Module - Translate Chinese queries to English for retrieval"""

from typing import Optional
from utils import create_openai_client


class QueryTranslator:
    """
    Translates Chinese queries to English while preserving technical terms.
    Designed for semantic search in English-language documents.
    """

    # Technical terms that should be preserved during translation
    TECHNICAL_TERMS = {
        "SuperStream", "APRA", "SIS Act", "AML", "KYC", "ESG"
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ):
        """
        Initialize translator with OpenAI client.

        Args:
            api_key: OpenAI API key. Defaults to OPENAI_API_KEY env var.
            api_base: OpenAI API base URL. Defaults to OPENAI_API_BASE env var.
            model: Model to use for translation. Defaults to gpt-3.5-turbo.
        """
        self.model = model
        self.client = create_openai_client(api_key=api_key, api_base=api_base)

    def translate(self, query: str) -> str:
        """
        Translate Chinese query to English for semantic search.
        Preserves technical terms and professional vocabulary.

        Args:
            query: Chinese query text to translate

        Returns:
            English translation of the query
        """
        technical_terms_str = ", ".join(self.TECHNICAL_TERMS)

        prompt = f"""Translate the following Chinese query to English for document retrieval.

Instructions:
1. Preserve these technical terms exactly: {technical_terms_str}
2. Keep proper nouns unchanged
3. Maintain professional/technical vocabulary
4. Return only the translation, no explanations

Chinese query: {query}

English translation:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator specializing in financial and compliance documents. Preserve technical terms and proper nouns."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return query
