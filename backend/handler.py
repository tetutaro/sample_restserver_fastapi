#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""handler module that handle the request
"""
from __future__ import annotations
import re
from logging import Logger

from backend.dto import (
    SampleNumericItem,
    SampleTextItem,
    SampleCount,
)
from backend.error import (
    SampleErrorNotFound,
    SampleErrorFound,
)


class SampleHandler:
    """handle the request.

    Args:
        logger (Logger): logger instance
    """

    def __init__(self: SampleHandler, logger: Logger) -> None:
        self.logger = logger
        return

    def insert_number(self: SampleHandler, item: SampleNumericItem) -> None:
        """insert the numeric item

        Args:
            item (SampleNumericItem): the numeric item

        Raises:
            SampleErrorFound:
                length of ID != 4 or ID contains non-numeric charactor(s)
        """
        match = re.match(r"^[0-9]{4}$", item.item_id)
        if match is None:
            raise SampleErrorFound(item_id=item.item_id)
        return

    def insert_text(self: SampleHandler, item: SampleTextItem) -> None:
        """insert the text item

        Args:
            item (SampleTextItem): the text item

        Raises:
            SampleErrorFound:
                length of ID != 4 or ID contains non-alphabet charactor(s)
        """
        match = re.match(r"^[a-zA-Z]{4}$", item.item_id)
        if match is None:
            raise SampleErrorFound(item_id=item.item_id)
        return

    def delete(self: SampleHandler, item_id: str) -> None:
        """delete the item

        Args:
            item_id (str): the numeric item ID

        Raises:
            SampleErrorNotFound:
                length of ID != 4 or
                ID contains non-numeric & non-alphabet charactor(s)
        """
        match = re.match(r"[0-9a-zA-Z]{4}$", item_id)
        if match is None:
            raise SampleErrorNotFound(item_id=item_id)
        return

    def refer_number(self: SampleHandler, item_id: str) -> SampleNumericItem:
        """refer the numeric item

        Args:
            item_id (str): the numeric item ID

        Returns:
            SampleNumericItem: the numeric item

        Raises:
            SampleErrorNotFound:
                length of ID != 4 or ID contains non-numeric charactor(s)
        """
        if len(item_id) != 4:
            raise SampleErrorNotFound(item_id=item_id)
        match = re.match(r"^[0-9]$", item_id)
        if match is not None:
            raise SampleErrorNotFound(item_id=item_id)
        return SampleNumericItem(
            **{
                "item_id": item_id,
                "number": 5,
            }
        )

    def refer_text(self: SampleHandler, item_id: str) -> SampleTextItem:
        """refer the text item

        Args:
            item_id (str): the text item ID

        Returns:
            SampleTextItem: the text item

        Raises:
            SampleErrorNotFound:
                length of ID != 4 or ID contains non-alphabet charactor(s)
        """
        if len(item_id) != 4:
            raise SampleErrorNotFound(item_id=item_id)
        match = re.match(r"^[a-zA-Z]$", item_id)
        if match is not None:
            raise SampleErrorNotFound(item_id=item_id)
        return SampleTextItem(
            **{
                "item_id": item_id,
                "text": "hogehoge",
            }
        )

    def count(self: SampleHandler) -> SampleCount:
        """get the number of items

        Returns:
            SampleCount: the number of items
        """
        return SampleCount(
            **{
                "count_numeric": 123,
                "count_text": 456,
            }
        )
