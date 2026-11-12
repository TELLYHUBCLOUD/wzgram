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
from .wallet_nft_item import WalletNftItem


class WalletCardSticker(Object):
    """An NFT sticker placed on a Telegram wallet card.

    Parameters:
        x (``float``):
            Horizontal position of the sticker, as a percentage of the card width.

        y (``float``):
            Vertical position of the sticker, as a percentage of the card height.

        width (``float``):
            Width of the sticker, as a percentage of the card width.

        height (``float``):
            Height of the sticker, as a percentage of the card height.

        rotation (``float``):
            Clockwise rotation of the sticker, in degrees.

        nft_address (``str``):
            Address of the NFT in the TON blockchain displayed by the sticker.

        nft (:obj:`~pyrogram.types.WalletNftItem`, *optional*):
            The NFT displayed by the sticker, when the sticker was received from Telegram.

        radius (``float``, *optional*):
            Corner radius of the sticker, as a percentage of the card width. Currently, it is 0.
    """

    def __init__(
        self,
        *,
        x: float,
        y: float,
        width: float,
        height: float,
        rotation: float,
        nft_address: str,
        nft: Optional["WalletNftItem"] = None,
        radius: Optional[float] = None
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.radius = radius
        self.nft_address = nft_address
        self.nft = nft

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        sticker: "raw.types.wallet.CardSticker",
        users: dict = {},
        chats: dict = {}
    ) -> "WalletCardSticker":
        return WalletCardSticker(
            x=sticker.coordinates.x,
            y=sticker.coordinates.y,
            width=sticker.coordinates.w,
            height=sticker.coordinates.h,
            rotation=sticker.coordinates.rotation,
            radius=getattr(sticker.coordinates, "radius", None),
            nft=await WalletNftItem._parse(client, sticker.nft, users=users, chats=chats),
            nft_address=sticker.nft.address
        )

    def write(self) -> "raw.types.InputWalletCardSticker":
        return raw.types.InputWalletCardSticker(
            coordinates=raw.types.MediaAreaCoordinates(
                x=self.x,
                y=self.y,
                w=self.width,
                h=self.height,
                rotation=self.rotation,
                radius=self.radius
            ),
            nft_address=self.nft_address
        )
