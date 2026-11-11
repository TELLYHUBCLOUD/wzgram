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

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class GetUniqueGift:
    async def get_unique_gift(
        self: "pyrogram.Client",
        gift_name: str
    ) -> "types.Gift":
        """Look up a unique gift by its name (slug), simplifying gift integrations.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            gift_name (``str``):
                Name of the unique gift, e.g. *"SignetRing-903"*, or its
                *t.me/nft/* link.

        Returns:
            :obj:`~pyrogram.types.Gift`: Information about the unique gift.

        Example:
            .. code-block:: python

                # Get a unique gift by name
                gift = await app.get_unique_gift("SignetRing-903")

                # ... or by link
                gift = await app.get_unique_gift("https://t.me/nft/SignetRing-903")
        """
        match = self.UPGRADED_GIFT_RE.match(gift_name)

        if match:
            slug = match.group(1)
        elif isinstance(gift_name, str):
            slug = gift_name
        else:
            raise ValueError("Invalid gift name")

        r = await self.invoke(
            raw.functions.payments.GetUniqueStarGift(
                slug=slug.replace(" ", "")
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return await types.Gift._parse(self, r.gift, users=users, chats=chats)
