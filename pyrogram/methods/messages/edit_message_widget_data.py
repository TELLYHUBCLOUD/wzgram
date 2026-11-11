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
from pyrogram import raw, types

log = logging.getLogger(__name__)


class EditMessageWidgetData:
    async def edit_message_widget_data(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        public_data: Optional[str] = None,
        chat_data: Optional[str] = None
    ) -> "types.Message":
        """Update the data of an HTML widget in place, keeping its dynamic UI up to date.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the message the widget is attached to.

            public_data (``str``, *optional*):
                New public data shown by the widget to everyone.

            chat_data (``str``, *optional*):
                New data of the widget specific to the chat the message belongs to.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited widget message is returned.

        Example:
            .. code-block:: python

                await app.edit_message_widget_data(
                    chat_id, message_id,
                    public_data='{"score": 100}'
                )
        """
        r = await self.invoke(
            raw.functions.messages.EditMessageWidgetData(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                public_data=public_data,
                chat_data=chat_data
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateEditMessage,
                              raw.types.UpdateEditChannelMessage,
                              raw.types.UpdateBotEditBusinessMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(i, "connection_id", None)
                )
