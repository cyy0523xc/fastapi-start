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
from .schema import TokenGenerateParams, TokenGenerateResp, TokenData
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

    # TODO 如果可能，则可以在此对路径参数进行校验
    # 例如参数允许访问task_id=100的任务，但是实际上该用户并没有访问该任务的权限，则可以直接抛出异常信息

    # 生成token
    token_data = TokenData(params.data)
    token_data.user_id = user_id
    token = create_token(token_data, params.expire)
    return TokenGenerateResp(token=token, user_id=user_id)
