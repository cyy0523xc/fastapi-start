# -*- coding: utf-8 -*-
#
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from uuid import uuid1
from typing import List
from fastapi import Request, FastAPI
from fastapi.routing import APIRoute

from exceptions import InternalException, status
from .schema import TokenParams


def create_token(data: TokenParams, expire: int) -> str:
    """生成Token
    Args:
        data (TokenParams): _description_
    Returns:
        str: _description_
    """
    data_dict = data.dict()
    token = str(uuid1())
    # 保存token
    return token


def check_token(token: str, app: FastAPI, req: Request) -> bool:
    """
    验证token
    """
    def _check_path_params(path_params: dict):
        for key, val in path_params:
            if key in token_data.path_params and token_data.path_params[key]:
                if val not in token_data.path_params[key]:     # 需要校验参数
                    raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限, 路径参数校验不通过, key: {key}, val: {val}")

    # 获取token数据
    token_data = TokenParams()
    if token_data.api_tags or token_data.path_params:
        for r in app.routes:
            if isinstance(r, APIRoute) and r.tags and req.method in r.methods:
                # 根据route tags进行权限过滤
                _, match = r.matches(req)
                if not match:
                    continue
                # print(r.path, r.tags, match, match.items(), flush=True)
                if not _check_tags(token_data.api_tags, r.tags):    # 权限不匹配
                    raise InternalException(status.HTTP_401_UNAUTHORIZED, f"没有访问该接口的权限: {token_data.api_tags} not in {r.tags}")

                # path_params
                _check_path_params(match['path_params'])
                break
    return True


def _check_tags(token_tags: List[str], route_tags: List[str]) -> bool:
    tags_set = set(route_tags)
    for tag in token_tags:
        if tag in tags_set:
            return True
    return False
