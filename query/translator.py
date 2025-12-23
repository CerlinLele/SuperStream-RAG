"""Query Translation Module - Handles multilingual query translation"""

import re
from typing import Optional, List, Tuple
from .api_client import create_openai_client


class QueryTranslator:
    """
    Handles translation of queries between languages.
    Primary use: Chinese queries to English for retrieval in English documents.
    Supports language detection and translation.
    """

    # Technical terms that should be preserved during translation
    TECHNICAL_TERMS = {
        "SuperStream", "APRA", "SIS Act", "AML", "KYC", "ESG"
    }

    # Supported languages
    SUPPORTED_LANGUAGES = ["en", "zh"]

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

    def detect_language(self, query: str) -> str:
        """
        Detect the language of the input query.
        Returns language code: "en", "zh", "mixed", etc.
        """
        # Check for Chinese characters
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
        english_pattern = re.compile(r'[a-zA-Z]')

        has_chinese = bool(chinese_pattern.search(query))
        has_english = bool(english_pattern.search(query))

        if has_chinese and has_english:
            return "mixed"
        elif has_chinese:
            return "zh"
        elif has_english:
            return "en"
        else:
            return "unknown"

    def translate_query(self, query: str, source_lang: Optional[str] = None, target_lang: str = "en") -> str:
        """
        Translate query from source language to target language.
        If source_lang is None, auto-detect it.
        """
        if source_lang is None:
            source_lang = self.detect_language(query)

        # If already in target language, return as-is
        if source_lang == target_lang:
            return query

        # Handle mixed language queries
        if source_lang == "mixed":
            return self.handle_mixed_language_query(query)[0]

        # Route to specific translation methods
        if source_lang == "zh" and target_lang == "en":
            return self.translate_chinese_to_english(query)
        elif source_lang == "en" and target_lang == "zh":
            return self.translate_english_to_chinese(query)
        else:
            # Fallback to general translation
            return self._translate_via_openai(query, source_lang, target_lang)

    def translate_chinese_to_english(self, query: str) -> str:
        """
        Specialized translation from Chinese to English.
        Preserves technical terms and proper nouns.
        """
        technical_terms_str = ", ".join(self.TECHNICAL_TERMS)

        prompt = f"""Translate the following Chinese query to English for semantic search purposes.

Important instructions:
1. Preserve these technical terms exactly as-is: {technical_terms_str}
2. Keep proper nouns unchanged
3. Focus on semantic meaning for document retrieval
4. Return only the translated query, no explanations

Chinese query: {query}

English translation:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator specializing in technical and financial documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            translated = response.choices[0].message.content.strip()
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return query

    def translate_english_to_chinese(self, query: str) -> str:
        """
        Specialized translation from English to Chinese.
        For response display purposes.
        """
        prompt = f"""Translate the following English text to Chinese.

Important instructions:
1. Preserve proper nouns and brand names
2. Use professional terminology appropriate for financial/compliance context
3. Return only the translated text, no explanations

English text: {query}

Chinese translation:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator specializing in technical and financial documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            translated = response.choices[0].message.content.strip()
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return query

    def handle_mixed_language_query(self, query: str) -> Tuple[str, str]:
        """
        Handle queries with mixed Chinese and English.
        Separates and processes each language portion.
        Returns (normalized_query, language_info)
        """
        # Split by language patterns and translate Chinese parts
        result_parts = []
        language_info = "mixed"

        # Pattern to match Chinese sequences
        chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

        last_end = 0
        for match in chinese_pattern.finditer(query):
            # Add English part before Chinese
            if match.start() > last_end:
                result_parts.append(query[last_end:match.start()])

            # Translate Chinese part
            chinese_text = match.group()
            translated = self.translate_chinese_to_english(chinese_text)
            result_parts.append(translated)

            last_end = match.end()

        # Add remaining English part
        if last_end < len(query):
            result_parts.append(query[last_end:])

        normalized_query = "".join(result_parts).strip()
        return normalized_query, language_info

    def preserve_technical_terms(self, query: str, technical_terms: Optional[List[str]] = None) -> str:
        """
        Translate query while preserving SuperStream technical terms.
        Example: Keep "SuperStream", "APRA", "SIS Act" in English
        """
        terms_to_preserve = technical_terms or list(self.TECHNICAL_TERMS)

        # Create placeholders for technical terms
        placeholders = {}
        modified_query = query

        for i, term in enumerate(terms_to_preserve):
            placeholder = f"__TECH_TERM_{i}__"
            # Case-insensitive replacement
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            matches = pattern.findall(modified_query)
            if matches:
                modified_query = pattern.sub(placeholder, modified_query)
                placeholders[placeholder] = matches[0]

        # Translate the modified query
        if self.detect_language(modified_query) == "zh":
            translated = self.translate_chinese_to_english(modified_query)
        else:
            translated = modified_query

        # Restore technical terms
        for placeholder, original_term in placeholders.items():
            translated = translated.replace(placeholder, original_term)

        return translated

    def _translate_via_openai(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generic translation using OpenAI API"""
        prompt = f"Translate the following {source_lang} text to {target_lang}. Return only the translation:\n\n{text}"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def get_translation_confidence(self, original: str, translated: str) -> float:
        """
        Calculate confidence score of translation quality.
        Returns score between 0.0 and 1.0
        """
        # Simple heuristic: longer translations tend to be more confident
        if not original or not translated:
            return 0.0

        length_ratio = len(translated) / len(original) if original else 1.0
        # Reasonable translations are typically 0.8-1.5x the length
        if 0.6 < length_ratio < 1.8:
            confidence = 0.9
        elif 0.3 < length_ratio < 2.5:
            confidence = 0.7
        else:
            confidence = 0.5

        # Check if technical terms were preserved
        preserved_terms = sum(1 for term in self.TECHNICAL_TERMS if term in translated)
        if preserved_terms > 0:
            confidence = min(1.0, confidence + 0.1)

        return confidence

    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        return self.SUPPORTED_LANGUAGES.copy()

    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported"""
        return language_code in self.SUPPORTED_LANGUAGES or language_code == "mixed"
