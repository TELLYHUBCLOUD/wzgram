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

from typing import Dict, Optional, Union

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class WidgetQuery(Object):
    """An incoming query sent by an HTML :obj:`~pyrogram.types.Widget` attached to a
    message the bot sent.

    Widget queries let the reactive UI inside a message talk back to the bot: the
    widget posts a payload and waits for :meth:`~pyrogram.types.WidgetQuery.answer`
    to return data to it. A query can also carry a signed payload or a transaction
    notification from the user's TON wallet (see *query_type*).

    Parameters:
        id (``str``):
            Unique identifier of the query.

        query_type (:obj:`~pyrogram.types.WidgetQueryTypeData` | :obj:`~pyrogram.types.WidgetQueryTypeSignData` | :obj:`~pyrogram.types.WidgetQueryTypeSentTransaction`):
            Kind of query the widget sent: plain data, signed wallet data or a
            transaction notification.

        from_user (:obj:`~pyrogram.types.User`):
            The user whose widget sent the query.

        data (``bytes``):
            Opaque payload the widget attached to the query.

        chat_type (``str``):
            Type of the chat the widget lives in, as reported by the client.

        chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat the widget message belongs to. Not set for queries coming from
            inline widgets or from widget copies.

        message_id (``int``, *optional*):
            Identifier of the message the widget is attached to, if any.

        inline_message_id (``str``, *optional*):
            Identifier of the inline message the widget is attached to, if any.

        chat_instance (``str``, *optional*):
            Global identifier of the chat the widget lives in, used with inline widgets.

        widget_id (``int``, *optional*):
            Identifier of the shared widget, when the query comes from one.

        wallet_card (:obj:`~pyrogram.types.WalletCard`, *optional*):
            Card of the user's TON wallet, with balances and NFT stickers, sent
            together with the query when the widget asked for it.
    """

    def __init__(
        self,
        *,
        id: str,
        query_type: Union[
            "types.WidgetQueryTypeData",
            "types.WidgetQueryTypeSignData",
            "types.WidgetQueryTypeSentTransaction"
        ],
        from_user: "types.User",
        data: bytes,
        chat_type: Optional[str] = None,
        chat: Optional["types.Chat"] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        chat_instance: Optional[str] = None,
        widget_id: Optional[int] = None,
        wallet_card: Optional["types.WalletCard"] = None,
        client: "pyrogram.Client" = None
    ):
        super().__init__(client)

        self.id = id
        self.query_type = query_type
        self.from_user = from_user
        self.data = data
        self.chat_type = chat_type
        self.chat = chat
        self.message_id = message_id
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.widget_id = widget_id
        self.wallet_card = wallet_card

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        update: Union[
            "raw.types.UpdateBotWidgetQuery",
            "raw.types.UpdateInlineBotWidgetQuery",
            "raw.types.UpdateBotWidgetCopyQuery"
        ],
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"]
    ) -> "WidgetQuery":
        chat = None
        message_id = None
        inline_message_id = None

        if isinstance(update, raw.types.UpdateBotWidgetQuery):
            raw_id = utils.get_raw_peer_id(update.peer)

            if (isinstance(update.peer, (raw.types.PeerUser,)) and raw_id in users) or (
                isinstance(update.peer, (raw.types.PeerChat, raw.types.PeerChannel)) and raw_id in chats
            ):
                chat = types.Chat._parse_dialog(client, update.peer, users, chats)

            message_id = update.msg_id
        elif isinstance(update, raw.types.UpdateInlineBotWidgetQuery):
            inline_message_id = utils.pack_inline_message_id(update.inline_message_id)

        chat_instance = getattr(update, "chat_instance", None)
        chat_type = getattr(update, "chat_type", None)

        return WidgetQuery(
            id=str(update.query_id),
            query_type=types.WidgetQueryType._parse(update.query_type),
            from_user=types.User._parse(client, users[update.user_id]),
            data=update.data,
            chat_type=chat_type if chat_type else None,
            chat=chat,
            message_id=message_id,
            inline_message_id=inline_message_id,
            chat_instance=(
                str(chat_instance)
                if chat_instance is not None else None
            ),
            widget_id=update.widget_id,
            wallet_card=await types.WalletCard._parse(client, update.wallet_card, users=users, chats=chats),
            client=client
        )

    async def answer(self, result: Optional[str] = None) -> bool:
        """Bound method *answer* of :obj:`~pyrogram.types.WidgetQuery`.

        Use this method as a shortcut for:

        .. code-block:: python

            await client.answer_widget_query(widget_query.id, result="{}")

        Example:
            .. code-block:: python

                await widget_query.answer(result='{"ok": true}')

        Parameters:
            result (``str``, *optional*):
                Data passed back to the widget, as a JSON string. The widget receives
                it as the answer of its pending query call.

        Returns:
            ``bool``: True on success.
        """
        return await self._client.answer_widget_query(
            widget_query_id=self.id,
            result=result
        )
