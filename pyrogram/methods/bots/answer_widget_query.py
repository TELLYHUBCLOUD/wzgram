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


class AnswerWidgetQuery:
    async def answer_widget_query(
        self: "pyrogram.Client",
        widget_query_id: Union[str, int],
        result: Optional[str] = None
    ) -> bool:
        """Send answers to widget queries sent from HTML widgets.

        The answer is handed back to the widget as the result of its pending query.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            widget_query_id (``str`` | ``int``):
                Unique identifier of the query to be answered, as found on
                :obj:`~pyrogram.types.WidgetQuery`.

            result (``str``, *optional*):
                Data passed back to the widget, as a JSON string.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Answer with data
                await app.answer_widget_query(query.id, result='{"ok": true}')
        """
        return await self.invoke(
            raw.functions.messages.SetBotWidgetQueryAnswer(
                query_id=int(widget_query_id),
                result=result
            )
        )
