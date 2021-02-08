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

from __future__ import annotations
from datetime import datetime


class Embed:
    def __init__(self, title: str = None, description: str = None,
                 url: str = None, timestamp: datetime = None,
                 color: bytes = None) -> None:
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color

        self.footer = None
        self.image = None

    @property
    def _playload(self) -> dict:
        pass

    def add_footer(self, text: str,
                   icon_url: str = None) -> Embed:

        self.footer = {
            "text": text,
            "icon_url": icon_url
        }

        return self

    def add_image(self, url: str, height: int = None,
                  width: int = None) -> Embed:

        self.image = {
            "url": url,
            "height": height,
            "width": width
        }

        return self

    def add_field(self) -> Embed:
        return self

    def remove_field(self) -> Embed:
        return self


class Message:
    def __init__(self, content: str = None, username: str = None,
                 avatar_url: str = None, tts: bool = False) -> None:
        """Used to format a message.

        Parameters
        ----------
        content : str, optional
            by default None
        username : str, optional
            by default None
        avatar_url : str, optional
            by default None
        tts : bool, optional
            by default False
        """

        self.content = content
        self.username = username
        self.avatar_url = avatar_url
        self.tts = tts

    @property
    def _playload(self) -> dict:
        pass

    def add_embed(self, embed: Embed) -> Message:
        return self

    def remove_embed(self, embed: Embed) -> Message:
        return self
