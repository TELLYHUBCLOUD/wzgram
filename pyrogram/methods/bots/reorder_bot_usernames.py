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
from typing import List, Optional, Union

import pyrogram
from pyrogram import raw

from .add_bot_username import _as_input_user

log = logging.getLogger(__name__)


class ReorderBotUsernames:
    async def reorder_bot_usernames(
        self: "pyrogram.Client",
        order: List[str],
        bot_id: Optional[Union[int, str]] = None,
    ) -> bool:
        """Reorder the additional usernames of a bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            order (List of ``str``):
                The usernames in their new order, without the leading "@".

            bot_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the bot to change.
                Defaults to the current bot ("me").

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.reorder_bot_usernames(["my_helper_ai", "my_helper_agent"])
        """
        return await self.invoke(
            raw.functions.bots.ReorderUsernames(
                bot=await _as_input_user(self, "me" if bot_id is None else bot_id),
                order=[username.lstrip("@") for username in order]
            )
        )
