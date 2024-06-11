# -*- coding: utf-8 -*-
#
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from uuid import uuid1
from typing import List
from fastapi import Request, Header
from fastapi.routing import APIRoute

from exceptions import InternalException, status
from .schema import TokenData


def create_token(data: TokenData, expire: int) -> str:
    """生成Token
    Args:
        data (TokenData): token数据
    Returns:
        str: token key
    """
    token = str(uuid1())
    # TODO 保存token: 以token为key，将数据存储起来，通常使用redis进行存储
    return token


def valid_token(token: str = Header(...), req: Request = None) -> TokenData:
    """校验token
    Args:
        token (str, optional): 请求头的token key. Defaults to Header(...).
        req (Request, optional): http请求对象. Defaults to None.
    Raises:
        InternalException: 401
    Returns:
        TokenParams: token数据
    """
    # 根据token参数获取token数据
    token_data = TokenData()

    if token_data.auth_tags:     # 需要校验的功能权限
        app_route: APIRoute = req.scope["route"]
        if not _check_tags(token_data.auth_tags, app_route.tags):    # 校验权限tag
            raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限: {token_data.auth_tags} not in {app_route.tags}")

    if token_data.tasks_id and "task_id" in req.path_params and req.path_params["task_id"] not in token_data.tasks_id:     # 需要校验的路径参数权限: task id
        raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限, 路径参数校验不通过 task_id: {req.path_params['task_id']} not in {token_data.tasks_id}")

    # token data 写入req中，方便在中间件中获取
    req.scope["token_data"] = token_data
    return token_data


def _check_tags(token_tags: List[str], route_tags: List[str]) -> bool:
    tags_set = set(route_tags)
    for tag in token_tags:
        if tag in tags_set:
            return True
    return False
