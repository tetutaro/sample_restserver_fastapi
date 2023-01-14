#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""The module defines internal errors
"""
from __future__ import annotations


class SampleError(Exception):
    """base exception

    Attributes:
        status_code (int): Status code
        error (str): Exception name
        description (str): Description of the exception
        item_id (str): item ID
    """

    status_code: int = 400
    error: str = "Error"
    description: str = "Base exception"
    item_id: str = ""


class SampleErrorNotFound(SampleError):
    """the item is not found

    Args:
        item_id (str): item ID

    Attributes:
        status_code (int): 404
        error (str): ItemNotFound
        detail (str): The requested item is not found.
        item_id (str): item ID
    """

    status_code: int = 404
    error: str = "ItemNotFound"
    description: str = "The requested item is not found."
    item_id: str = ""

    def __init__(self: SampleErrorNotFound, item_id: str) -> None:
        self.item_id = item_id
        self.description = f"The requested item ({item_id}) is not found."
        return


class SampleErrorFound(SampleError):
    """the item is found

    Args:
        item_id (str): item ID

    Attributes:
        status_code (int): 409
        error (str): ItemFound
        detail (str): The requested item is found.
        item_id (str): item ID
    """

    status_code: int = 409
    error: str = "ItemFound"
    description: str = "The requested item is found."
    item_id: str = ""

    def __init__(self: SampleErrorFound, item_id: str) -> None:
        self.item_id = item_id
        self.description = f"The requested item ({item_id}) is found."
        return
