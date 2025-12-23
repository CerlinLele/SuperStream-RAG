"""Query Processing Module for SuperStream RAG"""

from dotenv import load_dotenv

# Load environment variables when the module is imported
load_dotenv()

from utils import APIClientConfig, create_openai_client
from .processor import QueryProcessor
from .normalizer import QueryNormalizer
from .expander import QueryExpander
from .rewriter import QueryRewriter
from .translator import QueryTranslator
from .decomposer import QueryDecomposer
from .intent_detector import IntentDetector

__all__ = [
    "APIClientConfig",
    "create_openai_client",
    "QueryProcessor",
    "QueryNormalizer",
    "QueryExpander",
    "QueryRewriter",
    "QueryTranslator",
    "QueryDecomposer",
    "IntentDetector",
]
