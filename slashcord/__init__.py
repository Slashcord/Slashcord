"""MIT License

Copyright (c) 2021 Slashcord

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import aiojobs

from typing import Coroutine, List, AsyncGenerator
from functools import wraps
from aiohttp import ClientSession

from json import JSONDecodeError, JSONDecoder

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ._settings import (
    Command,
    CommandChoice,
    WebhookServer
)
from ._exceptions import (
    SlashCordException,
    HttpException,
    CommandConfigException,
    InvalidName,
    InvalidDescription,
    InvalidChoiceName,
    WebhookException,
    InvalidSignature,
    InvalidJson,
    StartupNotCalled
)
from ._guild import Guild
from ._models import WebhookModel, CommandModel
from ._message import Message, Embed
from .http import HttpClient, HttpServer

assert Command, CommandChoice
assert WebhookServer
assert Message, Embed

assert SlashCordException
assert HttpException
assert CommandConfigException
assert InvalidName
assert InvalidDescription
assert InvalidChoiceName
assert WebhookException
assert InvalidSignature
assert InvalidJson
assert StartupNotCalled

assert WebhookModel


__version__ = "0.0.2"
__url__ = "https://slashcord.readthedocs.io/en/latest/"
__description__ = "Discord's slash commands built for asyncio python."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "MIT"


class SlashCord(HttpClient):
    BASE_URL = "https://discord.com/api/v8/"

    def __init__(self, token: str, client_id: int, public_key: str,
                 webhook_server: WebhookServer = WebhookServer()) -> None:
        """Wrapper for Discord's slash commands!

        Parameters
        ----------
        token : str
            You can use either your bot token or a client credentials token
            for your app with the applications.commmands.update scope
        client_id : int
            Client / Application ID.
        public_key : str
            Client public key.
        webhook_server : WebhookServer, optional
            Used to configure webhook server, set as None to disable.
            by default WebhookServer()

        Notes
        -----
        Calling self.start
        ~~~~~~~~~~~~~~~~~~
        await self.start must be called before using.

        WebhookServer not passed
        ~~~~~~~~~~~~~~~~~~~~~~~~
        If the webhook server configuration isn't passed
        the command decorator won't work

        The point of this is so you can use this wrapper
        without having to run a HTTP server, what you might
        already be running.

        The self.webhook can be used to validate & phrase
        json data given.

        Reverse Proxy
        ~~~~~~~~~~~~~
        For production you should setup a reverse proxy
        for the http server, something like nginx.
        """

        if len(token) == 32:
            self._auth = "Bearer "
        else:
            self._auth = "Bot "

        self._auth += token

        if webhook_server:
            self._server = HttpServer(
                webhook_server._ip, webhook_server._port, self
            )
        else:
            self._server = None

        self._requests = None

        self._client_id = client_id
        self._verify_key = VerifyKey(bytes.fromhex(public_key))

        # Used for decorator
        # {
        #   "command_id": List[Coroutine],
        # }
        self._global_funcs = {}

        # Used for decorator
        # {
        #   "guild_id": {
        #       "command_id": List[Coroutine],
        #    }
        # }
        self._guild_funcs = {}

    async def startup(self) -> None:
        """Used to start up SlashCord, must be called
           before making any other calls.

        Notes
        -----
        Should only be called once.
        """

        # ClientSession should be created within
        # context of event loop.
        self._requests = ClientSession(
            headers={"Authorization": self._auth}
        )

        if self._server:
            self._scheduler = await aiojobs.create_scheduler()
            await self._server.start()

    async def shutdown(self) -> None:
        """Close underlying sessions.

        Notes
        -----
        Should only be called once.
        """

        assert self._requests
        await self._requests.close()

        if self._server:
            await self._scheduler.close()
            await self._server.close()

    async def _call_listeners(self, funcs: List[Coroutine],
                              webhook: WebhookModel) -> None:
        """Used to call listeners.

        Parameters
        ----------
        funcs : List[Coroutine]
            List of funcs to call.
        webhook : WebhookModel
            WebhookModel to pass.

        Notes
        -----
        Should be spawned with self._scheduler.spawn
        """

        assert self._server

        for func in funcs:
            func(webhook=webhook)

    def listener(self, command: Command):
        """Used to listen to command.

        Parameters
        ----------
        command : Command

        Notes
        -----
        Webhook server must be enabled.
        """

        assert self._server

        def decorator(func):
            @wraps(func)
            async def _add_listener(*args, **kwargs):
                # Keep it simple and just overwrite the command
                # every time the script is started.
                command_id = (await self.create_command(command)).id

                if command_id not in self._global_funcs:
                    self._global_funcs[command_id] = []

                self._global_funcs[command_id].append(func)

            return _add_listener

        return decorator

    def webhook(self, ed25519: str, timestamp: str,
                body: bytes) -> WebhookModel:
        """Used to validate webhook.

        Parameters
        ----------
        ed25519 : str
            X-Signature-Ed25519 header.
        timestamp : str
            X-Signature-Timestamp header.
        body : bytes
            Request body.

        Raises
        ------
        WebhookException
            InvalidJson
            InvalidSignature

        Returns
        -------
        WebhookModel
        """

        try:
            self._verify_key.verify(
                (ed25519 + str(body)).encode(),
                bytes.fromhex(timestamp)
            )
        except BadSignatureError:
            raise InvalidSignature()

        try:
            json = JSONDecoder(body)
        except JSONDecodeError:
            raise InvalidJson()

        return WebhookModel(**json)

    def guild(self, guild_id: str) -> Guild:
        """Used to interact with guild.

        Parameters
        ----------
        guild_id : str

        Returns
        -------
        Guild
        """

        return Guild(self, guild_id)

    async def commands(self) -> AsyncGenerator[CommandModel, None]:
        """Used to list global commands.

        Yields
        -------
        CommandModel
        """

        data = await self._get(
            "applications/{}/commands".format(self._client_id)
        )

        for command in data:
            yield CommandModel(**command)

    async def create_command(self, command: Command) -> CommandModel:
        """Used to create a global command.

        Parameters
        ----------
        command : Command

        Returns
        -------
        CommandModel
        """

        command_model = CommandModel(
            **(
                await self._post(
                    "applications/{}/commands".format(self._client_id),
                    payload=command._payload
                )
            )
        )

        return command_model
