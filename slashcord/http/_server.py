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

from aiohttp import web

from .._exceptions import InvalidSignature, InvalidJson
from .._models import WebhookModel


class HttpServer:
    def __init__(self, ip: str, port: int, upper: object) -> None:
        """Used to create a lightweight HTTP server.

        Parameters
        ----------
        ip : str
        port : int
        upper : object
            SlashCord instance
        """

        self._server = web.Server(self.handler)
        self._runner = web.ServerRunner(self._server)

        self._ip = ip
        self._port = port
        self._upper = upper

    def __response(data: dict = None, error: str = False,
                   status_code: int = 200) -> web.json_response:
        """Used to respond to a request.

        Parameters
        ----------
        data : dict, optional
            by default None
        error : str, optional
            by default False
        status_code : int, optional
            by default 200

        Returns
        -------
        web.json_response
        """

        return web.json_response(
            {"data": data, "error": error},
            status=500 if error and status_code == 200 else status_code
        )

    async def start(self) -> None:
        """Used to start lightweight HTTP server.
        """

        await self._runner.setup()
        site = web.TCPSite(self._runner, self._ip, self._port)
        await site.start()

    async def close(self) -> None:
        """Closes lightweight HTTP server.
        """

        await self._runner.cleanup()

    async def handler(self, request: web.Request) -> web.json_response:
        """Used to handle HTTP request.

        Parameters
        ----------
        request : web.Request

        Returns
        -------
        web.json_response
        """

        if request.method != "POST":
            return self.__response(error="Invalid method", status_code=405)

        if ("X-Signature-Ed25519" not in request.headers
                or "X-Signature-Timestamp" not in request.headers):
            return self.__response(error="Missing headers", status_code=400)

        body = await request.read()

        try:
            webhook: WebhookModel = self._upper.webhook(
                request.headers["X-Signature-Ed25519"],
                request.headers["X-Signature-Timestamp"],
                body
            )
        except InvalidSignature:
            return self.__response(
                error="Invalid request signature", status_code=401
            )
        except InvalidJson:
            return self.__response(error="Invalid json", status_code=400)

        # Handles calling the event listeners.
        if webhook.id in self._upper._global_commands:

            await self._upper._call_listeners(
                self._upper._global_commands[webhook.id],
                webhook
            )

        elif (webhook.guild_id in self._upper._guild_commands and
                webhook.id in self._upper._guild_commands[webhook.guild_id]):

            await self._upper._call_listeners(
                self._upper._guild_commands[webhook.guild_id][webhook.id],
                webhook
            )

        return self.__response({"type": webhook.type})
