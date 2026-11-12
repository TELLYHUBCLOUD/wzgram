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
from typing import Optional

import pyrogram
from pyrogram import raw, utils

log = logging.getLogger(__name__)


class EditInlineWidgetData:
    async def edit_inline_widget_data(
        self: "pyrogram.Client",
        inline_message_id: str,
        public_data: Optional[str] = None,
        chat_data: Optional[str] = None
    ) -> bool:
        """Update the data of an HTML widget attached to an inline message in place.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message the widget is attached to.

            public_data (``str``, *optional*):
                New public data shown by the widget to everyone.

            chat_data (``str``, *optional*):
                New data of the widget specific to the chat the message belongs to.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.edit_inline_widget_data(
                    inline_message_id,
                    public_data='{"score": 100}'
                )
        """
        return await self.invoke(
            raw.functions.messages.EditInlineBotMessageWidgetData(
                id=utils.unpack_inline_message_id(inline_message_id),
                public_data=public_data,
                chat_data=chat_data
            )
        )
