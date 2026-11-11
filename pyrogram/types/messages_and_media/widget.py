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

from typing import Optional

import pyrogram
from pyrogram import raw

from ..object import Object


class Widget(Object):
    """An HTML widget attached to a message.

    Widgets are custom, dynamic interfaces rendered right inside message bubbles,
    giving bots and AI agents a canvas for interactive tools, games and workflows.

    Parameters:
        width (``int``):
            Width of the widget viewport, in device-independent pixels.

        height (``int``):
            Height of the widget viewport, in device-independent pixels.

        payload (``bytes``):
            Opaque payload the widget was sent with, as passed by the bot.

        is_copy (``bool``, *optional*):
            True, if the widget is a copy of a widget sent through the inline mode.

        can_query (``bool``, *optional*):
            True, if the widget is allowed to send queries to the bot.

        background_query (``bool``, *optional*):
            True, if the widget may send queries without a direct user action.

        public_data (``str``, *optional*):
            Public data currently shown by the widget.

        public_data_hash (``int``, *optional*):
            Hash of the current public data, usable with
            :meth:`~pyrogram.Client.get_widget_public_data` to avoid refetching unchanged data.

        chat_data (``str``, *optional*):
            Per-chat data shown by the widget.

        widget_id (``int``, *optional*):
            Identifier of the shared widget this message renders, if it renders one.
    """

    def __init__(
        self,
        *,
        width: int,
        height: int,
        payload: bytes,
        is_copy: Optional[bool] = None,
        can_query: Optional[bool] = None,
        background_query: Optional[bool] = None,
        public_data: Optional[str] = None,
        public_data_hash: Optional[int] = None,
        chat_data: Optional[str] = None,
        widget_id: Optional[int] = None
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.payload = payload
        self.is_copy = is_copy
        self.can_query = can_query
        self.background_query = background_query
        self.public_data = public_data
        self.public_data_hash = public_data_hash
        self.chat_data = chat_data
        self.widget_id = widget_id

    @staticmethod
    def _parse(client: "pyrogram.Client", media: "raw.types.MessageMediaWidget") -> "Widget":
        return Widget(
            width=media.width,
            height=media.height,
            payload=media.payload,
            is_copy=media.is_copy,
            can_query=media.can_query,
            background_query=media.background_query,
            public_data=media.public_data,
            public_data_hash=media.public_data_hash,
            chat_data=media.chat_data,
            widget_id=media.widget_id
        )
