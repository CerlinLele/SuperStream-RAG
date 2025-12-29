"""Extract SuperStream Glossary from HTML and Save as JSON."""

import argparse
import json
from pathlib import Path

from ingest.glossary_extractor import GlossaryExtractor
from config import GLOSSARY_OUTPUT_DIR


def extract_glossary_from_html(
    html_path: Path,
    output_name: str = "superstream_glossary",
    output_dir: Path = None
) -> None:
    """
    Extract glossary terms from HTML file and save as JSON.

    Args:
        html_path: Path to HTML glossary file.
        output_name: Name for output JSON file (without .json extension).
        output_dir: Directory to save JSON file (defaults to GLOSSARY_OUTPUT_DIR).
    """
    if output_dir is None:
        output_dir = GLOSSARY_OUTPUT_DIR

    print("=" * 70)
    print("SuperStream Glossary Extraction - HTML to JSON")
    print("=" * 70)

    print(f"\n[Input]  HTML file: {html_path}")
    print(f"[Output] JSON file: {output_dir / f'{output_name}.json'}")

    # Create glossary extractor
    extractor = GlossaryExtractor(output_dir=output_dir)

    try:
        # Extract glossary from HTML
        print("\n[Step 1] Extracting glossary terms from HTML...")
        result = extractor.extract_from_html(html_path)

        if result["count"] == 0:
            print("[WARNING] No glossary terms found in HTML file.")
            return

        print(f"[SUCCESS] Found {result['count']} glossary terms")

        # Save as JSON
        print("\n[Step 2] Saving glossary as JSON...")
        output_path = extractor.save_glossary_json(result["terms"], output_name)

        # Display statistics
        print("\n" + "=" * 70)
        print("[SUCCESS] Glossary extraction completed successfully!")
        print("=" * 70)
        print(f"\nStatistics:")
        print(f"  Total terms extracted: {result['count']}")
        print(f"  Output file: {output_path}")
        print(f"  File size: {output_path.stat().st_size / 1024:.2f} KB")

        # Display first few terms as sample
        print(f"\nFirst 5 terms:")
        for i, (term, definition) in enumerate(list(result["terms"].items())[:5], 1):
            term_display = term[:50] if len(term) > 50 else term
            def_display = definition[:70] if len(definition) > 70 else definition
            print(f"  {i}. {term_display}")
            print(f"     -> {def_display}...")

    except FileNotFoundError as e:
        print(f"\n[ERROR] HTML file not found - {e}")
        raise
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        raise
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        raise


def extract_all_glossaries(source_dir: Path, output_dir: Path = None) -> None:
    """
    Extract all HTML glossary files from a directory.

    Args:
        source_dir: Directory containing HTML glossary files.
        output_dir: Directory to save JSON files (defaults to GLOSSARY_OUTPUT_DIR).
    """
    if output_dir is None:
        output_dir = GLOSSARY_OUTPUT_DIR

    print("=" * 70)
    print("SuperStream Glossary Extraction - Batch Processing")
    print("=" * 70)
    print(f"\n[Source] Directory: {source_dir}")
    print(f"[Output] Directory: {output_dir}")

    # Find all HTML files
    html_files = list(source_dir.rglob("*.html"))

    if not html_files:
        print(f"\n[WARNING] No HTML files found in {source_dir}")
        return

    print(f"\nFound {len(html_files)} HTML file(s)")

    # Create glossary extractor
    extractor = GlossaryExtractor(output_dir=output_dir)

    total_terms = 0
    successful = 0

    for idx, html_file in enumerate(html_files, 1):
        print(f"\n[{idx}/{len(html_files)}] Processing: {html_file.name}")

        try:
            # Extract glossary
            result = extractor.extract_from_html(html_file)

            if result["count"] > 0:
                # Save JSON with file stem as name
                output_name = html_file.stem
                extractor.save_glossary_json(result["terms"], output_name)

                total_terms += result["count"]
                successful += 1

                print(f"  [SUCCESS] Extracted {result['count']} terms")
            else:
                print(f"  [WARNING] No terms found")

        except Exception as e:
            print(f"  [ERROR] {e}")

    # Summary
    print("\n" + "=" * 70)
    print(f"[SUCCESS] Batch extraction completed!")
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  Files processed: {successful}/{len(html_files)}")
    print(f"  Total terms extracted: {total_terms}")
    print(f"  Output directory: {output_dir}")


def main():
    """Main entry point for glossary extraction."""
    parser = argparse.ArgumentParser(
        description="Extract SuperStream glossary from HTML and save as JSON"
    )

    # Create subparsers for different operations
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Single file extraction
    single_parser = subparsers.add_parser("single", help="Extract single HTML file")
    single_parser.add_argument(
        "html_file",
        type=Path,
        help="Path to HTML glossary file"
    )
    single_parser.add_argument(
        "--output-name",
        type=str,
        default="superstream_glossary",
        help="Output JSON file name (without .json extension)"
    )
    single_parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for JSON file"
    )

    # Batch extraction
    batch_parser = subparsers.add_parser("batch", help="Extract all HTML files from directory")
    batch_parser.add_argument(
        "source_dir",
        type=Path,
        help="Directory containing HTML glossary files"
    )
    batch_parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for JSON files"
    )

    args = parser.parse_args()

    # Execute command
    if args.command == "single":
        extract_glossary_from_html(
            html_path=args.html_file,
            output_name=args.output_name,
            output_dir=args.output_dir
        )
    elif args.command == "batch":
        extract_all_glossaries(
            source_dir=args.source_dir,
            output_dir=args.output_dir
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
