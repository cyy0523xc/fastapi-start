# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import List, Dict, Tuple
from pydantic import BaseModel, Field


class TokenParams(BaseModel):
    """token参数
    可以根据需要扩展其他的参数"""
    auth_tags: List[str] = Field([], title="授权tags", description="如果为空则允许访问所有接口")
    path_params: List[Tuple[str, List]] = Field([], title="需要匹配的路由参数", description="路由参数的校验，如果路由参数在参数里则是通过校验，列表的每个参数是一个元组，如参数：(\"task_id\", [12, 13]), 其表示task_id参数的值需要为12或者13")

    def get_path_params(self):
        if not hasattr(self, "dict_path_params"):
             self.dict_path_params = {key: val for key, val in self.path_params}
        return self.dict_path_params


class TokenGenerateParams(BaseModel):
    """token生成接口输入参数"""
    username: str = Field(..., title="用户名")
    expire: int = Field(..., title="token有效期", description="单位：秒")
    signature: str = Field(..., title="参数签名字符串", description="将token相关参数生成签名字符串")
    data: TokenParams = Field(..., title="token数据")


class TokenGenerateResp(BaseModel):
    """token生成接口输出参数"""
    token: str = Field(..., title="生成后的token")
