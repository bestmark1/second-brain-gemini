"""Handler for /do command - arbitrary Gemini requests."""

import asyncio
import logging

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from d_brain.bot.formatters import format_process_report
from d_brain.bot.states import DoCommandState
from d_brain.config import get_settings
from d_brain.services.processor import GeminiProcessor
from d_brain.services.transcription import DeepgramTranscriber

router = Router(name="do")
logger = logging.getLogger(__name__)


@router.message(Command("do"))
async def cmd_do(message: Message, command: CommandObject, state: FSMContext) -> None:
    """Handle /do command."""
    user_id = message.from_user.id if message.from_user else 0

    # Check for inline text: /do move overdue tasks
    if command.args:
        await process_request(message, command.args, user_id)
        return

    # Otherwise, wait for next message
    await state.set_state(DoCommandState.waiting_for_input)
    await message.answer(
        "🎯 <b>Что сделать?</b>\n\n"
        "Отправь голосовое или текстовое сообщение с запросом."
    )


@router.message(DoCommandState.waiting_for_input)
async def handle_do_input(message: Message, bot: Bot, state: FSMContext) -> None:
    """Handle voice/text input after /do command."""
    await state.clear()  # Clear state immediately

    prompt = None

    # Handle voice input
    if message.voice:
        await message.chat.do(action="typing")
        settings = get_settings()
        transcriber = DeepgramTranscriber(settings.deepgram_api_key)

        try:
            file = await bot.get_file(message.voice.file_id)
            if not file.file_path:
                await message.answer("❌ Не удалось скачать голосовое")
                return

            file_bytes = await bot.download_file(file.file_path)
            if not file_bytes:
                await message.answer("❌ Не удалось скачать голосовое")
                return

            audio_bytes = file_bytes.read()
            prompt = await transcriber.transcribe(audio_bytes)
        except Exception as e:
            logger.exception("Failed to transcribe voice for /do")
            await message.answer(f"❌ Не удалось транскрибировать: {e}")
            return

        if not prompt:
            await message.answer("❌ Не удалось распознать речь")
            return

        # Echo transcription to user
        await message.answer(f"🎤 <i>{prompt}</i>")

    # Handle text input
    elif message.text:
        prompt = message.text

    else:
        await message.answer("❌ Отправь текст или голосовое сообщение")
        return

    user_id = message.from_user.id if message.from_user else 0
    await process_request(message, prompt, user_id)


async def process_request(message: Message, prompt: str, user_id: int = 0) -> None:
    """Process the user's request with Gemini."""
    status_msg = await message.answer("⏳ Выполняю...")

    settings = get_settings()
    processor = GeminiProcessor(settings.vault_path, settings.todoist_api_key)

    async def run_with_progress() -> dict:
        task = asyncio.create_task(
            asyncio.to_thread(processor.execute_prompt, prompt, user_id)
        )

        elapsed = 0
        while not task.done():
            await asyncio.sleep(30)
            elapsed += 30
            if not task.done():
                try:
                    await status_msg.edit_text(
                        f"⏳ Выполняю... ({elapsed // 60}m {elapsed % 60}s)"
                    )
                except Exception:
                    pass

        return await task

    report = await run_with_progress()

    formatted = format_process_report(report)
    try:
        await status_msg.edit_text(formatted)
    except Exception:
        # Fallback: send without HTML parsing
        await status_msg.edit_text(formatted, parse_mode=None)
