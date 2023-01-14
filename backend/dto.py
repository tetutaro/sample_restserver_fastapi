#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""The module defines API (Data Transfer Object)
"""
from __future__ import annotations
import re

from pydantic import BaseModel, Field, validator


def check_version(version: str) -> str:
    """validate version

    Args:
        version (str): the version of backend server

    Returns:
        str: the version which passes the check

    Raises:
        ValueError: format validation of version
    """
    match = re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", version)
    if match is None:
        raise ValueError(f"wrong version: {version}")
    return version


def check_item_id(item_id: str) -> str:
    """validate function of item ID

    Args:
        item_id (str): item ID

    Returns:
        str: item ID which passes the check

    Raises:
        ValueError: format violation of item ID
    """
    match = re.match(r"^[0-9a-zA-Z]{4}$", item_id)
    if match is None:
        raise ValueError(f"wrong item ID: {item_id}")
    return item_id


def check_number(number: int) -> int:
    """validate function of number

    Args:
        number (int): the number which the numeric item contains

    Returns:
        int: the number which passes the check

    Raises:
        ValueError: format violation of number
    """
    if number < 1 or number > 10:
        raise ValueError(f"wrong number: {number}")
    return number


def check_text(text: str) -> str:
    """validate function of text

    Args:
        text (str): the text which the text item contains

    Returns:
        int: the number which passes the check

    Raises:
        ValueError: format violation of text
    """
    if len(text) < 1 or len(text) > 10:
        raise ValueError(f"wrong text: {text}")
    return text


class SampleVersion(BaseModel):
    """the version of backend server

    Attributes:
        version (str): the version of backend server
    """

    version: str = Field(..., example="the version of backend server")
    # validation
    _validated_version: str = validator("version")(check_version)


class SampleWSGIServer(BaseModel):
    """the WSGI server name

    Attributes:
        wsgi_server (str): the name of WSGI server
    """

    wsgi_server: str = Field(..., example="the name of WSGI server")


class SampleNumericItem(BaseModel):
    """the item contains number

    Attributes:
        item_id (str): item ID
        number (int): the number the item contains
    """

    item_id: str = Field(..., example="item ID")
    number: int = Field(..., example="the number the item contains")
    # validation
    _validated_item_id: str = validator("item_id", allow_reuse=True)(
        check_item_id
    )
    _validated_number: str = validator("number")(check_number)


class SampleTextItem(BaseModel):
    """the item contains text

    Attributes:
        item_id (str): item ID
        text (str): the text the item contains
    """

    item_id: str = Field(..., example="item ID")
    text: str = Field(..., example="the text the item contains")
    # validation
    _validated_item_id: str = validator("item_id", allow_reuse=True)(
        check_item_id
    )
    _validated_text: str = validator("text")(check_text)


class SampleCount(BaseModel):
    """保持されている文書数

    Attributes:
        count_numric (int): the number of numeric items
        count_text (int): the number of text items
    """

    count_numeric: int = Field(..., example="the number of numeric items")
    count_text: int = Field(..., example="the number of text items")
