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
from pyrogram import raw, types

log = logging.getLogger(__name__)


class GetWidgetPublicData:
    async def get_widget_public_data(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        hash: int = 0
    ) -> "types.WidgetPublicData":
        """Get the public data currently shown by a widget attached to a message.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the message the widget is attached to.

            hash (``int``, *optional*):
                Hash of the data last seen, as found on :obj:`~pyrogram.types.Widget`
                (``public_data_hash``) or :obj:`~pyrogram.types.WidgetPublicData` (``hash``).
                When the data did not change, the result has ``not_modified`` set and
                carries no data. Defaults to 0, which always fetches.

        Returns:
            :obj:`~pyrogram.types.WidgetPublicData`: The current public data of the widget.

        Example:
            .. code-block:: python

                data = await app.get_widget_public_data(chat_id, message_id)

                if not data.not_modified:
                    print(data.data)
        """
        r = await self.invoke(
            raw.functions.messages.GetWidgetPublicData(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                hash=hash
            )
        )

        return types.WidgetPublicData._parse(self, r, current_hash=hash)
