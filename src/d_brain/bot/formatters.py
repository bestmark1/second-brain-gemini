"""Report formatters for Telegram messages."""

import html
import re
from typing import Any


def to_readable_text(text: str) -> str:
    """Convert mixed HTML/plain text into readable plain text for Telegram."""
    if not text:
        return ""

    # HTML -> plain line structure
    text = re.sub(r"<br\\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?(ul|ol|p|div)\\b[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li\\b[^>]*>", "- ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)

    # Strip inline formatting tags
    text = re.sub(r"</?(b|i|u|code|pre|a)\\b[^>]*>", "", text, flags=re.IGNORECASE)

    # Remove parentheses as requested
    text = text.replace("(", " ").replace(")", "")

    # Normalize whitespace/newlines
    text = re.sub(r"[ \\t]+", " ", text)
    text = re.sub(r"\\n{3,}", "\\n\\n", text).strip()

    return text


def format_process_report(report: dict[str, Any]) -> str:
    """Format processing report for Telegram."""
    if "error" in report:
        error_msg = html.escape(str(report["error"]))
        return f"Ошибка: {error_msg}"

    if "report" in report:
        raw_report = str(report["report"])
        return to_readable_text(raw_report)

    return "Обработка завершена"


def format_error(error: str) -> str:
    """Format error message for Telegram."""
    return f"Ошибка: {html.escape(error)}"


def format_empty_daily() -> str:
    """Format message for empty daily file."""
    return (
        "Нет записей для обработки\n\n"
        "Добавьте голосовые сообщения или текст в течение дня"
    )
