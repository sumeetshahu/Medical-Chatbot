"""Medical report parsing and interpretation service."""

from typing import List
import logging

from models import LabResult, RiskLevel
from config.settings import REFERENCE_RANGES, TEST_DESCRIPTIONS, SAMPLE_LAB_DATA

logger = logging.getLogger(__name__)


class MedicalReportParser:
    """Handles parsing and interpretation of medical reports."""

    def __init__(self):
        self.reference_ranges = REFERENCE_RANGES
        self.test_descriptions = TEST_DESCRIPTIONS

    def determine_status(self, test_name: str, value: float) -> RiskLevel:
        """Determine the risk level based on test results."""
        test_key = test_name.lower().replace(' ', '_')

        if test_key not in self.reference_ranges:
            logger.warning(f"No reference range found for test: {test_name}")
            return RiskLevel.NORMAL

        ref = self.reference_ranges[test_key]

        # Critical thresholds (50% below min or 200% above max)
        if value < ref['min'] * 0.5 or value > ref['max'] * 2:
            return RiskLevel.CRITICAL

        # High or Low (outside normal range)
        elif value < ref['min'] or value > ref['max']:
            return RiskLevel.HIGH if value > ref['max'] else RiskLevel.LOW

        # Borderline (within 10% of limits)
        elif (value < ref['min'] * 1.1 and value >= ref['min']) or \
                (value > ref['max'] * 0.9 and value <= ref['max']):
            return RiskLevel.BORDERLINE

        # Normal
        else:
            return RiskLevel.NORMAL

    def get_test_description(self, test_name: str) -> str:
        """Get description for lab tests."""
        return self.test_descriptions.get(test_name, 'Lab test result')

    def parse_sample_report(self) -> List[LabResult]:
        """Generate sample lab results for demonstration."""
        results = []

        for name, value, unit, ref_range in SAMPLE_LAB_DATA:
            status = self.determine_status(name, value)
            description = self.get_test_description(name)

            results.append(LabResult(
                test_name=name,
                value=value,
                unit=unit,
                reference_range=ref_range,
                status=status,
                description=description
            ))

        logger.info(f"Generated {len(results)} sample lab results")
        return results

    def parse_uploaded_report(self, file_content: str) -> List[LabResult]:
        """Parse uploaded lab report (placeholder for future implementation)."""
        # TODO: Implement actual file parsing logic
        logger.info("Uploaded report parsing not yet implemented")
        return self.parse_sample_report()