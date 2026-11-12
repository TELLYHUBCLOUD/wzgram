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

"""Bot API 10.4: HTML widgets, widget queries, TON wallet cards and
secondary bot usernames."""

from unittest.mock import AsyncMock, MagicMock

import pyrogram
from pyrogram import enums, filters, raw, types, utils
from pyrogram.dispatcher import Dispatcher
from pyrogram.handlers import WidgetQueryHandler


def _raw_user(user_id, first_name):
    return raw.types.User(
        id=user_id, first_name=first_name, usernames=[], restriction_reason=[]
    )


def _widget_message(**media_kwargs):
    return raw.types.Message(
        id=10,
        from_id=raw.types.PeerUser(user_id=1),
        peer_id=raw.types.PeerUser(user_id=2),
        date=0,
        message="",
        entities=[],
        restriction_reason=[],
        media=raw.types.MessageMediaWidget(
            width=320,
            height=240,
            payload=b"\x01\x02",
            **media_kwargs
        ),
    )


class TestWidgetMedia:
    async def test_a_widget_media_message_is_parsed(self):
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}
        message = _widget_message(
            can_query=True,
            public_data='{"score": 3}',
            public_data_hash=42,
            chat_data="per-chat",
            widget_id=9001,
        )

        parsed = await types.Message._parse(MagicMock(), message, users, {})

        assert parsed.media == enums.MessageMediaType.WIDGET
        assert parsed.widget.width == 320
        assert parsed.widget.height == 240
        assert parsed.widget.payload == b"\x01\x02"
        assert parsed.widget.can_query is True
        assert parsed.widget.public_data == '{"score": 3}'
        assert parsed.widget.public_data_hash == 42
        assert parsed.widget.chat_data == "per-chat"
        assert parsed.widget.widget_id == 9001

    async def test_a_widget_copy_is_flagged(self):
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}
        parsed = await types.Message._parse(
            MagicMock(), _widget_message(is_copy=True), users, {}
        )

        assert parsed.widget.is_copy is True

    async def test_the_widget_filter_matches_widgets_only(self):
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}
        widget_message = await types.Message._parse(
            MagicMock(), _widget_message(), users, {}
        )
        plain_message = types.Message(id=1)

        assert await filters.widget(None, widget_message)
        assert not (await filters.widget(None, plain_message))


class TestWidgetQueryTypes:
    def test_a_plain_data_query(self):
        parsed = types.WidgetQueryType._parse(
            raw.types.WidgetQueryTypeData(with_wallet=True)
        )

        assert isinstance(parsed, types.WidgetQueryTypeData)
        assert parsed.with_wallet is True

    def test_a_sign_data_query_carries_the_wallet(self):
        parsed = types.WidgetQueryType._parse(
            raw.types.WidgetQueryTypeSignData(
                wallet=raw.types.UserWallet(address="EQxxx", balance=1000000000),
                sign_data=raw.types.DataJSON(data='{"payload": 1}')
            )
        )

        assert isinstance(parsed, types.WidgetQueryTypeSignData)
        assert parsed.wallet.address == "EQxxx"
        assert parsed.wallet.balance == 1000000000
        assert parsed.sign_data == '{"payload": 1}'

    def test_a_sent_transaction_query_carries_the_hash(self):
        parsed = types.WidgetQueryType._parse(
            raw.types.WidgetQueryTypeSentTransaction(
                wallet=raw.types.UserWallet(
                    address="EQyyy", balance=0, public_key=b"k", state_init=b"s"
                ),
                msg_hash="deadbeef"
            )
        )

        assert isinstance(parsed, types.WidgetQueryTypeSentTransaction)
        assert parsed.transaction_hash == "deadbeef"
        assert parsed.wallet.public_key == b"k"
        assert parsed.wallet.state_init == b"s"


