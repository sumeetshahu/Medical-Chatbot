"""Main chatbot service with OpenAI integration."""

import openai
import logging
from typing import List, Dict
from openai._exceptions import AuthenticationError, RateLimitError

from models import LabResult, RiskLevel
from config.settings import OPENAI_CONFIG, SYSTEM_PROMPT
from .security import SecurityManager

logger = logging.getLogger(__name__)


class MedicalChatbot:
    """Main chatbot class with OpenAI integration."""

    def __init__(self, api_key: str):
        """Initialize the chatbot with OpenAI API key."""
        if not api_key:
            raise ValueError("OpenAI API key is required")

        # openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        self.security = SecurityManager()
        self.config = OPENAI_CONFIG
        self.system_prompt = SYSTEM_PROMPT

        logger.info("Medical chatbot initialized successfully")

    def generate_context(self, lab_results: List[LabResult]) -> str:
        """Generate context from lab results for the AI."""
        if not lab_results:
            return "No lab results available."

        context = "Patient Lab Results:\n\n"

        for result in lab_results:
            status_emoji = result.get_status_emoji()
            context += (
                f"{status_emoji} {result.test_name}: {result.value} {result.unit} "
                f"(Reference: {result.reference_range}) - Status: {result.status.value}\n"
            )

        return context

    def process_query(self, user_query: str, lab_results: List[LabResult], session_id: str) -> str:
        """Process user query and generate response."""
        try:
            # Validate inputs
            if not user_query.strip():
                return "Please ask a specific question about your lab results."

            if not self.security.validate_session_id(session_id):
                logger.warning("Invalid session ID provided")

            # Sanitize input
            sanitized_query = self.security.sanitize_input(user_query)

            # Generate context
            context = self.generate_context(lab_results)

            # Create messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {sanitized_query}"}
            ]

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )

            ai_response = response.choices[0].message.content.strip()

            # Log interaction
            self.security.log_interaction(session_id, "medical_query", "successful_response")

            return ai_response

        except AuthenticationError:
            logger.error("OpenAI authentication failed")
            return "Authentication error. Please check your API key."

        except RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            return "Service temporarily unavailable due to high demand. Please try again later."

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return ("I apologize, but I'm experiencing technical difficulties. "
                    "Please try again later or consult your healthcare provider directly.")

    def get_quick_insights(self, lab_results: List[LabResult]) -> Dict[str, int]:
        """Generate quick insights about lab results."""
        if not lab_results:
            return {'normal': 0, 'borderline': 0, 'abnormal': 0, 'critical': 0}

        insights = {
            'normal': 0,
            'borderline': 0,
            'abnormal': 0,
            'critical': 0
        }

        for result in lab_results:
            if result.status == RiskLevel.NORMAL:
                insights['normal'] += 1
            elif result.status == RiskLevel.BORDERLINE:
                insights['borderline'] += 1
            elif result.status in [RiskLevel.HIGH, RiskLevel.LOW]:
                insights['abnormal'] += 1
            elif result.status == RiskLevel.CRITICAL:
                insights['critical'] += 1

        return insights

    def get_suggested_questions(self) -> List[str]:
        """Get list of suggested questions for users."""
        return [
            "What do my cholesterol levels mean?",
            "Are any of my results concerning?",
            "What lifestyle changes should I consider?",
            "Which tests are outside the normal range?",
            "What does my blood sugar level indicate?",
            "How are my kidney function tests?",
            "What do my blood count results show?",
            "Should I be worried about any results?"
        ]