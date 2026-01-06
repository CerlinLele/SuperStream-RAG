"""
Schedule 2 Processor - Terms and Definitions

Handles PDF extraction using PDFReader (free LlamaIndex reader).
Optimized for Schedule 2's simple 2-3 column glossary table structure.

Processing approach:
1. Detect PDF version (v2.x or v3.x)
2. Route to appropriate version-specific processor
3. Extract text from PDF using PDFReader
4. Parse table structure from extracted text
5. Extract term-definition pairs
6. Create LlamaIndex documents for RAG
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from llama_index.readers.file import PDFReader
from llama_index.core.schema import Document

from ingest.processors.pdf import BaseProcessor
from ingest.processors.pdf.schedule2.version_detector import (
    Schedule2VersionDetector,
    VersionInfo
)


@dataclass
class TermDefinition:
    """Single term and its definition."""

    term: str
    definition: str
    source_page: int
    document_id: str
    data_element_name: Optional[str] = None
    unique_reference_id: Optional[str] = None
    term_legal_reference: Optional[str] = None
    term_version_no: Optional[str] = None


class Schedule2Processor(BaseProcessor):
    """
    Processor for Schedule 2 - Terms and Definitions.

    This processor specializes in extracting terminology from Schedule 2 PDFs.
    It uses LlamaParse to intelligently parse tables and preserve structure.

    Processing strategy:
    1. Detect PDF version (v2.x or v3.x)
    2. Route to appropriate version-specific processor
    3. Use LlamaParse to extract PDF with table awareness
    4. Parse the structured markdown output
    5. Extract term-definition pairs from tables
    6. Create semantic-aware chunks for RAG
    7. Generate searchable text representations
    """

    def __init__(self):
        """
        Initialize Schedule 2 processor with version detection.
        """
        self.parser = PDFReader()
        self.version_detector = Schedule2VersionDetector()
        self.version_info = None

    def process(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Process Schedule 2 PDF and extract terminology.

        Args:
            pdf_path: Path to the Schedule 2 PDF file

        Returns:
            Dictionary containing:
            - raw_content: Text content from PDFReader
            - terms: List of TermDefinition objects
            - documents: List of LlamaIndex Document objects for RAG
            - metadata: Processing metadata
            - version_info: Detected version information
        """
        print(f"Processing Schedule 2: {pdf_path.name}")

        # Step 1: Detect PDF version
        self.version_info = self._detect_version(pdf_path)

        # Step 2: Parse PDF with PDFReader
        raw_content = self._parse_with_pdfreader(pdf_path)

        # Step 3: Extract term-definition pairs
        terms = self._extract_terms(raw_content, pdf_path)

        # Step 4: Create LlamaIndex Documents for RAG
        documents = self._create_documents(terms, pdf_path)

        # Step 5: Generate metadata
        metadata = {
            "source_file": pdf_path.name,
            "schedule_type": "Schedule_2",
            "total_terms": len(terms),
            "processor_type": "schedule2",
            "parsing_method": "pdfreader",
            "version": str(self.version_info),
            "version_major": self.version_info.major,
            "version_minor": self.version_info.minor,
            "version_detected_from": self.version_info.detected_from,
            "version_confidence": self.version_info.confidence,
        }

        return {
            "raw_content": raw_content,
            "terms": terms,
            "documents": documents,
            "metadata": metadata,
            "version_info": self.version_info,
        }

    def _detect_version(self, pdf_path: Path) -> VersionInfo:
        """
        Detect Schedule 2 PDF version.

        Args:
            pdf_path: Path to PDF file

        Returns:
            VersionInfo object with detected version
        """
        print(f"  🔍 Detecting version...")

        # First try filename detection (fast)
        version_info = self.version_detector.detect_from_filename(pdf_path)

        if version_info and version_info.confidence > 0.9:
            self.version_detector.print_detection_info(pdf_path, version_info)
            return version_info

        # If filename detection not confident, we'll do content detection
        # after parsing (to avoid parsing twice)
        print(f"     Filename detection inconclusive, will analyze content...")

        return version_info or VersionInfo(
            major=2,
            minor=1,
            detected_from="default",
            confidence=0.0
        )

    def _parse_with_pdfreader(self, pdf_path: Path) -> str:
        """
        Parse PDF using PDFReader (free LlamaIndex reader).

        PDFReader uses PyPDF library for text extraction.
        Works well for structured documents like glossaries.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Text content extracted from PDF
        """
        print(f"  Parsing with PDFReader...")

        try:
            # PDFReader extracts text from PDF
            documents = self.parser.load_data(pdf_path)

            # Combine all page documents into single text
            if isinstance(documents, list):
                content = "\n\n".join([doc.get_content() for doc in documents])
            else:
                content = documents.get_content()

            print(f"  Successfully parsed {len(documents)} pages")

            # If version detection was inconclusive, try content-based detection
            if self.version_info.confidence < 0.9:
                content_version = self.version_detector.detect_from_content(content)
                if content_version and content_version.confidence > 0.7:
                    self.version_info = content_version
                    self.version_detector.print_detection_info(pdf_path, self.version_info)

            return content

        except Exception as e:
            print(f"  Error parsing PDF: {e}")
            raise

    def _extract_terms(self, content: str, pdf_path: Path) -> List[TermDefinition]:
        """
        Extract term-definition pairs from text content.

        PDFReader returns plain text with structured blocks:
        Business term <TERM_NAME>
        Definition <DEFINITION_TEXT>
        Data element name: ...
        Term legal reference: ...
        Unique reference ID: ...
        Term version no.: ...

        Args:
            content: Text content from PDFReader
            pdf_path: PDF file path (for document_id)

        Returns:
            List of TermDefinition objects
        """
        print(f"  Extracting terms from content...")

        terms = []
        document_id = pdf_path.stem
        lines = content.split("\n")
        current_page = 1

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Track page markers (e.g., "PAGE 5 OF 23")
            if "PAGE" in line and any(c.isdigit() for c in line):
                try:
                    page_match = re.search(r'PAGE\s+(\d+)', line, re.IGNORECASE)
                    if page_match:
                        current_page = int(page_match.group(1))
                except:
                    pass
                i += 1
                continue

            # Look for "Business term" marker
            if line.startswith("Business term "):
                term_name = line.replace("Business term ", "").strip()

                # Initialize metadata fields
                definition_text = ""
                data_element_name = None
                term_legal_reference = None
                unique_reference_id = None
                term_version_no = None

                j = i + 1

                # Scan for Definition line and metadata
                while j < len(lines):
                    next_line = lines[j].strip()

                    # Extract Definition
                    if next_line.startswith("Definition "):
                        definition_text = next_line.replace("Definition ", "").strip()
                        # Collect continuation lines of definition (until we hit another field)
                        k = j + 1
                        while k < len(lines):
                            potential_def_line = lines[k].strip()
                            # Stop if we hit a metadata field or empty line
                            if (potential_def_line.startswith("Data element name:") or
                                potential_def_line.startswith("Term legal reference:") or
                                potential_def_line.startswith("Unique reference ID:") or
                                potential_def_line.startswith("Term version no.:") or
                                not potential_def_line):
                                break
                            # Continue accumulating definition text
                            if potential_def_line:
                                definition_text += " " + potential_def_line
                            k += 1

                    # Extract Data element name (may also contain Term legal reference on same line)
                    elif next_line.startswith("Data element name:"):
                        # Could be: "Data element name: XXX Term legal reference: YYY"
                        if "Term legal reference:" in next_line:
                            parts = next_line.split("Term legal reference:", 1)
                            data_element_name = parts[0].replace("Data element name:", "").strip()
                            term_legal_reference = parts[1].strip()
                        else:
                            data_element_name = next_line.replace("Data element name:", "").strip()

                    # Extract Term legal reference (if it appears alone on a line)
                    elif next_line.startswith("Term legal reference:"):
                        term_legal_reference = next_line.replace("Term legal reference:", "").strip()

                    # Extract Unique reference ID (may also contain Term version no. on same line)
                    elif next_line.startswith("Unique reference ID:"):
                        # Could be: "Unique reference ID: XXX Term version no.: YYY"
                        if "Term version no.:" in next_line:
                            parts = next_line.split("Term version no.:", 1)
                            unique_reference_id = parts[0].replace("Unique reference ID:", "").strip()
                            term_version_no = parts[1].strip()
                        else:
                            unique_reference_id = next_line.replace("Unique reference ID:", "").strip()

                    # Extract Term version no. (if it appears alone on a line)
                    elif next_line.startswith("Term version no.:"):
                        term_version_no = next_line.replace("Term version no.:", "").strip()

                    # Stop when we hit the next Business term block
                    elif next_line.startswith("Business term "):
                        break

                    j += 1

                # Validate and create term
                if term_name and definition_text:
                    definition_text = definition_text.strip()
                    # Apply filters: reasonable length for both term and definition
                    if len(term_name) < 200 and len(term_name.split()) <= 20:
                        term_obj = TermDefinition(
                            term=term_name,
                            definition=definition_text,
                            source_page=current_page,
                            document_id=document_id,
                            data_element_name=data_element_name if data_element_name else None,
                            term_legal_reference=term_legal_reference if term_legal_reference else None,
                            unique_reference_id=unique_reference_id if unique_reference_id else None,
                            term_version_no=term_version_no if term_version_no else None,
                        )
                        terms.append(term_obj)

            i += 1

        print(f"  Extracted {len(terms)} terms")
        return terms

    def _create_documents(
        self, terms: List[TermDefinition], pdf_path: Path
    ) -> List[Document]:
        """
        Create LlamaIndex Document objects from terms.

        Strategy:
        1. Each term becomes a separate document for fine-grained retrieval
        2. Create semantic-aware text combining term and definition
        3. Add rich metadata for filtering and context
        4. Group by sections for batch operations

        Args:
            terms: List of TermDefinition objects
            pdf_path: PDF file path

        Returns:
            List of LlamaIndex Document objects
        """
        print(f"  Creating LlamaIndex documents...")

        documents = []

        for idx, term_obj in enumerate(terms):
            # Create searchable text combining term and definition
            # This helps with semantic search
            text = self._create_searchable_text(term_obj)

            # Create metadata for filtering and context
            metadata = {
                "doc_type": "terminology",
                "schedule_type": "Schedule_2",
                "term": term_obj.term,
                "source_file": pdf_path.name,
                "page_num": term_obj.source_page,
                "document_id": term_obj.document_id,
                "is_definition": True,
                "version": str(self.version_info),
                "version_major": self.version_info.major,
                "version_minor": self.version_info.minor,
            }

            # Create LlamaIndex Document
            doc = Document(
                text=text,
                metadata=metadata,
                doc_id=f"schedule2_{term_obj.document_id}_{idx}",
            )

            documents.append(doc)

        print(f"  Created {len(documents)} LlamaIndex documents")
        return documents

    def get_processor_type(self) -> str:
        """
        Get processor type based on detected version.

        Returns:
            Processor type string: 'schedule2_v2' or 'schedule2_v3'
        """
        if self.version_info:
            return self.version_detector.get_processor_type(self.version_info)
        return 'schedule2_v2'

    def get_version_info(self) -> Optional[VersionInfo]:
        """
        Get detected version information.

        Returns:
            VersionInfo object or None
        """
        return self.version_info

    def _create_searchable_text(self, term_obj: TermDefinition) -> str:
        """
        Create semantic-aware text for the term.

        Combines term and definition in natural language style
        to improve semantic search relevance.

        Example output:
        "APRA is defined as: Australian Prudential Regulation Authority.
         This is a key term in the SuperStream framework."

        Args:
            term_obj: TermDefinition object

        Returns:
            Searchable text string
        """
        text_parts = [
            f'The term "{term_obj.term}" is defined as:',
            term_obj.definition,
            f"This definition is from {term_obj.document_id} on page {term_obj.source_page}.",
        ]

        return " ".join(text_parts)

    def save_extracted_data(
        self, processed_data: Dict[str, Any], output_dir: Path
    ) -> None:
        """
        Save extracted terminology data to JSON and CSV.

        Useful for:
        1. Standalone glossary reference
        2. Integration with other tools
        3. Data validation and review
        4. Backup of extracted data

        Args:
            processed_data: Dictionary from process() method
            output_dir: Directory to save extracted data
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save as JSON (structured)
        terms = processed_data["terms"]
        terms_dict = {term.term: term.definition for term in terms}

        json_file = output_dir / "schedule_2_glossary.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(terms_dict, f, ensure_ascii=False, indent=2)
        print(f"  Saved glossary to {json_file}")

        # Save as CSV (spreadsheet format)
        try:
            import csv

            csv_file = output_dir / "schedule_2_glossary.csv"
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["term", "definition", "page"]
                )
                writer.writeheader()
                for term in terms:
                    writer.writerow({
                        "term": term.term,
                        "definition": term.definition,
                        "page": term.source_page,
                    })
            print(f"  Saved glossary to {csv_file}")
        except ImportError:
            print("  (CSV export requires csv module)")

    def export_llm_context(self, terms: List[TermDefinition]) -> str:
        """
        Export terms in a format useful for LLM context.

        Used when feeding the glossary to an LLM for
        context-aware responses about SuperStream terms.

        Args:
            terms: List of TermDefinition objects

        Returns:
            Formatted string for LLM context
        """
        lines = ["# SuperStream Glossary\n"]

        for term in terms:
            lines.append(f"## {term.term}\n")
            lines.append(f"{term.definition}\n")

        return "\n".join(lines)
