"""Query Translation Module - Handles multilingual query translation"""

from typing import Optional, List, Tuple


class QueryTranslator:
    """
    Handles translation of queries between languages.
    Primary use: Chinese queries to English for retrieval in English documents.
    Supports language detection and translation.
    """

    def detect_language(self, query: str) -> str:
        """
        Detect the language of the input query.
        Returns language code: "en", "zh", "mixed", etc.
        """
        pass

    def translate_query(self, query: str, source_lang: Optional[str] = None, target_lang: str = "en") -> str:
        """
        Translate query from source language to target language.
        If source_lang is None, auto-detect it.
        """
        pass

    def translate_chinese_to_english(self, query: str) -> str:
        """
        Specialized translation from Chinese to English.
        Preserves technical terms and proper nouns.
        """
        pass

    def translate_english_to_chinese(self, query: str) -> str:
        """
        Specialized translation from English to Chinese.
        For response display purposes.
        """
        pass

    def handle_mixed_language_query(self, query: str) -> Tuple[str, str]:
        """
        Handle queries with mixed Chinese and English.
        Separates and processes each language portion.
        Returns (normalized_query, language_info)
        """
        pass

    def preserve_technical_terms(self, query: str, technical_terms: List[str]) -> str:
        """
        Translate query while preserving SuperStream technical terms.
        Example: Keep "SuperStream", "APRA", "SIS Act" in English
        """
        pass

    def get_translation_confidence(self, original: str, translated: str) -> float:
        """
        Calculate confidence score of translation quality.
        Returns score between 0.0 and 1.0
        """
        pass

    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        pass

    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported"""
        pass
