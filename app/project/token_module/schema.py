# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import List, Dict
from pydantic import BaseModel, Field


class TokenParams(BaseModel):
    """token参数
    可以根据需要扩展其他的参数"""
    api_tags: List[str] = Field([], title="允许访问的接口tags", description="如果为空则允许访问所有接口")
    page_tags: List[str] = Field([], title="允许访问的页面tags", description="如果为空则允许访问所有页面")
    path_params: Dict[str, List] = Field({}, title="需要匹配的路由参数", description="路由参数的校验，如果路由参数在参数里则是通过校验")


class TokenGenerateParams(BaseModel):
    """token生成接口输入参数"""
    username: str = Field(..., title="用户名")
    expire: int = Field(..., title="token有效期", description="单位：秒")
    signature: str = Field(..., title="参数签名字符串", description="将token相关参数生成签名字符串")
    params: TokenParams = Field(..., title="token相关参数")


class TokenGenerateResp(BaseModel):
    """token生成接口输出参数"""
    token: str = Field(..., title="生成后的token")
