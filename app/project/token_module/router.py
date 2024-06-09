# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
# from typing import Dict
from fastapi import APIRouter
# from fastapi import Depends, HTTPException

from exceptions import InternalException, status
from .schema import TokenGenerateParams, TokenGenerateResp
from .utils import create_token

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.post("/generate", summary='token生成接口', response_model=TokenGenerateResp)
async def token_generate_api(
    params: TokenGenerateParams
):
    """token生成接口"""
    # TODO 根据用户名获取用户密码
    password = ""
    user_id = 111

    # 检验签名
    if not params.verify_signature(password):
        raise InternalException(status.HTTP_601_SIGN_VERIFY_ERROR)

    # TODO 获取用户的权限tag
    # 通常是通过用户ID查到用户角色，而角色可以直接关联tag，这些tag可以是定义在api的tags属性中

    # TODO 合并接口输入的权限tag和数据库中的tag

    # 生成token
    token = create_token(params.data, params.expire)
    return TokenGenerateResp(token=token, user_id=user_id,
                             auth_tags=params.data.auth_tags,
                             path_params=params.data.path_params)
