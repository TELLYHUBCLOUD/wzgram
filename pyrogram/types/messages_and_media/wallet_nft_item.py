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

import json
from typing import Dict, List, Optional

import pyrogram
from pyrogram import raw, types

from ..object import Object


class WalletNftAttribute(Object):
    """A trait of a TON NFT item.

    Parameters:
        trait_type (``str``):
            Type of the trait, e.g. *"Model"* or *"Symbol"*.

        value (``str``):
            Value of the trait.
    """

    def __init__(self, *, trait_type: str, value: str):
        super().__init__()

        self.trait_type = trait_type
        self.value = value

    @staticmethod
    def _parse(attribute: "raw.types.wallet.NftAttribute") -> "WalletNftAttribute":
        return WalletNftAttribute(
            trait_type=attribute.trait_type,
            value=attribute.value
        )


class WalletNftItem(Object):
    """An NFT item held by a TON wallet, as returned for example in a wallet card.

    Parameters:
        address (``str``):
            Address of the NFT item in the TON blockchain.

        owner_address (``str``):
            Address of the wallet owning the item.

        index (``str``):
            Index of the item inside its collection.

        collection_address (``str``, *optional*):
            Address of the collection the item belongs to.

        name (``str``, *optional*):
            Human readable name of the item.

        description (``str``, *optional*):
            Description of the item.

        image_url (``str``, *optional*):
            URL of the item image.

        image_small_url (``str``, *optional*):
            URL of a smaller version of the item image.

        content_url (``str``, *optional*):
            URL of the item content.

        lottie_url (``str``, *optional*):
            URL of a Lottie animation representing the item.

        attributes (List of :obj:`~pyrogram.types.WalletNftAttribute`, *optional*):
            Traits of the item.

        extra (``dict``, *optional*):
            Additional metadata attached to the item, as a JSON object.

        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            The unique gift this item was minted from, if any.
    """

    def __init__(
        self,
        *,
        address: str,
        owner_address: str,
        index: str,
        collection_address: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        image_small_url: Optional[str] = None,
        content_url: Optional[str] = None,
        lottie_url: Optional[str] = None,
        attributes: Optional[List["WalletNftAttribute"]] = None,
        extra: Optional[dict] = None,
        gift: Optional["types.Gift"] = None
    ):
        super().__init__()

        self.address = address
        self.owner_address = owner_address
        self.index = index
        self.collection_address = collection_address
        self.name = name
        self.description = description
        self.image_url = image_url
        self.image_small_url = image_small_url
        self.content_url = content_url
        self.lottie_url = lottie_url
        self.attributes = attributes
        self.extra = extra
        self.gift = gift

    @staticmethod
    def _web_document_url(web_document: "raw.base.WebDocument") -> Optional[str]:
        return getattr(web_document, "url", None) if web_document else None

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        item: "raw.types.wallet.NftItem",
        users: Dict[int, "raw.base.User"] = {},
        chats: Dict[int, "raw.base.Chat"] = {}
    ) -> Optional["WalletNftItem"]:
        if not isinstance(item, raw.types.wallet.NftItem):
            return None

        extra = None

        if item.extra is not None:
            try:
                extra = json.loads(item.extra.data)
            except (ValueError, TypeError):
                extra = None

        return WalletNftItem(
            address=item.address,
            owner_address=item.owner_address,
            index=item.index,
            collection_address=item.collection_address,
            name=item.name,
            description=item.description,
            image_url=WalletNftItem._web_document_url(item.image),
            image_small_url=WalletNftItem._web_document_url(item.image_small),
            content_url=WalletNftItem._web_document_url(item.content_url),
            lottie_url=WalletNftItem._web_document_url(item.lottie),
            attributes=(
                types.List(WalletNftAttribute._parse(a) for a in item.attributes)
                if item.attributes else None
            ),
            extra=extra,
            gift=(
                await types.Gift._parse(client, item.gift, users=users, chats=chats)
                if item.gift is not None else None
            )
        )

    @property
    def link(self) -> str:
        return f"https://tonviewer.com/{self.address}"
