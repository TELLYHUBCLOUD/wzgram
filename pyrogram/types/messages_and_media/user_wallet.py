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

from pyrogram import raw

from ..object import Object


class UserWallet(Object):
    """The TON wallet of a user, as attached for example to a widget query asking
    to sign data or notifying about a transaction.

    Parameters:
        address (``str``):
            Address of the wallet in the TON blockchain.

        balance (``int``):
            Balance of the wallet, in nanotons.

        public_key (``bytes``, *optional*):
            Public key of the wallet.

        state_init (``bytes``, *optional*):
            State init of the wallet contract, for wallets not deployed yet.
    """

    def __init__(
        self,
        *,
        address: str,
        balance: int,
        public_key: Optional[bytes] = None,
        state_init: Optional[bytes] = None
    ):
        super().__init__()

        self.address = address
        self.balance = balance
        self.public_key = public_key
        self.state_init = state_init

    @staticmethod
    def _parse(wallet: "raw.types.UserWallet") -> Optional["UserWallet"]:
        if not isinstance(wallet, raw.types.UserWallet):
            return None

        return UserWallet(
            address=wallet.address,
            balance=wallet.balance,
            public_key=wallet.public_key,
            state_init=wallet.state_init
        )

    @property
    def link(self) -> str:
        return f"https://tonviewer.com/{self.address}"
