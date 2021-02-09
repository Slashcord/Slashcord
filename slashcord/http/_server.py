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

        webhook

        return self.__response()
