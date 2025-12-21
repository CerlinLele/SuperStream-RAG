"""Query Intent Detection Module - Identifies user intent and query type"""

from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class IntentInfo:
    """Represents detected query intent"""
    primary_intent: str  # main intent type
    secondary_intents: List[str]  # other possible intents
    intent_confidence: float  # 0.0 to 1.0
    query_type: str  # specific query category


class IntentDetector:
    """
    Detects user query intent and question type.
    Helps optimize retrieval strategy based on intent.

    Intent types:
    - definition: Asking for explanation/definition of a concept
    - requirement: Asking about rules, regulations, requirements
    - process: Asking for steps or procedures
    - penalty: Asking about consequences or penalties
    - exception: Asking about exceptions or special cases
    - clarification: Asking to clarify conflicting information
    - comparison: Comparing two concepts or scenarios
    - calculation: Asking for numerical calculation
    """

    def detect_intent(self, query: str) -> IntentInfo:
        """
        Detect the primary intent of the query.
        Returns IntentInfo with primary and secondary intents.
        """
        pass

    def is_definition_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is asking for a definition.
        Example: "What is SuperStream?", "Define APRA"
        Returns (is_definition, confidence)
        """
        pass

    def is_requirement_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is asking about requirements or rules.
        Example: "What must employers do?", "Are there any restrictions?"
        Returns (is_requirement, confidence)
        """
        pass

    def is_process_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is asking about a process or procedure.
        Example: "How to file?", "Steps for submitting?"
        Returns (is_process, confidence)
        """
        pass

    def is_penalty_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is asking about penalties or consequences.
        Example: "What happens if...", "Are there penalties for..."
        Returns (is_penalty, confidence)
        """
        pass

    def is_exception_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is asking about exceptions or special cases.
        Example: "Are there any exceptions?", "What about special cases?"
        Returns (is_exception, confidence)
        """
        pass

    def is_comparison_query(self, query: str) -> Tuple[bool, float]:
        """
        Detect if query is comparing two concepts or scenarios.
        Example: "Difference between X and Y?", "X vs Y?"
        Returns (is_comparison, confidence)
        """
        pass

    def get_intent_keywords(self, intent_type: str) -> List[str]:
        """
        Get list of keywords associated with an intent type.
        Used for pattern matching during intent detection.
        """
        pass

    def get_optimal_retrieval_strategy(self, intent: str) -> Dict[str, any]:
        """
        Get recommended retrieval strategy based on detected intent.
        Returns dict with retrieval parameters and hints.
        """
        pass

    def rank_intents(self, query: str) -> List[Tuple[str, float]]:
        """
        Rank possible intents by likelihood.
        Returns list of (intent, confidence) tuples sorted by confidence.
        """
        pass
