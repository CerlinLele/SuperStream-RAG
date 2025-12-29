"""
Script to extract glossary terms from PDF and create FAISS vector index.

This script supports multiple methods:
1. Extract from PDF tables (for table-based glossaries)
2. Extract from JSON file (for pre-processed glossaries)
3. Extract from text file (for simple text-based glossaries)
"""

import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ingest.glossary_extractor import GlossaryExtractor
from ingest.indexer import IndexBuilder
from config import EMBEDDING_MODEL, EMBEDDING_MODEL_TYPE, DATA_DIR

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


def create_glossary_faiss_index(
    pdf_path: Optional[Path] = None,
    json_path: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    embedding_model: str = EMBEDDING_MODEL,
    index_name: str = "glossary_index"
) -> str:
    """
    Extract glossary from PDF or JSON and create FAISS vector index.

    Args:
        pdf_path: Path to the glossary PDF file.
        json_path: Path to glossary JSON file (alternative to PDF).
        output_dir: Directory to save the FAISS index. Defaults to data/indices.
        embedding_model: Embedding model to use. Defaults to config.EMBEDDING_MODEL.
        index_name: Name for the index (used for saving).

    Returns:
        Path to the saved FAISS index.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If extraction or indexing fails.
    """
    # Set up output directory
    if output_dir is None:
        output_dir = DATA_DIR / "indices"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"SuperStream Glossary to FAISS Index")
    print(f"{'='*60}")

    # Step 1: Extract glossary from source
    print(f"\n[Step 1] Extracting glossary from source...")

    if json_path:
        json_path = Path(json_path)
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")

        import json
        print(f"JSON File: {json_path}")

        with open(json_path, 'r', encoding='utf-8-sig') as f:
            terms_dict = json.load(f)

        # Convert to Document objects
        documents = []
        for term, definition in terms_dict.items():
            from llama_index.core.schema import Document
            doc = Document(
                text=f"{term}: {definition}",
                metadata={
                    "term": term,
                    "definition": definition,
                    "source": "SuperStream Glossary of Terms",
                    "doc_type": "glossary",
                    "last_updated": "2025-12-29",
                    "file_name": json_path.name
                }
            )
            documents.append(doc)

    elif pdf_path:
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        if not HAS_PDFPLUMBER:
            raise ImportError("pdfplumber is required for PDF extraction. Install with: pip install pdfplumber")

        print(f"PDF File: {pdf_path}")

        extractor = GlossaryExtractor()
        extraction_result = extractor.extract_from_file(
            pdf_path=pdf_path,
            source_name="SuperStream Glossary of Terms",
            last_updated="2025-12-24"
        )

        terms_dict = extraction_result["terms"]
        documents = extraction_result["documents"]

    else:
        raise ValueError("Either pdf_path or json_path must be provided")

    terms_count = len(terms_dict)

    if terms_count == 0:
        raise ValueError("No glossary terms found")

    print(f"[OK] Successfully extracted {terms_count} glossary terms")
    print(f"[OK] Created {len(documents)} Document objects")

    # Step 2: Create embeddings and build FAISS index
    print(f"\n[Step 2] Building FAISS vector index...")
    print(f"Embedding Model: {embedding_model}")
    print(f"Model Type: {EMBEDDING_MODEL_TYPE}")

    try:
        index_builder = IndexBuilder(embedding_model=embedding_model)
        vector_index = index_builder.build_index(documents)

        # Save the FAISS index
        index_path = output_dir / index_name
        vector_index.storage_context.persist(str(index_path))

        print(f"[OK] FAISS index built and saved successfully")
        print(f"[OK] Index location: {index_path}")

        # Print summary
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Total Terms Extracted: {terms_count}")
        print(f"Total Documents: {len(documents)}")
        print(f"Embedding Model: {embedding_model}")
        print(f"Index Name: {index_name}")
        print(f"Index Path: {index_path}")
        print(f"{'='*60}\n")

        return str(index_path)

    except Exception as e:
        print(f"[ERROR] Error building index: {e}")
        raise


def main():
    """Main entry point for the script."""
    import json
    from pathlib import Path

    # Try JSON file first (preferred method for this problematic PDF)
    json_path = DATA_DIR / "glossaries" / "glossary.json"

    if json_path.exists():
        print(f"Found pre-existing glossary JSON file, using that...")
        try:
            index_path = create_glossary_faiss_index(
                json_path=json_path,
                embedding_model=EMBEDDING_MODEL,
                index_name="superstream_glossary_index"
            )
            print(f"\n[OK] Script completed successfully!")
            print(f"Index saved at: {index_path}")
            return
        except Exception as e:
            print(f"[ERROR] Error processing JSON: {e}")
            sys.exit(1)

    # # Try PDF if JSON doesn't exist
    # pdf_path = Path(
    #     r"c:\Users\hy120\Downloads\AI project\SuperStream-RAG"
    #     r"\superstream-kb\2-role-based-guides\employers"
    #     r"\SuperStream glossary of terms _ Australian Taxation Office.pdf"
    # )

    # try:
    #     index_path = create_glossary_faiss_index(
    #         pdf_path=pdf_path,
    #         embedding_model=EMBEDDING_MODEL,
    #         index_name="superstream_glossary_index"
    #     )
    #     print(f"\n[OK] Script completed successfully!")
    #     print(f"Index saved at: {index_path}")

    # except FileNotFoundError as e:
    #     print(f"\n[ERROR] Error: {e}")
    #     print(f"\nTip: To use this script, either:")
    #     print(f"  1. Provide a glossary.json file in {json_path}")
    #     print(f"  2. Ensure the PDF file exists at: {pdf_path}")
    #     sys.exit(1)
    # except ValueError as e:
    #     print(f"\n[ERROR] Error: {e}")
    #     print(f"\nThe PDF file appears to be image-based or scanned.")
    #     print(f"Please provide a JSON file with the glossary terms instead.")
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"\n[ERROR] Unexpected error: {e}")
    #     sys.exit(1)


if __name__ == "__main__":
    main()
