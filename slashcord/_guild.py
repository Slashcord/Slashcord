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

from functools import wraps

from ._settings import Command
from ._models import CommandModel


class Guild:
    def __init__(self, upper: object, guild_id: str) -> None:
        self._upper = upper
        self.guild_id = guild_id

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

                if self.guild_id not in self._upper._guild_funcs:
                    self._upper._guild_funcs[self.guild_id] = {}

                if (command_id not in
                        self._upper._guild_funcs[self.guild_id]):
                    self._upper._guild_funcs[self.guild_id][command_id] = []

                self._upper._guild_funcs[self.guild_id][command_id].append(
                    func
                )

            return _add_listener

        return decorator

    async def create_command(self, command: Command) -> CommandModel:
        """Used to create guild command.

        Parameters
        ----------
        command : Command

        Returns
        -------
        CommandModel
        """

        return CommandModel(
            **(
                await self._upper._post(
                    "applications/{}/guilds/{}/commands".format(
                        self._upper._client_id, self.guild_id
                    ),
                    payload=command._payload
                )
            )
        )
