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

log = logging.getLogger(__name__)


async def _as_input_user(client: "pyrogram.Client", bot_id: Union[int, str]) -> "raw.base.InputUser":
    peer = await client.resolve_peer(bot_id)

    if isinstance(peer, raw.types.InputPeerSelf):
        return raw.types.InputUserSelf()

    if isinstance(peer, raw.types.InputPeerUser):
        return raw.types.InputUser(user_id=peer.user_id, access_hash=peer.access_hash)

    raise ValueError("bot_id must point to a user (a bot), not to a chat or a channel")


class AddBotUsername:
    async def add_bot_username(
        self: "pyrogram.Client",
        username: str,
        bot_id: Optional[Union[int, str]] = None,
    ) -> bool:
        """Give a bot an additional username.

        A premium user can give up to two of their bots secondary usernames ending
        in *agent*, *ai*, *app*, *game* or *gay*.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            username (``str``):
                Username to attach, without the leading "@".

            bot_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the bot to change.
                Defaults to the current bot ("me").

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.add_bot_username("my_helper_agent", bot_id="@MyHelperBot")
        """
        return await self.invoke(
            raw.functions.bots.AddUsername(
                bot=await _as_input_user(self, "me" if bot_id is None else bot_id),
                username=username.lstrip("@")
            )
        )
