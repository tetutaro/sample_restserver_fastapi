#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""the module that create API and pass the request to the handler
"""
from typing import List, Type, Dict, Optional, Union, Any
import os
from logging import Logger, getLogger

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from backend import __version__
from backend.dto import (
    SampleHealth,
    SampleVersion,
    SampleWSGIServer,
    SampleNumericItem,
    SampleTextItem,
    SampleCount,
)
from backend.error import (
    SampleError,
    SampleErrorNotFound,
    SampleErrorFound,
)
from backend.handler import SampleHandler

# URLs that FastAPI server allows CORS access
allow_origins: List[str] = [
    "http://localhost:3000",
    "http://frontend:3000",
]

# settings for API document
title: str = "Sample Backend"
description: str = "Sample backend server with REST API"
tags_metadata: List[Dict[str, str]] = [
    {
        "name": "Others",
        "description": "Others",
    },
    {
        "name": "Operation",
        "description": "Operation of item",
    },
    {
        "name": "Reference",
        "description": "Reference of item",
    },
]
API_VERSION: str = (
    "v" + "1" if __version__.startswith("0.") else __version__.split(".")[0]
)
openapi_url: str = f"/api/{API_VERSION}/openapi.json"

# Instances
app: FastAPI = FastAPI(
    title=title,
    description=description,
    openapi_tags=tags_metadata,
    version=__version__,
    openapi_url=openapi_url,
    docs_url=None,
    redoc_url=f"/api/{API_VERSION}/redoc",
)  # instance of FastAPI
# mount static directory
app.mount("/icons", StaticFiles(directory="icons"), name="icons")
# add CORS middleware to allow CORS access
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# instance of Logger
wsgi_server: str = os.environ.get("WSGI_SERVER", "uvicorn")
logger: Logger = getLogger(wsgi_server)
# handler instance
handler: SampleHandler = SampleHandler(logger=logger)


def error_response(
    error_types: Optional[List[Type[SampleError]]],
) -> Optional[Dict[Union[int, str], Dict[str, Any]]]:
    """describe error types with OpenAPI format

    Args:
        error_types (Optional[List[Type[SampleError]]]): error types

    Returns:
        Optional[Dict[Union[int, str], Dict[str, Any]]]:
            error types for OpenAPI format
    """
    if error_types is None:
        return None
    d: Dict[Union[int, str], Dict[str, Any]] = dict()
    for et in error_types:
        if not d.get(et.status_code):
            d[et.status_code] = {
                "description": f'"{et.description}"',
                "content": {
                    "application/json": {
                        "example": {
                            "error": et.error,
                            "description": et.description,
                            "item_id": et.item_id,
                        }
                    }
                },
            }
        else:
            d[et.status_code]["description"] += f'<br>"{et.description}"'
    return d


@app.exception_handler(SampleError)
async def backend_error_handler(
    req: Request, err: SampleError
) -> JSONResponse:
    """return error response when raise exception

    Args:
        req (Request): request of FastAPI
        err (SampleError): exception

    Returns:
        JSONResponse: JSON response
    """
    return JSONResponse(
        status_code=err.status_code,
        content={
            "error": f"{err.error}",
            "description": f"{err.description}",
            "item_id": f"{err.item_id}",
        },
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    """display favicon

    Returns:
        FileResponse: favicon.ico
    """
    return FileResponse("icons/favicon.ico")


@app.get(f"/api/{API_VERSION}/docs", include_in_schema=False)
async def swagger_ui_html() -> HTMLResponse:
    """display Swagger UI

    Returns:
        HTMLResponse: Swagger UI Page
    """
    return get_swagger_ui_html(
        title=title,
        openapi_url=openapi_url,
        swagger_favicon_url="/icons/favicon.ico",
    )


@app.get(
    "/health",
    summary="health check",
    status_code=status.HTTP_200_OK,
    tags=["Others"],
    responses=error_response(error_types=None),
)
async def op_health() -> SampleHealth:
    """confirm alive of server (GET `/health`)

    Returns:
        SampleHealth: dummy response
    """
    return SampleHealth(health="OK")


@app.get(
    f"/api/{API_VERSION}/version",
    summary="get version",
    status_code=status.HTTP_200_OK,
    tags=["Others"],
    responses=error_response(error_types=None),
)
async def op_version() -> SampleVersion:
    f"""get version (GET `/api/{API_VERSION}/version`)

    Returns:
        SampleVersion: version number
    """
    logger.info("version")
    return SampleVersion(version=__version__)


@app.get(
    f"/api/{API_VERSION}/wsgi_server",
    summary="get WSGI server name",
    status_code=status.HTTP_200_OK,
    tags=["Others"],
    responses=error_response(error_types=None),
)
async def op_wsgi_server() -> SampleWSGIServer:
    f"""get WSGI server name (GET `/api/{API_VERSION}/wsgi_server`)

    Returns:
        SampleWSGIServer: WSGI server name
    """
    logger.info("wsgi_server")
    return SampleWSGIServer(wsgi_server=wsgi_server)


@app.post(
    f"/api/{API_VERSION}/number",
    summary="insert the numeric item",
    status_code=status.HTTP_201_CREATED,
    tags=["Operation"],
    responses=error_response(
        error_types=[
            SampleErrorFound,
        ]
    ),
)
async def op_insert_number(req: SampleNumericItem) -> None:
    f"""insert the numeric item (POST `/api/{API_VERSION}/number`)

    Args:
        req (SampleNumericItem): the item to insert
    """
    handler.insert_number(item=req)
    return


@app.post(
    f"/api/{API_VERSION}/text",
    summary="insert the text item",
    status_code=status.HTTP_201_CREATED,
    tags=["Operation"],
    responses=error_response(
        error_types=[
            SampleErrorFound,
        ]
    ),
)
async def op_insert_text(req: SampleTextItem) -> None:
    f"""insert the text item (POST `/api/{API_VERSION}/text`)

    Args:
        req (SampleTextItem): the item to insert
    """
    handler.insert_text(item=req)
    return


@app.delete(
    f"/api/{API_VERSION}/delete/{{item_id}}",
    summary="delete the item",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Operation"],
    responses=error_response(
        error_types=[
            SampleErrorNotFound,
        ]
    ),
)
async def op_delete(item_id: str) -> None:
    f"""delete the item (DELETE `/api/{API_VERSION}/delete/{{item_id}}`)

    Args:
        item_id (str): the item ID to delete
    """
    handler.delete(item_id=item_id)
    return


@app.get(
    f"/api/{API_VERSION}/number/{{item_id}}",
    summary="refer the numeric item",
    status_code=status.HTTP_200_OK,
    tags=["Reference"],
    responses=error_response(
        error_types=[
            SampleErrorNotFound,
        ]
    ),
)
async def op_refer_number(item_id: str) -> SampleNumericItem:
    f"""refer the numeric item (GET `/api/{API_VERSION}/number/{{item_id}}`)

    Args:
        item_id (str): the numeric item ID to refer

    Returns:
        SampleNumericItem: the numeric item
    """
    return handler.refer_number(item_id=item_id)


@app.get(
    f"/api/{API_VERSION}/text/{{item_id}}",
    summary="refer the text item",
    status_code=status.HTTP_200_OK,
    tags=["Reference"],
    responses=error_response(
        error_types=[
            SampleErrorNotFound,
        ]
    ),
)
async def op_refer_text(item_id: str) -> SampleTextItem:
    f"""refer the text item (GET `/api/{API_VERSION}/text/{{item_id}}`)

    Args:
        item_id (str): the text item ID to refer

    Returns:
        SampleNumericItem: the text item
    """
    return handler.refer_text(item_id=item_id)


@app.get(
    f"/api/{API_VERSION}/count",
    summary="get the number of items",
    status_code=status.HTTP_200_OK,
    tags=["Reference"],
    responses=error_response(error_types=None),
)
async def op_count() -> SampleCount:
    f"""get the number of items (GET `/api/{API_VERSION}/count`)

    Returns:
        SampleCount: the number of items
    """
    return handler.count()
