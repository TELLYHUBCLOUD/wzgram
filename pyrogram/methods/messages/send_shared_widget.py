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
from datetime import datetime
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils

from ..ephemeral.as_ephemeral import as_ephemeral

log = logging.getLogger(__name__)


class SendSharedWidget:
    async def send_shared_widget(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        widget_id: int,
        chat_data: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        schedule_date: Optional[datetime] = None,
        protect_content: Optional[bool] = None,
        business_connection_id: Optional[str] = None,
        ephemeral_message_parameters: Optional["types.EphemeralMessageParameters"] = None
    ) -> "types.Message":
        """Send a shared widget.

        Shared widgets reuse the same UI across messages: every message renders the
        widget identified by *widget_id* and is instantly updated whenever
        :meth:`~pyrogram.Client.edit_widget_data` changes its public data from the
        centralized setting.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            widget_id (``int``):
                Identifier of the shared widget to render, as found on
                :obj:`~pyrogram.types.Widget` (``widget_id``) of a widget sent with
                :meth:`~pyrogram.Client.send_widget` using ``shared_widget=True``.

            chat_data (``str``, *optional*):
                Data of the widget specific to the chat the message is sent to.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier of a message thread to which the message belongs.
                For supergroups only.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            ephemeral_message_parameters (:obj:`~pyrogram.types.EphemeralMessageParameters`, *optional*):
                Send the shared widget as an ephemeral message, visible only to the user
                it names and absent from the chat's history.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent widget message is returned.

        Example:
            .. code-block:: python

                await app.send_shared_widget(chat_id, widget_id=widget.widget_id)
        """
        r = await self.invoke(
            await as_ephemeral(self, ephemeral_message_parameters, raw.functions.messages.SendMedia(
                    peer=await self.resolve_peer(chat_id),
                    media=raw.types.InputMediaWidgetId(
                        widget_id=widget_id,
                        chat_data=chat_data
                    ),
                    silent=disable_notification if disable_notification is not None else None,
                    reply_to=await utils.get_reply_to(
                        self,
                        reply_parameters,
                        message_thread_id
                    ),
                    random_id=self.rnd_id(),
                    schedule_date=utils.datetime_to_timestamp(schedule_date),
                    noforwards=protect_content,
                    entities=None,
                    message=""
                )
            ),
            sleep_threshold=60,
            business_connection_id=business_connection_id
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewEphemeralMessage,
                              raw.types.UpdateNewScheduledMessage,
                              raw.types.UpdateBotNewBusinessMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    business_connection_id=getattr(i, "connection_id", None),
                    raw_reply_to_message=getattr(i, "reply_to_message", None)
                )
