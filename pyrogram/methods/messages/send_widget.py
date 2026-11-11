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

log = logging.getLogger(__name__)


class SendWidget:
    async def send_widget(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        html: str,
        width: int,
        height: int,
        allow_queries: Optional[bool] = None,
        shared_widget: Optional[bool] = None,
        public_data: Optional[str] = None,
        chat_data: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        schedule_date: Optional[datetime] = None,
        protect_content: Optional[bool] = None,
        reply_markup: Optional[Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ]] = None,
        business_connection_id: Optional[str] = None
    ) -> "types.Message":
        """Send an HTML widget.

        Widgets are custom, dynamic interfaces rendered right inside message bubbles,
        giving bots and AI agents a canvas for interactive tools, games and workflows.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            html (``str``):
                HTML markup of the widget. The markup may use dynamic layouts, custom
                sizing and interactive elements; widget scripts reach the bot through
                widget queries (see :meth:`~pyrogram.Client.on_widget_query`).

            width (``int``):
                Width of the widget viewport, in device-independent pixels.

            height (``int``):
                Height of the widget viewport, in device-independent pixels.

            allow_queries (``bool``, *optional*):
                Pass True to allow the widget to send queries to the bot.

            shared_widget (``bool``, *optional*):
                Pass True to make this the current message rendering the bot's shared
                widget, immediately updated whenever
                :meth:`~pyrogram.Client.edit_widget_data` changes it.

            public_data (``str``, *optional*):
                Public data shown by the widget, visible to everyone who sees the message.

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

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent widget message is returned.

        Example:
            .. code-block:: python

                await app.send_widget(
                    chat_id,
                    "<b>Game</b><canvas id='board'></canvas>",
                    width=320,
                    height=240,
                    allow_queries=True,
                )
        """
        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaWidget(
                    allow_queries=allow_queries,
                    shared_widget=shared_widget,
                    width=width,
                    height=height,
                    html=html,
                    public_data=public_data,
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
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                entities=None,
                message=""
            ),
            sleep_threshold=60,
            business_connection_id=business_connection_id
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
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
