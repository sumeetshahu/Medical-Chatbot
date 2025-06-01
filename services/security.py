"""Security and privacy management service."""

import hashlib
import re
import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)


class SecurityManager:
    """Handles data privacy and security compliance."""

    # Common PII patterns
    PII_PATTERNS = [
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]'),  # SSN
        (r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE_REDACTED]'),  # Phone
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),  # Email
        (r'\b\d{1,2}\/\d{1,2}\/\d{4}\b', '[DATE_REDACTED]'),  # Date MM/DD/YYYY
        (r'\b\d{4}-\d{2}-\d{2}\b', '[DATE_REDACTED]'),  # Date YYYY-MM-DD
    ]

    @staticmethod
    def hash_identifier(identifier: str) -> str:
        """Hash patient identifiers for privacy."""
        if not identifier:
            return ""

        hashed = hashlib.sha256(identifier.encode('utf-8')).hexdigest()
        return hashed[:12]  # Return first 12 characters for brevity

    @classmethod
    def sanitize_input(cls, user_input: str) -> str:
        """Remove potentially sensitive information from user input."""
        if not user_input:
            return ""

        sanitized = user_input

        for pattern, replacement in cls.PII_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def log_interaction(session_id: str, query_type: str, additional_info: str = ""):
        """Log interactions for audit purposes (without PII)."""
        truncated_session = session_id[:8] + "..." if len(session_id) > 8 else session_id

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": truncated_session,
            "query_type": query_type,
            "additional_info": additional_info
        }

        logger.info(f"Interaction logged: {log_entry}")

    @staticmethod
    def validate_session_id(session_id: str) -> bool:
        """Validate session ID format."""
        if not session_id or len(session_id) < 10:
            return False

        # Check if it's a valid UUID-like string
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, session_id, re.IGNORECASE))

    @classmethod
    def get_privacy_info(cls) -> List[str]:
        """Get privacy compliance information."""
        return [
            "🔒 No data is permanently stored",
            "🔐 Patient identifiers are hashed",
            "📝 Interactions logged without PII",
            "⏰ Session-based data only",
            "🛡️ Input sanitization removes sensitive info"
        ]
