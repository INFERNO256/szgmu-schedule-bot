from aiogram.filters import BaseFilter
from aiogram.types import Update


class IsAdminFilter(BaseFilter):
    """Filter to check if user is admin."""

    ADMIN_IDS = set()

    def __init__(self, admin_ids: list[int] | None = None):
        super().__init__()
        if admin_ids:
            self.ADMIN_IDS = set(admin_ids)

    async def __call__(self, update: Update) -> bool:
        user_id = None

        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id

        return user_id in self.ADMIN_IDS if user_id else False
