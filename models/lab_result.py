"""Data models for lab results."""

from dataclasses import dataclass
from .enums import RiskLevel

@dataclass
class LabResult:
    """Represents a single lab test result."""
    test_name: str
    value: float
    unit: str
    reference_range: str
    status: RiskLevel
    description: str

    def __str__(self) -> str:
        return f"{self.test_name}: {self.value} {self.unit} ({self.status.value})"

    def is_abnormal(self) -> bool:
        """Check if the result is outside normal range."""
        return self.status in [RiskLevel.HIGH, RiskLevel.LOW, RiskLevel.CRITICAL]

    def get_status_emoji(self) -> str:
        """Get emoji representation of status."""
        status_emojis = {
            RiskLevel.NORMAL: "✅",
            RiskLevel.BORDERLINE: "⚠️",
            RiskLevel.HIGH: "🔴",
            RiskLevel.LOW: "🔵",
            RiskLevel.CRITICAL: "🚨"
        }
        return status_emojis.get(self.status, "❓")