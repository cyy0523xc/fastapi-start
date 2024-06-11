# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import List
from pydantic import BaseModel, Field

from common.encrypt import md5_signature_verify, dict_serialize


class TokenParams(BaseModel):
    """token接口参数
    可以根据需要扩展其他的参数"""
    auth_tags: List[str] = Field(..., title="授权tags", description="如果为空则允许访问所有接口")

    # 路由中的参数样例
    tasks_id: List[int] = Field(..., title="路由中的任务ID列表", description="用于限制该token可以访问的任务ID")


class TokenGenerateParams(BaseModel):
    """token生成接口输入参数"""
    username: str = Field(..., title="用户名")
    expire: int = Field(86400, title="token有效期", description="单位：秒")
    signature: str = Field(..., title="参数签名字符串", description="将token相关参数生成签名字符串")
    data: TokenParams = Field(..., title="token数据")

    def verify_signature(self, password: str) -> bool:
        """校验签名
        Returns:
            bool: 签名校验是否成功
        """
        return md5_signature_verify(dict_serialize(self.data.dict()), password, self.signature)


class TokenData(TokenParams):
    """Token数据(存储的数据)，可以根据需要进行扩展更多的字段
    """
    user_id: int = Field(..., title="用户ID")


class TokenGenerateResp(BaseModel):
    """token生成接口输出参数"""
    token: str = Field(..., title="生成后的token")
    user_id: int = Field(..., title="用户ID")
