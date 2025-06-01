"""Utility functions for the medical chatbot application."""

import pandas as pd
from typing import List, Callable

from models import LabResult, RiskLevel


def format_lab_results_dataframe(lab_results: List[LabResult]) -> pd.DataFrame:
    """Convert lab results to a formatted pandas DataFrame."""
    if not lab_results:
        return pd.DataFrame()

    results_data = []
    for result in lab_results:
        results_data.append({
            'Test': result.test_name,
            'Value': f"{result.value} {result.unit}",
            'Reference Range': result.reference_range,
            'Status': result.status.value,
            'Description': result.description
        })

    return pd.DataFrame(results_data)


def get_status_color(status: str) -> str:
    """Get background color for status styling."""
    color_map = {
        'Normal': 'background-color: #388E3C',  # Light green
        'Borderline': 'background-color: #FFA000',  # Light yellow
        'High': 'background-color: #D32F2F',  # Light red
        'Low': 'background-color: #D32F2F',  # Light red
        'Critical': 'background-color: #7B1FA2'  # Darker red
    }
    return color_map.get(status, '')


def create_status_styler() -> Callable:
    """Create a styler function for pandas DataFrame."""

    def color_status(val):
        return get_status_color(val)

    return color_status


def get_medical_disclaimer() -> str:
    """Get the standard medical disclaimer text."""
    return """
    ⚠️ **Medical Disclaimer**: This tool is for educational purposes only and does not provide medical advice, 
    diagnosis, or treatment recommendations. Always consult with qualified healthcare professionals 
    for medical concerns and before making any medical decisions.
    """


def get_privacy_notice() -> str:
    """Get the privacy notice text."""
    return """
    🔒 **Privacy Notice**: This application is designed with HIPAA compliance in mind. 
    Your data is not permanently stored and all interactions are processed securely.
    """
