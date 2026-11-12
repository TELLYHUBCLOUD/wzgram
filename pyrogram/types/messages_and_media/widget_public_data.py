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


class WidgetPublicData(Object):
    """The public data currently shown by a widget, as returned by
    :meth:`~pyrogram.Client.get_widget_public_data`.

    Parameters:
        hash (``int``):
            Hash of the public data. Pass it back to
            :meth:`~pyrogram.Client.get_widget_public_data` to be told when it changes
            instead of pulling the same data again.

        period (``int``):
            For how long, in seconds, the data may be cached by the client.

        data (``str``, *optional*):
            The public data itself. Not set when *not_modified* is True.

        not_modified (``bool``, *optional*):
            True, if the passed hash is still current and no data was returned.
    """

    def __init__(
        self,
        *,
        hash: int,
        period: int,
        data: Optional[str] = None,
        not_modified: Optional[bool] = None
    ):
        super().__init__()

        self.hash = hash
        self.period = period
        self.data = data
        self.not_modified = not_modified

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        result: "raw.base.messages.WidgetPublicData",
        current_hash: int = 0
    ) -> "WidgetPublicData":
        if isinstance(result, raw.types.messages.WidgetPublicDataNotModified):
            return WidgetPublicData(
                hash=current_hash,
                period=result.period,
                not_modified=True
            )

        return WidgetPublicData(
            hash=result.hash,
            period=result.period,
            data=result.data,
            not_modified=False
        )
