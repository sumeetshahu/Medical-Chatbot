"""Enumerations for the medical chatbot application."""

from enum import Enum

class RiskLevel(Enum):
    """Risk levels for lab test results."""
    NORMAL = "Normal"
    BORDERLINE = "Borderline"
    HIGH = "High"
    LOW = "Low"
    CRITICAL = "Critical"