class TestWidgetQuery:
    def _update(self, **overrides):
        args = dict(
            query_id=777,
            query_type=raw.types.WidgetQueryTypeData(),
            user_id=1,
            peer=raw.types.PeerUser(user_id=2),
            msg_id=10,
            chat_instance=12345,
            chat_type="private",
            data=b'{"tap": 1}',
        )
        args.update(overrides)
        return raw.types.UpdateBotWidgetQuery(**args)

    async def test_a_bot_widget_query_is_parsed(self):
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}

        query = await types.WidgetQuery._parse(
            MagicMock(), self._update(wallet_card=None), users, {}
        )

        assert query.id == "777"
        assert query.from_user.id == 1
        assert query.message_id == 10
        assert query.chat_type == "private"
        assert query.chat_instance == "12345"
        assert query.data == b'{"tap": 1}'
        assert query.chat is not None
        assert isinstance(query.query_type, types.WidgetQueryTypeData)
        assert query.wallet_card is None

    async def test_an_inline_widget_query_packs_the_inline_message_id(self):
        users = {1: _raw_user(1, "Tapper")}
        inline_id = raw.types.InputBotInlineMessageID(dc_id=2, id=99, access_hash=7)
        update = raw.types.UpdateInlineBotWidgetQuery(
            query_id=888,
            query_type=raw.types.WidgetQueryTypeData(),
            user_id=1,
            inline_message_id=inline_id,
            chat_instance=12345,
            chat_type="private",
            data=b"{}",
        )

        query = await types.WidgetQuery._parse(MagicMock(), update, users, {})

        assert query.inline_message_id == utils.pack_inline_message_id(inline_id)
        assert query.message_id is None
        assert query.chat is None

    async def test_a_copy_query_has_no_chat_bits(self):
        users = {1: _raw_user(1, "Copier")}
        update = raw.types.UpdateBotWidgetCopyQuery(
            query_id=999,
            query_type=raw.types.WidgetQueryTypeData(with_wallet=False),
            user_id=1,
            data=b"{}",
            widget_id=555,
        )

        query = await types.WidgetQuery._parse(MagicMock(), update, users, {})

        assert query.id == "999"
        assert query.widget_id == 555
        assert query.chat is None
        assert query.chat_instance is None
        assert query.chat_type is None

    async def test_a_query_can_carry_the_wallet_card(self):
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}
        card = raw.types.wallet.Card(
            stickers=[
                raw.types.wallet.CardSticker(
                    coordinates=raw.types.MediaAreaCoordinates(
                        x=1.0, y=2.0, w=3.0, h=4.0, rotation=5.0
                    ),
                    nft=raw.types.wallet.NftItem(
                        address="EQnft", owner_address="EQowner", index="0",
                        name="Cool NFT"
                    ),
                )
            ],
            address="EQcard",
            balance=42000000000,
        )

        query = await types.WidgetQuery._parse(
            MagicMock(), self._update(wallet_card=card), users, {}
        )

        assert query.wallet_card.address == "EQcard"
        assert query.wallet_card.balance == 42000000000
        sticker = query.wallet_card.stickers[0]
        assert (sticker.x, sticker.y, sticker.width, sticker.height, sticker.rotation) == (1.0, 2.0, 3.0, 4.0, 5.0)
        assert sticker.nft_address == "EQnft"
        assert sticker.nft.name == "Cool NFT"

    async def test_the_bound_answer_calls_the_client(self):
        client = MagicMock()
        client.answer_widget_query = AsyncMock(return_value=True)
        users = {1: _raw_user(1, "Sender"), 2: _raw_user(2, "Receiver")}

        query = await types.WidgetQuery._parse(
            client, self._update(wallet_card=None), users, {}
        )
        await query.answer(result='{"ok": true}')

        client.answer_widget_query.assert_awaited_once_with(
            widget_query_id="777", result='{"ok": true}'
        )


