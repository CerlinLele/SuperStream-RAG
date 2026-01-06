"""Base processor class for PDF processing pipeline."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseProcessor(ABC):
    """Abstract base class for PDF content processors."""

    @abstractmethod
    def process(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Process PDF and return structured data.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing extracted content and metadata
        """
        pass
