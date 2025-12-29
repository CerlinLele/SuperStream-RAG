"""Glossary Extractor for SuperStream Glossary HTML files."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from llama_index.core.schema import Document

from config import GLOSSARY_OUTPUT_DIR


class GlossaryExtractor:
    """
    Extracts glossary terms and definitions from HTML files.

    Uses BeautifulSoup to extract table-structured data and converts
    term-definition pairs into LlamaIndex Document objects and JSON format.

    Attributes:
        output_dir: Directory to save extracted glossary JSON files.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize glossary extractor.

        Args:
            output_dir: Directory to save glossary JSON files.
                       Defaults to GLOSSARY_OUTPUT_DIR from config.
        """
        self.output_dir = output_dir or GLOSSARY_OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def extract_from_html(
        self,
        html_path: Path,
        source_name: str = "SuperStream Glossary",
        last_updated: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Extract glossary terms from an HTML file.

        Searches for tables in the HTML and extracts term-definition pairs.
        Each pair is converted into a Document with metadata.

        Args:
            html_path: Path to HTML file.
            source_name: Name of the glossary source.
            last_updated: Last update date (YYYY-MM-DD format).

        Returns:
            Dictionary containing extracted terms and Document objects.

        Raises:
            FileNotFoundError: If HTML file does not exist.
            ValueError: If no tables found in HTML.
        """
        terms_dict = {}
        documents = []

        try:
            # Try to open the file with different approaches
            html_content = None

            # First attempt: direct path open
            try:
                with open(str(html_path), 'r', encoding='utf-8') as f:
                    html_content = f.read()
            except (FileNotFoundError, OSError):
                # Second attempt: try relative to current directory
                try:
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                except (FileNotFoundError, OSError):
                    # Final attempt: check if path exists by other means
                    import os
                    if os.path.isfile(str(html_path)):
                        with open(str(html_path), 'r', encoding='utf-8') as f:
                            html_content = f.read()
                    else:
                        raise FileNotFoundError(f"HTML file does not exist: {html_path}")

            if not html_content:
                raise FileNotFoundError(f"Could not read HTML file: {html_path}")

            # Parse HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all tables
            tables = soup.find_all('table')
            if not tables:
                raise ValueError("No tables found in HTML file")

            for table in tables:
                rows = table.find_all('tr')

                # Skip header row (first row)
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])

                    if not cells or len(cells) < 2:
                        continue

                    # Extract text from cells
                    term_cell = cells[0].get_text(strip=True)
                    definition_cell = cells[1].get_text(strip=True)

                    term = term_cell.strip() if term_cell else None
                    definition = definition_cell.strip() if definition_cell else None

                    if not term or not definition:
                        continue

                    # Store in dictionary
                    terms_dict[term] = definition

                    # Create Document object
                    doc = Document(
                        text=f"{term}: {definition}",
                        metadata={
                            "term": term,
                            "definition": definition,
                            "source": source_name,
                            "doc_type": "glossary",
                            "last_updated": last_updated or "2025-08-12",
                            "file_name": html_path.name
                        }
                    )
                    documents.append(doc)

            return {
                "terms": terms_dict,
                "documents": documents,
                "count": len(terms_dict)
            }

        except Exception as e:
            print(f"Error extracting glossary from {html_path}: {e}")
            raise

    def save_glossary_json(
        self,
        terms_dict: Dict[str, str],
        output_name: str
    ) -> Path:
        """
        Save extracted glossary to JSON file.

        Args:
            terms_dict: Dictionary of term-definition pairs.
            output_name: Output file name (without .json extension).

        Returns:
            Path to saved JSON file.
        """
        output_path = self.output_dir / f"{output_name}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(terms_dict, f, ensure_ascii=False, indent=2)

        print(f"Glossary saved to {output_path}")
        return output_path

    def extract_multiple(
        self,
        html_paths: List[Path],
        source_name: str = "SuperStream Glossaries"
    ) -> Dict[str, any]:
        """
        Extract glossaries from multiple HTML files.

        Args:
            html_paths: List of HTML file paths.
            source_name: Name of the glossary source.

        Returns:
            Dictionary with combined terms and documents.
        """
        combined_terms = {}
        combined_documents = []

        for html_path in html_paths:
            result = self.extract_from_html(html_path, source_name)
            combined_terms.update(result["terms"])
            combined_documents.extend(result["documents"])

        return {
            "terms": combined_terms,
            "documents": combined_documents,
            "count": len(combined_terms)
        }