class TestDispatcherWiring:
    def test_all_three_widget_query_updates_share_the_widget_parser(self):
        dispatcher = Dispatcher(MagicMock(listeners=None))

        parsers = [
            dispatcher.update_parsers[upd]
            for upd in (
                raw.types.UpdateBotWidgetQuery,
                raw.types.UpdateInlineBotWidgetQuery,
                raw.types.UpdateBotWidgetCopyQuery,
            )
        ]

        assert None not in parsers
        assert parsers[0] is parsers[1] is parsers[2]

    async def test_each_widget_update_yields_a_widget_query_handler(self):
        dispatcher = Dispatcher(MagicMock(listeners=None))
        users = {1: _raw_user(1, "Tapper"), 2: _raw_user(2, "Receiver")}
        updates = [
            raw.types.UpdateBotWidgetQuery(
                query_id=777,
                query_type=raw.types.WidgetQueryTypeData(),
                user_id=1,
                peer=raw.types.PeerUser(user_id=2),
                msg_id=10,
                chat_instance=12345,
                chat_type="private",
                data=b"{}",
            ),
            raw.types.UpdateInlineBotWidgetQuery(
                query_id=888,
                query_type=raw.types.WidgetQueryTypeData(),
                user_id=1,
                inline_message_id=raw.types.InputBotInlineMessageID(dc_id=2, id=99, access_hash=7),
                chat_instance=12345,
                chat_type="private",
                data=b"{}",
            ),
            raw.types.UpdateBotWidgetCopyQuery(
                query_id=999,
                query_type=raw.types.WidgetQueryTypeData(),
                user_id=1,
                data=b"{}",
                widget_id=2,
            ),
        ]

        for update in updates:
            parsed, handler_type = await dispatcher.update_parsers[type(update)](
                update, users, {}
            )

            assert isinstance(parsed, types.WidgetQuery)
            assert handler_type is WidgetQueryHandler

    def test_the_decorator_registers_the_handler_type(self):
        @pyrogram.Client.on_widget_query(filters=None)
        async def handler(client, query):
            pass

        pairs = handler.handlers

        assert len(pairs) == 1
        assert isinstance(pairs[0][0], WidgetQueryHandler)


def _client():
    client = pyrogram.Client("t", in_memory=True, api_id=1, api_hash="x")
    client.is_connected = True

    async def resolve_peer(peer_id):
        if peer_id in ("me", "self"):
            return raw.types.InputPeerSelf()

        return raw.types.InputPeerUser(user_id=1, access_hash=77)

    client.resolve_peer = AsyncMock(side_effect=resolve_peer)
    return client


