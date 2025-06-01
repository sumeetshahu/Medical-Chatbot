"""Configuration settings for the medical chatbot application."""

from typing import Dict, Any

# OpenAI Configuration
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 1000,
    "temperature": 0.3
}

# Medical Reference Ranges
REFERENCE_RANGES = {
    'glucose': {'min': 70, 'max': 100, 'unit': 'mg/dL'},
    'hemoglobin': {'min': 12.0, 'max': 16.0, 'unit': 'g/dL'},
    'cholesterol_total': {'min': 0, 'max': 200, 'unit': 'mg/dL'},
    'cholesterol_ldl': {'min': 0, 'max': 100, 'unit': 'mg/dL'},
    'cholesterol_hdl': {'min': 40, 'max': 999, 'unit': 'mg/dL'},
    'triglycerides': {'min': 0, 'max': 150, 'unit': 'mg/dL'},
    'creatinine': {'min': 0.6, 'max': 1.2, 'unit': 'mg/dL'},
    'bun': {'min': 7, 'max': 20, 'unit': 'mg/dL'},
    'white_blood_cells': {'min': 4.0, 'max': 11.0, 'unit': 'K/uL'},
    'red_blood_cells': {'min': 4.2, 'max': 5.4, 'unit': 'M/uL'},
    'platelets': {'min': 150, 'max': 450, 'unit': 'K/uL'},
    'tsh': {'min': 0.4, 'max': 4.0, 'unit': 'mIU/L'},
    'vitamin_d': {'min': 30, 'max': 100, 'unit': 'ng/mL'}
}

# Test Descriptions
TEST_DESCRIPTIONS = {
    'Glucose': 'Measures blood sugar levels',
    'Hemoglobin': 'Protein in red blood cells that carries oxygen',
    'Total Cholesterol': 'Total amount of cholesterol in blood',
    'LDL Cholesterol': 'Low-density lipoprotein (bad cholesterol)',
    'HDL Cholesterol': 'High-density lipoprotein (good cholesterol)',
    'Triglycerides': 'Type of fat found in blood',
    'Creatinine': 'Waste product filtered by kidneys',
    'BUN': 'Blood Urea Nitrogen - kidney function indicator',
    'White Blood Cells': 'Cells that fight infection',
    'Red Blood Cells': 'Cells that carry oxygen',
    'Platelets': 'Cells that help blood clot',
    'TSH': 'Thyroid Stimulating Hormone',
    'Vitamin D': 'Essential vitamin for bone health'
}

# Sample Lab Data
SAMPLE_LAB_DATA = [
    ('Glucose', 95, 'mg/dL', '70-100'),
    ('Hemoglobin', 13.5, 'g/dL', '12.0-16.0'),
    ('Total Cholesterol', 220, 'mg/dL', '<200'),
    ('LDL Cholesterol', 130, 'mg/dL', '<100'),
    ('HDL Cholesterol', 45, 'mg/dL', '>40'),
    ('Triglycerides', 180, 'mg/dL', '<150'),
    ('Creatinine', 1.0, 'mg/dL', '0.6-1.2'),
    ('BUN', 15, 'mg/dL', '7-20'),
    ('White Blood Cells', 7.5, 'K/uL', '4.0-11.0'),
    ('Red Blood Cells', 4.8, 'M/uL', '4.2-5.4'),
    ('Platelets', 250, 'K/uL', '150-450'),
    ('TSH', 2.5, 'mIU/L', '0.4-4.0'),
    ('Vitamin D', 25, 'ng/mL', '30-100')
]

# System Prompt for AI
SYSTEM_PROMPT = """
You are a medical report assistant chatbot designed to help patients understand their lab results. 

IMPORTANT GUIDELINES:
1. Always include medical disclaimers
2. Never provide specific medical advice or diagnoses
3. Encourage consultation with healthcare providers
4. Focus on explaining test results in plain language
5. Be empathetic and supportive
6. If unsure about anything, recommend consulting a doctor

Your role is to:
- Explain what lab tests measure
- Help interpret results in context of reference ranges
- Provide general health information
- Answer questions about lab terminology

Always end responses with: "Please consult your healthcare provider for medical advice and treatment recommendations."
"""

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "Medical Report Assistant",
    "page_icon": "🏥",
    "layout": "wide"
}