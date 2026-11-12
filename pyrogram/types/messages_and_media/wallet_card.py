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

from typing import Dict, List, Optional

import pyrogram
from pyrogram import raw, types

from ..object import Object
from .wallet_card_sticker import WalletCardSticker
from .wallet_nft_item import WalletNftItem


class WalletCard(Object):
    """A Telegram wallet card, showing the TON wallet balance and the NFT stickers
    a user chose to display on it.

    Parameters:
        address (``str``):
            Address of the wallet in the TON blockchain.

        balance (``int``):
            Balance of the wallet, in nanotons.

        stickers (List of :obj:`~pyrogram.types.WalletCardSticker`, *optional*):
            NFT stickers placed on the card.

        background_nft (:obj:`~pyrogram.types.WalletNftItem`, *optional*):
            The NFT used as the card background, if any.
    """

    def __init__(
        self,
        *,
        address: str,
        balance: int,
        stickers: Optional[List["WalletCardSticker"]] = None,
        background_nft: Optional["WalletNftItem"] = None
    ):
        super().__init__()

        self.address = address
        self.balance = balance
        self.stickers = stickers
        self.background_nft = background_nft

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        card: "raw.types.wallet.Card",
        users: Dict[int, "raw.base.User"] = {},
        chats: Dict[int, "raw.base.Chat"] = {}
    ) -> Optional["WalletCard"]:
        if not isinstance(card, raw.types.wallet.Card):
            return None

        stickers = None

        if card.stickers:
            stickers = types.List(
                [
                    await WalletCardSticker._parse(client, sticker, users=users, chats=chats)
                    for sticker in card.stickers
                ]
            )

        return WalletCard(
            address=card.address,
            balance=card.balance,
            stickers=stickers or None,
            background_nft=(
                await WalletNftItem._parse(client, card.bg_nft_item, users=users, chats=chats)
                if card.bg_nft_item is not None else None
            )
        )

    @property
    def link(self) -> str:
        return f"https://tonviewer.com/{self.address}"