class TestWidgetMethods:
    async def test_send_widget_sends_a_widget_input_media(self):
        client = _client()
        client.invoke = AsyncMock(return_value=MagicMock(updates=[]))

        await client.send_widget(
            1, "<b>hi</b>", width=320, height=240,
            allow_queries=True, shared_widget=True,
            public_data="{}", chat_data="chat"
        )

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.messages.SendMedia)
        assert isinstance(query.media, raw.types.InputMediaWidget)
        assert query.media.html == "<b>hi</b>"
        assert (query.media.width, query.media.height) == (320, 240)
        assert query.media.allow_queries is True
        assert query.media.shared_widget is True
        assert query.media.public_data == "{}"
        assert query.media.chat_data == "chat"

    async def test_send_shared_widget_references_the_widget_id(self):
        client = _client()
        client.invoke = AsyncMock(return_value=MagicMock(updates=[]))

        await client.send_shared_widget(1, widget_id=123, chat_data="x")

        query = client.invoke.await_args.args[0]
        assert isinstance(query.media, raw.types.InputMediaWidgetId)
        assert query.media.widget_id == 123
        assert query.media.chat_data == "x"

    async def test_send_widget_can_be_ephemeral(self):
        client = _client()
        client.invoke = AsyncMock(return_value=MagicMock(updates=[]))

        await client.send_widget(
            1, "<b>hi</b>", width=320, height=240,
            ephemeral_message_parameters=types.EphemeralMessageParameters(
                receiver_user_id=2,
                callback_query_id="777",
                replace_callback_query_message=True,
            )
        )

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.ephemeral.SendMessage)
        assert isinstance(query.media, raw.types.InputMediaWidget)
        assert query.media.html == "<b>hi</b>"
        assert query.query_id == 777
        assert query.anchor is True
        assert (query.receiver_id.user_id, query.receiver_id.access_hash) == (1, 77)

    async def test_send_shared_widget_can_be_ephemeral(self):
        client = _client()
        client.invoke = AsyncMock(return_value=MagicMock(updates=[]))

        await client.send_shared_widget(
            1, widget_id=123,
            ephemeral_message_parameters=types.EphemeralMessageParameters(receiver_user_id=2)
        )

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.ephemeral.SendMessage)
        assert isinstance(query.media, raw.types.InputMediaWidgetId)
        assert query.media.widget_id == 123

    async def test_edit_message_widget_data_hits_the_right_function(self):
        client = _client()
        client.invoke = AsyncMock(return_value=MagicMock(updates=[]))

        await client.edit_message_widget_data(
            1, 10, public_data="{}", chat_data="c",
            business_connection_id="business-id"
        )

        call = client.invoke.await_args
        query = call.args[0]
        assert isinstance(query, raw.functions.messages.EditMessageWidgetData)
        assert query.id == 10
        assert query.public_data == "{}"
        assert query.chat_data == "c"
        assert call.kwargs["business_connection_id"] == "business-id"

    async def test_edit_message_widget_data_accepts_the_lightweight_update(self):
        client = _client()
        client.invoke = AsyncMock(
            return_value=MagicMock(
                users=[],
                chats=[],
                updates=[
                    raw.types.UpdateMessageWidgetData(
                        peer=raw.types.PeerUser(user_id=1),
                        msg_id=10,
                        public_data="{}",
                        public_data_hash=42,
                        chat_data="c",
                        pts=1,
                        pts_count=1,
                    )
                ]
            )
        )

        assert await client.edit_message_widget_data(1, 10, public_data="{}") is None

    async def test_edit_inline_widget_data_unpacks_the_inline_message_id(self):
        client = _client()
        client.invoke = AsyncMock(return_value=True)
        packed = utils.pack_inline_message_id(
            raw.types.InputBotInlineMessageID(dc_id=4, id=42, access_hash=9)
        )

        await client.edit_inline_widget_data(packed, public_data="{}")

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.messages.EditInlineBotMessageWidgetData)
        unpacked = query.id
        assert (unpacked.dc_id, unpacked.id, unpacked.access_hash) == (4, 42, 9)

    async def test_edit_widget_data_is_the_shared_one(self):
        client = _client()
        client.invoke = AsyncMock(return_value=True)

        await client.edit_widget_data(555, public_data="{}", cache_time=30)

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.messages.EditWidgetData)
        assert (query.widget_id, query.public_data, query.cache_time) == (555, "{}", 30)

    async def test_answer_widget_query(self):
        client = _client()
        client.invoke = AsyncMock(return_value=True)

        await client.answer_widget_query("777", result='{"ok": true}')

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.messages.SetBotWidgetQueryAnswer)
        assert (query.query_id, query.result) == (777, '{"ok": true}')

    async def test_get_widget_public_data_passes_the_hash(self):
        client = _client()
        client.invoke = AsyncMock(
            return_value=raw.types.messages.WidgetPublicData(hash=5, data="{}", period=60)
        )

        result = await client.get_widget_public_data(1, 10, hash=5)

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.messages.GetWidgetPublicData)
        assert (query.msg_id, query.hash) == (10, 5)
        assert result.data == "{}" and result.hash == 5 and result.period == 60
        assert result.not_modified is False

    async def test_get_widget_public_data_reports_not_modified(self):
        client = _client()
        client.invoke = AsyncMock(
            return_value=raw.types.messages.WidgetPublicDataNotModified(period=60)
        )

        result = await client.get_widget_public_data(1, 10, hash=5)

        assert result.not_modified is True
        assert result.hash == 5
        assert result.data is None

    async def test_get_unique_gift_looks_up_by_name(self):
        client = _client()

        async def fake_invoke(query, *args, **kwargs):
            assert isinstance(query, raw.functions.payments.GetUniqueStarGift)
            assert query.slug == "SignetRing-903"
            return MagicMock(gift=None, users=[], chats=[])

        client.invoke = fake_invoke
        await client.get_unique_gift("https://t.me/nft/SignetRing-903")

    async def test_get_unique_gift_accepts_a_bare_name(self):
        client = _client()

        async def fake_invoke(query, *args, **kwargs):
            assert query.slug == "SignetRing-903"
            return MagicMock(gift=None, users=[], chats=[])

        client.invoke = fake_invoke
        await client.get_unique_gift("SignetRing-903")

    async def test_set_card_stickers_preserves_all_coordinates(self):
        client = _client()
        client.invoke = AsyncMock(
            return_value=raw.types.wallet.Card(
                stickers=[], address="EQcard", balance=100
            )
        )

        card = await client.set_card_stickers(
            [
                types.WalletCardSticker(
                    x=1.0,
                    y=2.0,
                    width=3.0,
                    height=4.0,
                    rotation=5.0,
                    radius=6.0,
                    nft_address="EQnft"
                )
            ],
            bg_nft_address="EQbackground"
        )

        query = client.invoke.await_args.args[0]
        sticker = query.stickers[0]
        assert isinstance(sticker, raw.types.InputWalletCardSticker)
        assert (sticker.coordinates.x, sticker.coordinates.y) == (1.0, 2.0)
        assert (sticker.coordinates.w, sticker.coordinates.h) == (3.0, 4.0)
        assert (sticker.coordinates.rotation, sticker.coordinates.radius) == (5.0, 6.0)
        assert (sticker.nft_address, query.bg_nft_address) == ("EQnft", "EQbackground")
        assert (card.address, card.balance) == ("EQcard", 100)


