"""Process command handler."""

import asyncio
import logging
from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from d_brain.bot.formatters import format_process_report
from d_brain.config import get_settings
from d_brain.services.git import VaultGit
from d_brain.services.processor import GeminiProcessor

router = Router(name="process")
logger = logging.getLogger(__name__)


@router.message(Command("process"))
async def cmd_process(message: Message) -> None:
    """Handle /process command - trigger Gemini processing."""
    user_id = message.from_user.id if message.from_user else "unknown"
    logger.info("Process command triggered by user %s", user_id)

    status_msg = await message.answer("⏳ Processing... (may take up to 10 min)")

    settings = get_settings()
    processor = GeminiProcessor(settings.vault_path, settings.todoist_api_key)
    git = VaultGit(settings.vault_path)

    # Run subprocess in thread to avoid blocking event loop
    async def process_with_progress() -> dict:
        task = asyncio.create_task(
            asyncio.to_thread(processor.process_daily, date.today())
        )

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    await status_msg.edit_text(
                        f"⏳ Processing... ({elapsed // 60}m {elapsed % 60}s)"
                    )
                except Exception:
                    pass  # Ignore edit errors

        return await task

    report = await process_with_progress()

    # Commit and push changes
    if "error" not in report:
        today = date.today().isoformat()
        await asyncio.to_thread(git.commit_and_push, f"chore: process daily {today}")

    # Format and send report
    formatted = format_process_report(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        # Fallback: send without HTML parsing
        await status_msg.edit_text(formatted, parse_mode=None)
