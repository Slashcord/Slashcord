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
                 color: int = None) -> None:
        """Used to create embed.

        Parameters
        ----------
        title : str, optional
            by default None
        description : str, optional
            by default None
        url : str, optional
            by default None
        timestamp : datetime, optional
            by default None
        color : int, optional
            by default None
        """

        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color

        self._footer = None
        self._image = None
        self._thumbnail = None
        self._video = None
        self._provider = None
        self._author = None

        self._fields = []

    @property
    def _playload(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "timestamp": self.timestamp.timestamp(),
            "color": self.color,
            "footer": self._footer,
            "image": self._image,
            "thumbnail": self._thumbnail,
            "video": self._video,
            "provider": self._provider,
            "author": self._author,
            "fields": self._fields
        }

    def add_footer(self, text: str,
                   icon_url: str = None) -> Embed:
        """Used to add footer.

        Parameters
        ----------
        text : str
        icon_url : str, optional
            by default None

        Returns
        -------
        Embed
        """

        self._footer = {
            "text": text,
            "icon_url": icon_url
        }

        return self

    def add_image(self, url: str, height: int = None,
                  width: int = None) -> Embed:
        """Used to add image.

        Parameters
        ----------
        url : str
        height : int, optional
            by default None
        width : int, optional
            by default None

        Returns
        -------
        Embed
        """

        self._image = {
            "url": url,
            "height": height,
            "width": width
        }

        return self

    def add_thumbnail(self, url: str, height: int = None,
                      width: int = None) -> Embed:
        """Used to add thumbnail.

        Parameters
        ----------
        url : str
        height : int, optional
            by default None
        width : int, optional
            by default None

        Returns
        -------
        Embed
        """

        self._thumbnail = {
            "url": url,
            "height": height,
            "width": width
        }

        return self

    def add_video(self, url: str, height: int = None,
                  width: int = None) -> Embed:
        """Used to set video.

        Parameters
        ----------
        url : str
        height : int, optional
            by default None
        width : int, optional
            by default None

        Returns
        -------
        Embed
        """

        self._video = {
            "url": url,
            "height": height,
            "width": width
        }

        return self

    def add_provider(self, name: str = None,
                     url: str = None) -> Embed:
        """Used to set provider.

        Parameters
        ----------
        name : str, optional
            by default None
        url : str, optional
            by default None

        Returns
        -------
        Embed
        """

        self._provider = {
            "name": name,
            "url": url
        }

        return self

    def add_author(self, name: str, url: str = None,
                   icon_url: str = None) -> Embed:
        """Used to add author.

        Parameters
        ----------
        name : str
        url : str, optional
            by default None
        icon_url : str, optional
            by default None

        Returns
        -------
        Embed
        """

        self._author = {
            "name": name,
            "url": url,
            "icon_url": icon_url
        }

        return self

    def add_field(self, name: str, value: str, inline: bool = False) -> Embed:
        """Used to add field.

        Parameters
        ----------
        name : str
        value : str
        inline : bool, optional
            by default False

        Returns
        -------
        Embed
        """

        self._fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })

        return self

    def remove_field(self, index: int) -> Embed:
        """Used to remove field.

        Parameters
        ----------
        index : int

        Returns
        -------
        Embed
        """

        self._fields.pop(index)
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

        self._embeds = []
        self._files = []

    @property
    def _playload(self) -> dict:
        return {
            "content": self.content,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "tts": self.tts,
            "embeds": self._embeds,
            "files": self._files
        }

    def add_file(self, file: str, filename: str) -> Message:
        """Used to add file.

        Parameters
        ----------
        file : str
        filename : str

        Returns
        -------
        Message
        """

        self._files["_{}".format(filename)] = (filename, file)
        return self

    def add_embed(self, embed: Embed) -> Message:
        """Used to add embed.

        Parameters
        ----------
        embed : Embed

        Returns
        -------
        Message
        """

        self._embeds.append(embed._playload)
        return self

    def remove_embed(self, index: int) -> Message:
        """Used to remove embed.

        Parameters
        ----------
        index : int

        Returns
        -------
        Message
        """

        self._embeds.pop(index)
        return self
