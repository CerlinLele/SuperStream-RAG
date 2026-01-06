"""PDF Router - detects document type and routes to appropriate processor."""

import re
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ProcessingPlan:
    """Plan for how to process a PDF document."""

    schedule_type: str  # Schedule_2, Schedule_3, Schedule_4a, etc.
    processor_type: str  # table, text, hybrid
    extractors: List[str]  # Which specialized extractors to use
    description: str  # Human-readable description


class PDFRouter:
    """Routes PDF documents to appropriate processors based on document type."""

    # Mapping of filename patterns to schedule types
    SCHEDULE_PATTERNS = {
        r"Schedule.*2.*Terms.*Definitions": "Schedule_2",
        r"Schedule.*3.*Payment": "Schedule_3",
        r"Schedule.*4a.*Contributions": "Schedule_4a",
        r"Schedule.*4b.*Rollover": "Schedule_4b",
        r"Schedule.*5.*Message": "Schedule_5",
        r"Schedule.*6.*Error": "Schedule_6",
    }

    # Define processing plans for each schedule type
    PROCESSING_PLANS = {
        "Schedule_2": ProcessingPlan(
            schedule_type="Schedule_2",
            processor_type="table",
            extractors=["terminology"],
            description="Terms and Definitions - Simple glossary table",
        ),
        "Schedule_3": ProcessingPlan(
            schedule_type="Schedule_3",
            processor_type="text",
            extractors=[],
            description="Payment Methods - Text-based specifications",
        ),
        "Schedule_4a": ProcessingPlan(
            schedule_type="Schedule_4a",
            processor_type="table",
            extractors=["field_spec"],
            description="Contributions - Complex field specifications (110 pages)",
        ),
        "Schedule_4b": ProcessingPlan(
            schedule_type="Schedule_4b",
            processor_type="table",
            extractors=["field_spec"],
            description="Rollover - Complex field specifications",
        ),
        "Schedule_5": ProcessingPlan(
            schedule_type="Schedule_5",
            processor_type="table",
            extractors=[],
            description="Message Orchestration - Specification tables",
        ),
        "Schedule_6": ProcessingPlan(
            schedule_type="Schedule_6",
            processor_type="hybrid",
            extractors=["error_code", "xml_schema"],
            description="Error Code Management - Tables + XSD code blocks",
        ),
    }

    def detect_schedule_type(self, pdf_path: Path) -> Optional[str]:
        """
        Detect which schedule type the PDF belongs to based on filename.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Schedule type (e.g., 'Schedule_2') or None if not recognized
        """
        filename = pdf_path.name

        for pattern, schedule_type in self.SCHEDULE_PATTERNS.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return schedule_type

        return None

    def route(self, pdf_path: Path) -> Optional[ProcessingPlan]:
        """
        Analyze PDF and return processing plan.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            ProcessingPlan object or None if document type not recognized
        """
        # Step 1: Detect schedule type from filename
        schedule_type = self.detect_schedule_type(pdf_path)

        if schedule_type is None:
            return None

        # Step 2: Return processing plan for this schedule type
        if schedule_type in self.PROCESSING_PLANS:
            return self.PROCESSING_PLANS[schedule_type]

        return None

    def route_batch(self, pdf_paths: List[Path]) -> dict:
        """
        Route multiple PDF files.

        Args:
            pdf_paths: List of paths to PDF files

        Returns:
            Dictionary mapping file paths to ProcessingPlans
        """
        routes = {}

        for pdf_path in pdf_paths:
            plan = self.route(pdf_path)
            routes[pdf_path] = plan

        return routes
