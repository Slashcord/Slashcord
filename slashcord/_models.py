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

from typing import Any, Dict, List
from datetime import datetime


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"


class Option:
    name: str
    value: str

    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value


class Data:
    options: List[Option]
    name: str
    id: str

    def __init__(self, options: List[str], name: str, id: str) -> None:
        self.options = [Option(option) for option in options]
        self.name = name
        self.id = id


class User:
    id: int
    username: str
    avatar: str
    discriminator: int
    public_flags: int

    def __init__(self, id: int, username: str, avatar: str, discriminator: int,
                 public_flags: int) -> None:
        self.id = id
        self.username = username
        self.avatar = avatar
        self.discriminator = discriminator
        self.public_flags = public_flags


class Member:
    user: User
    roles: List[str]
    premium_since: datetime
    permissions: int
    pending: bool
    nick: str
    mute: bool
    joined_at: datetime
    is_pending: bool
    deaf: bool

    def __init__(self, user: User, roles: List[str], premium_since: str,
                 permissions: int, pending: bool,
                 nick: str, mute: bool, joined_at: str,
                 is_pending: bool, deaf: bool) -> None:

        self.user = user
        self.roles = roles
        self.premium_since = datetime.strptime(
            premium_since, TIMESTAMP_FORMAT
        ) if premium_since else None
        self.permissions = permissions
        self.pending = pending
        self.nick = nick
        self.mute = mute
        self.joined_at = datetime.strptime(joined_at, TIMESTAMP_FORMAT)
        self.is_pending = is_pending
        self.deaf = deaf


class WebhookModel:
    type: int
    token: str
    member: Member
    id: str
    guild_id: str
    data: Data
    channel_id: str

    def __init__(self, type: int, token: str, member: Dict[str, Any], id: str,
                 guild_id: str, data: Data, channel_id: str) -> None:

        self.type = type
        self.token = token
        self.member = Member(member)
        self.id = id
        self.guild_id = guild_id
        self.data = data
        self.channel_id = channel_id


class CommandModel:
    id: str
    application_id: str
    name: str
    description: str
    version: str

    def __init__(self, id: str, application_id: str, name: str,
                 description: str, version: str, *args, **kwargs) -> None:
        self.id = id
        self.application_id = application_id
        self.name = name
        self.description = description
        self.version = version
