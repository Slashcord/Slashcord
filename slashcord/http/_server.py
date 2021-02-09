from aiohttp import web


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

    async def start(self) -> None:
        """Used to start lightweight HTTP server.
        """

        await self._runner.setup()
        site = web.TCPSite(self._runner, self._ip, self._port)
        await site.start()

    async def handler(self, request: web.Request) -> web.json_response:
        """Used to handle HTTP request.

        Parameters
        ----------
        request : web.Request

        Returns
        -------
        web.json_response
        """

        return web.json_response()
