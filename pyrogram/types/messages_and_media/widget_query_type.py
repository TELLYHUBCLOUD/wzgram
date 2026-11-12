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

from typing import Optional, Union

from pyrogram import raw

from ..object import Object
from .user_wallet import UserWallet


class WidgetQueryType(Object):
    """Base class for the kinds of queries a widget can send to the bot that owns it.

    The concrete subclasses are :obj:`~pyrogram.types.WidgetQueryTypeData`,
    :obj:`~pyrogram.types.WidgetQueryTypeSignData` and
    :obj:`~pyrogram.types.WidgetQueryTypeSentTransaction`.
    """

    @staticmethod
    def _parse(
        query_type: "raw.base.WidgetQueryType"
    ) -> Optional[Union["WidgetQueryTypeData", "WidgetQueryTypeSignData", "WidgetQueryTypeSentTransaction"]]:
        if isinstance(query_type, raw.types.WidgetQueryTypeData):
            return WidgetQueryTypeData(
                with_wallet=query_type.with_wallet
            )

        if isinstance(query_type, raw.types.WidgetQueryTypeSignData):
            return WidgetQueryTypeSignData(
                wallet=UserWallet._parse(query_type.wallet),
                sign_data=query_type.sign_data.data
            )

        if isinstance(query_type, raw.types.WidgetQueryTypeSentTransaction):
            return WidgetQueryTypeSentTransaction(
                wallet=UserWallet._parse(query_type.wallet),
                transaction_hash=query_type.msg_hash
            )

        return None


class WidgetQueryTypeData(WidgetQueryType):
    """A plain data query from a widget.

    Parameters:
        with_wallet (``bool``, *optional*):
            True, if the widget also sent the user's wallet card with the query.
    """

    def __init__(self, *, with_wallet: Optional[bool] = None):
        super().__init__()

        self.with_wallet = with_wallet


class WidgetQueryTypeSignData(WidgetQueryType):
    """A widget query asking the bot to be notified about data the user signed
    with their TON wallet.

    Parameters:
        wallet (:obj:`~pyrogram.types.UserWallet`):
            The wallet that signed the data.

        sign_data (``str``):
            The signed payload, as a JSON string.
    """

    def __init__(self, *, wallet: "UserWallet", sign_data: str):
        super().__init__()

        self.wallet = wallet
        self.sign_data = sign_data


class WidgetQueryTypeSentTransaction(WidgetQueryType):
    """A widget query notifying the bot about a transaction the user sent
    from their TON wallet.

    Parameters:
        wallet (:obj:`~pyrogram.types.UserWallet`):
            The wallet the transaction was sent from.

        transaction_hash (``str``):
            Hash of the transaction message in the TON blockchain.
    """

    def __init__(self, *, wallet: "UserWallet", transaction_hash: str):
        super().__init__()

        self.wallet = wallet
        self.transaction_hash = transaction_hash