class TestBotUsernames:
    async def _run(self, fn, *args, **kwargs):
        client = _client()
        client.invoke = AsyncMock(return_value=True)
        await fn(client, *args, **kwargs)
        return client.invoke.await_args.args[0]

    async def test_add_bot_username_targets_self_when_asked(self):
        client = _client()
        client.invoke = AsyncMock(return_value=True)

        await client.add_bot_username("helper_agent", bot_id="me")

        query = client.invoke.await_args.args[0]
        assert isinstance(query, raw.functions.bots.AddUsername)
        assert isinstance(query.bot, raw.types.InputUserSelf)
        assert query.username == "helper_agent"

    async def test_add_bot_username_resolves_a_named_bot(self):
        client = _client()
        client.invoke = AsyncMock(return_value=True)

        await client.add_bot_username("helper_ai", bot_id="@HelperBot")

        query = client.invoke.await_args.args[0]
        client.resolve_peer.assert_awaited_once_with("@HelperBot")
        assert isinstance(query.bot, raw.types.InputUser)
        assert (query.bot.user_id, query.bot.access_hash) == (1, 77)

    async def test_remove_bot_username(self):
        query = await self._run(pyrogram.Client.remove_bot_username, "helper_ai", "me")

        assert isinstance(query, raw.functions.bots.RemoveUsername)
        assert query.username == "helper_ai"

    async def test_toggle_bot_username(self):
        query = await self._run(
            pyrogram.Client.toggle_bot_username, "@helper_ai", False, "me"
        )

        assert isinstance(query, raw.functions.bots.ToggleUsername)
        assert (query.username, query.active) == ("helper_ai", False)

    async def test_reorder_bot_usernames(self):
        query = await self._run(
            pyrogram.Client.reorder_bot_usernames, ["b_ai", "a_agent"], "me"
        )

        assert isinstance(query, raw.functions.bots.ReorderUsernames)
        assert query.order == ["b_ai", "a_agent"]


class TestRichQuoteInput:
    async def test_quote_rich_is_passed_as_rich_text(self):
        client = _client()

        reply_to = await utils.get_reply_to(
            client,
            types.ReplyParameters(
                message_id=3,
                quote_rich=[raw.types.TextBold(text=raw.types.TextPlain(text="pay")), " now"],
            ),
        )

        assert isinstance(reply_to, raw.types.InputReplyToMessage)
        assert len(reply_to.quote_rich) == 2
        assert isinstance(reply_to.quote_rich[0], raw.types.TextBold)
        assert isinstance(reply_to.quote_rich[1], raw.types.TextPlain)
        assert reply_to.quote_rich[1].text == " now"

    async def test_a_lone_string_is_wrapped(self):
        client = _client()

        reply_to = await utils.get_reply_to(
            client,
            types.ReplyParameters(message_id=3, quote_rich="half a sentence"),
        )

        assert isinstance(reply_to.quote_rich[0], raw.types.TextPlain)
        assert reply_to.quote_rich[0].text == "half a sentence"
