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

from typing import List, Optional

import pyrogram
from pyrogram import raw, types


class SetCardStickers:
    async def set_card_stickers(
        self: "pyrogram.Client",
        stickers: List["types.WalletCardSticker"],
        bg_nft_address: Optional[str] = None,
    ) -> "types.WalletCard":
        """Set the NFT stickers of your TON wallet card.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            stickers (List of :obj:`~pyrogram.types.WalletCardSticker`):
                The stickers to place on the card, each referenced by its NFT address
                together with the position on the card (x, y, width, height and rotation
                in percent, may exceed 100).

            bg_nft_address (``str``, *optional*):
                TON address of the NFT to use as the card background.

        Returns:
            :obj:`~pyrogram.types.WalletCard`: On success, the updated wallet card is returned.
        """
        r = await self.invoke(
            raw.functions.wallet.SetCardStickers(
                stickers=[sticker.write() for sticker in stickers],
                bg_nft_address=bg_nft_address
            )
        )

        return await types.WalletCard._parse(self, r)
