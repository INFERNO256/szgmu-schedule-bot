"""Integration test: User requests schedule from main menu.

User story:
1. User is already registered and has a group selected
2. Opens main menu (/start)
3. Presses "Get schedule" button (📅 Расписание)
4. Bot fetches schedule and replies with schedule message
5. No DB changes are made
"""

from datetime import date, time
from unittest import mock

import pytest
import pytest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.base import BaseSession
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dialogs import (
    admin_dialog,
    group_selection_dialog,
    main_menu_dialog,
    onboarding_dialog,
    schedule_dialog,
    settings_dialog,
)
from bot.handlers.user import router as user_router
from models.group import Group
from models.lesson import Lesson
from models.speciality import Speciality
from models.subgroup import Subgroup
from models.user import User


@pytest.fixture
def bot_settings(app_settings):
    """Get BotSettings from test configuration."""
    return app_settings.bot


@pytest_asyncio.fixture
async def memory_storage():
    """Provide in-memory FSM storage for tests."""
    return MemoryStorage()


@pytest_asyncio.fixture
async def test_dispatcher(
    di_container: AsyncContainer,
    memory_storage: MemoryStorage,
    message_manager: MockMessageManager,
) -> Dispatcher:
    """Create Dispatcher with all dialogs configured for testing."""
    dp = Dispatcher(storage=memory_storage)
    setup_dishka(di_container, dp)
    setup_dialogs(dp, message_manager=message_manager)
    dp.include_router(user_router)
    dp.include_routers(
        main_menu_dialog,
        onboarding_dialog,
        group_selection_dialog,
        schedule_dialog,
        settings_dialog,
        admin_dialog,
    )
    return dp


@pytest_asyncio.fixture
async def bot_client(
    test_dispatcher: Dispatcher,
) -> BotClient:
    """
    Create BotClient for driving bot interactions in tests.
    BotClient simulates Telegram user interaction.
    """
    session = mock.AsyncMock(spec=BaseSession)
    bot = Bot(token="999:TEST_TOKEN", session=session)

    return BotClient(
        dp=test_dispatcher,
        user_id=123456789,
        chat_id=123456789,
        chat_type="private",
        bot=bot,
    )


@pytest_asyncio.fixture
async def message_manager() -> MockMessageManager:
    """
    Create MockMessageManager for managing messages in tests.
    """
    return MockMessageManager()


@pytest.fixture
def test_user_data() -> dict:
    """Provide test user data."""
    return {
        "telegram_id": 123456789,
        "username": "testuser",
        "full_name": "Test User",
    }


@pytest.fixture
def test_group_data() -> dict:
    """Provide test group data."""
    return {
        "course_number": 1,
        "stream": "1",
        "name": "G001",
    }


@pytest.fixture
def test_subgroup_data() -> dict:
    """Provide test subgroup data."""
    return {
        "name": "Подгруппа 1",
    }


@pytest.fixture
def test_lesson_data() -> dict:
    """Provide test lesson data."""
    return {
        "subject": "Математика",
        "lesson_type": "лекционного",
        "date": date.today(),
        "start_time": time(9, 0),
        "end_time": time(10, 30),
        "room": "101",
        "teacher": "Проф. Иванов",
    }


@pytest_asyncio.fixture
async def setup_test_data(
    setup_db_schema,  # Ensure schema is created first
    async_session: AsyncSession,
    test_user_data: dict,
    test_group_data: dict,
    test_subgroup_data: dict,
    test_lesson_data: dict,
):
    """
    Setup test data: user + group + lessons.
    Creates all necessary DB records for the test scenario.
    """
    # Create speciality (required for group)
    speciality = Speciality(
        code="CS001",
        full_name="Computer Science",
        clean_name="CS",
    )
    async_session.add(speciality)
    await async_session.flush()

    # Create group
    group = Group(
        speciality_id=speciality.id,
        **test_group_data,
    )
    async_session.add(group)
    await async_session.flush()

    # Create subgroup
    subgroup = Subgroup(
        group_id=group.id,
        **test_subgroup_data,
    )
    async_session.add(subgroup)
    await async_session.flush()

    # Create user with assigned subgroup
    user = User(
        subgroup_id=subgroup.id,
        **test_user_data,
        is_subscribed=False,
    )
    async_session.add(user)
    await async_session.flush()

    # Create lesson for the subgroup
    lesson = Lesson(
        subgroup_id=subgroup.id,
        **test_lesson_data,
    )
    async_session.add(lesson)
    await async_session.flush()

    return {
        "user": user,
        "group": group,
        "subgroup": subgroup,
        "lesson": lesson,
        "speciality": speciality,
    }


@pytest.mark.asyncio
async def test_user_gets_schedule(
    setup_test_data: dict,
    bot_client: BotClient,
    async_session: AsyncSession,
    message_manager: MockMessageManager,
):
    """User story: User requests schedule from main menu and views it."""
    user = setup_test_data["user"]
    lesson = setup_test_data["lesson"]
    test_user_id = 123456789
    await bot_client.send("/start")

    message = message_manager.one_message()
    assert "Главное меню" in message.text
    assert message.reply_markup
    message_manager.reset_history()

    await bot_client.click(message=message, locator=InlineButtonTextLocator(regex=".*Расписание"))

    message = message_manager.one_message()
    assert lesson.subject in message.text
    assert "Лекция" in message.text or "лекция" in message.text.lower()
    assert lesson.room in message.text

    db_user = await async_session.get(User, test_user_id)
    assert db_user is not None
    assert db_user.subgroup_id == user.subgroup_id

    db_lesson = await async_session.get(Lesson, lesson.id)
    assert db_lesson is not None
    assert db_lesson.subject == lesson.subject
