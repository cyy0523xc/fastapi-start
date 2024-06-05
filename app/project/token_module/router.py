# -*- coding: utf-8 -*-
#
# 模块路由文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
# from typing import Dict
from fastapi import APIRouter
# from fastapi import Depends, HTTPException

from common.encrypt import md5_signature_verify, dict_serialize
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
    # 检验签名
    password = ""
    if not md5_signature_verify(dict_serialize(params.data.dict()), password, params.signature):
        raise InternalException(status.HTTP_601_SIGN_VERIFY_ERROR)

    # 生成token
    token = create_token(params.data, params.expire)
    return {'token': token}
