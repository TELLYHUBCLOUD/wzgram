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
from pyrogram import raw

log = logging.getLogger(__name__)


class EditWidgetData:
    async def edit_widget_data(
        self: "pyrogram.Client",
        widget_id: int,
        public_data: str,
        cache_time: Optional[int] = None
    ) -> bool:
        """Update the public data of a shared widget from the centralized setting.

        Every message rendering the shared widget is instantly updated.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            widget_id (``int``):
                Identifier of the shared widget, as found on
                :obj:`~pyrogram.types.Widget` (``widget_id``).

            public_data (``str``):
                New public data shown by every rendering of the shared widget.

            cache_time (``int``, *optional*):
                The maximum amount of time in seconds the public data may be cached
                by clients before the update is fetched.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                await app.edit_widget_data(
                    widget_id,
                    public_data='{"status": "ended"}'
                )
        """
        return await self.invoke(
            raw.functions.messages.EditWidgetData(
                widget_id=widget_id,
                public_data=public_data,
                cache_time=cache_time
            )
        )
