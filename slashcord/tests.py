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

import asynctest

from . import SlashCord, Command, CommandChoice, CommandModel


class TestSlashCord(asynctest.TestCase):
    use_default_loop = True

    token: str
    client_id: int
    public_key: str
    guild_id: int

    async def setUp(self) -> None:
        self.slash_cord = SlashCord(
            token=self.token,
            client_id=self.client_id,
            public_key=self.public_key
        )

        self.guild = self.slash_cord.guild(self.guild_id)

        await self.slash_cord.startup()

    async def tearDown(self) -> None:
        await self.slash_cord.shutdown()

    async def test_getting_commads(self) -> None:
        async for command in self.slash_cord.commands():
            self.assertIsInstance(command, CommandModel)

    async def test_string_create_command(self) -> None:
        model = await self.guild.create_command(
            Command(
                name="testing",
                description="Command created by SlashCord for testing"
            ).option(
                name="choice",
                description="Choices you can select",
                required=True
            ).string([
                CommandChoice("Choice 1", "choice_1"),
                CommandChoice("Choice 2", "choice_2")
            ])
        )

        self.assertIsInstance(model, CommandModel)
