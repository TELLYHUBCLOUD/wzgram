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
from typing import Optional, Union

import pyrogram
from pyrogram import raw

from .add_bot_username import _as_input_user

log = logging.getLogger(__name__)


class RemoveBotUsername:
    async def remove_bot_username(
        self: "pyrogram.Client",
        username: str,
        bot_id: Optional[Union[int, str]] = None,
    ) -> bool:
        """Remove an additional username from a bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            username (``str``):
                Username to detach, without the leading "@".

            bot_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the bot to change.
                Defaults to the current bot ("me").

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.remove_bot_username("my_helper_agent", bot_id="@MyHelperBot")
        """
        return await self.invoke(
            raw.functions.bots.RemoveUsername(
                bot=await _as_input_user(self, "me" if bot_id is None else bot_id),
                username=username.lstrip("@")
            )
        )
