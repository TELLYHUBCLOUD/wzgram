#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import Union

import pyrogram
from pyrogram import raw

from .add_bot_username import _as_input_user

log = logging.getLogger(__name__)


class ToggleBotUsername:
    async def toggle_bot_username(
        self: "pyrogram.Client",
        username: str,
        active: bool,
        bot_id: Union[int, str],
    ) -> bool:
        """Activate or deactivate an additional username of a bot.

        Bots can pass "me" or "self" to change their own username.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            username (``str``):
                Username to toggle, without the leading "@".

            active (``bool``):
                Pass True to activate the username, False to deactivate it.

            bot_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the bot to change.
                Pass "me" or "self" only from a bot account.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.toggle_bot_username("my_helper_agent", False, bot_id="@MyHelperBot")
        """
        return await self.invoke(
            raw.functions.bots.ToggleUsername(
                bot=await _as_input_user(self, bot_id),
                username=username.lstrip("@"),
                active=active
            )
        )
