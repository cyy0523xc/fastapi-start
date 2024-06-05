# -*- coding: utf-8 -*-
#
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from uuid import uuid1
from enum import Enum
from typing import List, Dict
from fastapi import Request, FastAPI, Header
from fastapi.routing import APIRoute
from itertools import product

from exceptions import InternalException, status
from .schema import TokenParams


def create_token(data: TokenParams, expire: int) -> str:
    """生成Token
    Args:
        data (TokenParams): _description_
    Returns:
        str: _description_
    """
    path_params_keys = [p[0] for p in data.path_params]
    if len(set(path_params_keys)) != len(data.path_params):
        raise InternalException(status.HTTP_400_BAD_REQUEST, message=f"path_params的key参数必须唯一: {path_params_keys}")

    data_dict = data.dict()
    token = str(uuid1())
    # 保存token
    return token


def get_token_data(token: str = Header(...), req: Request = None) -> TokenParams:
    """
    获取token数据
    """
    # 根据token获取token数据
    token_data = TokenParams()

    def _check_path_params(path_params: dict):
        """校验路径参数"""
        auth_path_params = token_data.get_path_params()
        for key, val in path_params:
            if key in auth_path_params and auth_path_params[key]:
                if val not in auth_path_params[key]:     # 需要校验参数
                    raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限, 路径参数校验不通过, key: {key}, val: {val}")

    if token_data.auth_tags or token_data.path_params:     # 需要校验权限
        app_route: APIRoute = req.scope["route"]
        if not _check_tags(token_data.auth_tags, app_route.tags):    # 校验权限tag
            raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限: {token_data.auth_tags} not in {app_route.tags}")

        # path_params
        _check_path_params(req.path_params)

    return True


def _check_tags(token_tags: List[str], route_tags: List[str]) -> bool:
    tags_set = set(route_tags)
    for tag in token_tags:
        if tag in tags_set:
            return True
    return False
