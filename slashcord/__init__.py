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

from aiohttp import ClientSession

from ._settings import Command, CommandChoice
from ._exceptions import (
    SlashCordException,
    HttpException,
    CommandConfigException,
    InvalidName,
    InvalidDescription,
    InvalidChoiceName
)
from ._guild import Guild
from ._message import Message, Embed
from .http import HttpClient, HttpServer

assert Command, CommandChoice
assert Message, Embed

assert SlashCordException
assert HttpException
assert CommandConfigException
assert InvalidName
assert InvalidDescription
assert InvalidChoiceName


__version__ = "0.0.1"
__url__ = "https://slashcord.readthedocs.io/en/latest/"
__description__ = "Discord's slash commands built for asyncio python."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "MIT"


class SlashCord(HttpClient):
    BASE_URL = "https://discord.com/api/v8/"

    def __init__(self, token: str, client_id: int,
                 public_key: str, ip: str = "localhost",
                 port: int = 8888) -> None:
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
        ip : str, optional
            Ip of webhook server by default "localhost"
        port : int, optional
            Port of webhook server by default 8888

        Notes
        -----
        Calling self.start
        ~~~~~~~~~~~~~~~~~~
        await self.start must be called before using.

        Reverse Proxy
        ~~~~~~~~~~~~~
        For production you should setup a reverse proxy
        for the http server, something like nginx.
        """

        if len(token) == 32:
            self._auth = "Bearer "
        else:
            self._auth = "Bot "

        self._server = HttpServer(ip, port, self)
        self._requests = None

        self._client_id = client_id
        self._public_key = public_key
        self._auth += token

    async def start(self) -> None:
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

        await self._server.start()

    async def close(self) -> None:
        """Close underlying sessions.

        Notes
        -----
        Should only be called once.
        """

        assert self._requests
        await self._requests.close()

    def guild(self, guild_id: int) -> Guild:
        """Used to interact with guild.

        Parameters
        ----------
        guild_id : int

        Returns
        -------
        Guild
        """

        return Guild(self, guild_id)

    async def commands(self) -> None:
        await self._get(
            "applications/{}/commands".format(self._client_id)
        )

    async def create_command(self, command: Command) -> None:
        await self._post(
            "applications/{}/commands".format(self._client_id),
            payload=command._payload
        )
