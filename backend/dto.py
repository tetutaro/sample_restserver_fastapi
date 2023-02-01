#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""The module defines API (Data Transfer Object)
"""
from __future__ import annotations
import re

from pydantic import BaseModel, Field, validator


class SampleHealth(BaseModel):
    """health check

    Attributes:
        health (str): dummy string
    """

    health: str = Field(..., example="OK")


class SampleVersion(BaseModel):
    """the version of backend server

    Attributes:
        version (str): the version of backend server
    """

    version: str = Field(..., example="the version of backend server")

    # validation
    @validator("version")
    def check_version(cls: SampleVersion, version: str) -> str:
        if re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version) is None:
            raise ValueError(f"wrong version: {version}")
        return version


class SampleWSGIServer(BaseModel):
    """the WSGI server name

    Attributes:
        wsgi_server (str): the name of WSGI server
    """

    wsgi_server: str = Field(..., example="the name of WSGI server")


class SampleItem(BaseModel):
    """the basic class of SampleNumericItem and SampleTextItem
    to check item_id in common

    Attributes:
        item_id (str): item ID
    """

    item_id: str = Field(..., example="item ID")

    # validation
    @validator("item_id")
    def check_item_id(cls: SampleItem, item_id: str) -> str:
        if re.match(r"^[0-9a-zA-Z]{4}$", item_id) is None:
            raise ValueError(f"wrong item ID: {item_id}")
        return item_id


class SampleNumericItem(SampleItem):
    """the item contains number

    Attributes:
        item_id (str): item ID
        number (int): the number the item contains
    """

    number: int = Field(..., example="the number the item contains")

    # validation
    @validator("number")
    def check_number(cls: SampleNumericItem, number: int) -> int:
        if number < 1 or number > 10:
            raise ValueError(f"wrong number: {number}")
        return number


class SampleTextItem(SampleItem):
    """the item contains text

    Attributes:
        item_id (str): item ID
        text (str): the text the item contains
    """

    text: str = Field(..., example="the text the item contains")

    # validation
    def check_text(cls: SampleTextItem, text: str) -> str:
        if len(text) < 1 or len(text) > 10:
            raise ValueError(f"wrong text: {text}")
        return text

    _v_text = validator("text")(check_text)


class SampleCount(BaseModel):
    """the number of items (dummy count)

    Attributes:
        count_numric (int): the number of numeric items
        count_text (int): the number of text items
    """

    count_numeric: int = Field(..., example="the number of numeric items")
    count_text: int = Field(..., example="the number of text items")
