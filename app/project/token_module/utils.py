# -*- coding: utf-8 -*-
#
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from uuid import uuid1
from typing import List, Dict, Tuple
from fastapi import Request, Header
from fastapi.routing import APIRoute

from exceptions import InternalException, status
from .schema import TokenParams


def create_token(data: TokenParams, expire: int) -> str:
    """生成Token
    Args:
        data (TokenParams): token数据
    Returns:
        str: token key
    """
    path_params_keys = [p[0] for p in data.path_params]
    if len(set(path_params_keys)) != len(data.path_params):
        raise InternalException(status.HTTP_400_BAD_REQUEST, message=f"path_params的key参数必须唯一: {path_params_keys}")

    data_dict = data.dict()
    token = str(uuid1())
    # 保存token: 以token为key，将数据存储起来，通常使用redis进行存储
    return token


def get_token_data(token: str = Header(...), req: Request = None) -> TokenParams:
    """获取token数据
    Args:
        token (str, optional): 请求头的token key. Defaults to Header(...).
        req (Request, optional): http请求对象. Defaults to None.
    Raises:
        InternalException: 401
    Returns:
        TokenParams: token数据
    """
    # 根据token参数获取token数据
    token_data = TokenParams()

    if token_data.auth_tags:     # 需要校验的功能权限
        app_route: APIRoute = req.scope["route"]
        if not _check_tags(token_data.auth_tags, app_route.tags):    # 校验权限tag
            raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限: {token_data.auth_tags} not in {app_route.tags}")

    if token_data.path_params:     # 需要校验的路径参数权限
        auth_path_params = token_data.get_path_params()
        for key, val in req.path_params:
            if key in auth_path_params and auth_path_params[key]:
                if val not in auth_path_params[key]:     # 需要校验参数
                    raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限, 路径参数校验不通过, key: {key}, val: {val}")

    # token data 写入req中，方便在中间件中获取
    req.scope["token_data"] = token_data
    return token_data


def _check_tags(token_tags: List[str], route_tags: List[str]) -> bool:
    tags_set = set(route_tags)
    for tag in token_tags:
        if tag in tags_set:
            return True
    return False
