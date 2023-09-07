from __future__ import annotations

from pydantic import BaseModel, root_validator
from datetime import datetime, timezone
from typing import Annotated, Any, TypedDict

from fastapi import (
    Body,
    Depends,
    Header,
    HTTPException,
    Response,
    status,
)

from diracx.core.config import Config, ConfigSource
from diracx.routers.auth import UserInfo, has_properties, verify_dirac_token

from diracx.routers.fastapi_classes import DiracxRouter
from diracx_extension.db.ext.db import extDB

LAST_MODIFIED_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"

router = DiracxRouter()

class CustomObject(TypedDict):
    PathValueAsString: str
    IntegerValue: int

EXAMPLE_CUSTOMOBJECT = {
 "PathValueAsString": "/example/test",
 "IntegerValue": 1,
}

EXAMPLE_PATHVALUE = "/example/test"

@router.get("/example/search/{path_value:path}")
async def get_example_object(
    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    ext_db: Annotated[extDB, Depends(extDB.transaction)],
    path_value: Annotated[str, Body(examples=EXAMPLE_PATHVALUE)],

):
    return await ext_db.search(path_value)

@router.post("/example/post")
async def post_object(
    user_info: Annotated[UserInfo, Depends(verify_dirac_token)],
    ext_db: Annotated[extDB, Depends(extDB.transaction)],
    body: Annotated[CustomObject, Body(examples=EXAMPLE_CUSTOMOBJECT)],

):
    return await ext_db.insert(body["PathValueAsString"],body["IntegerValue"])
