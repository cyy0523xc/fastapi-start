# -*- coding: utf-8 -*-
#
# 模块路由配置文件
# Author: __author__
# Email: __email__
# Created Time: __created_time__
from typing import List, Dict, Tuple
from pydantic import BaseModel, Field

from common.encrypt import md5_signature_verify, dict_serialize


class TokenParams(BaseModel):
    """token参数
    可以根据需要扩展其他的参数"""
    auth_tags: List[str] = Field(..., title="授权tags", description="如果为空则允许访问所有接口")
    # 为了保证签名的唯一性，这里不定义为字典，否则在反序列化的时候就比较麻烦
    path_params: List[Tuple[str, List]] = Field(..., title="需要匹配的路由参数", description="路由参数的校验，如果路由参数在参数里则是通过校验，列表的每个参数是一个元组，如参数：(\"task_id\", [12, 13]), 其表示task_id参数的值需要为12或者13")

    def get_path_params(self) -> Dict[str, List]:
        return {key: val for key, val in self.path_params}

    def get_path_params_set(self) -> Dict[str, set]:
        return {key: set(val) for key, val in self.path_params}


class TokenGenerateParams(BaseModel):
    """token生成接口输入参数"""
    username: str = Field(..., title="用户名")
    expire: int = Field(..., title="token有效期", description="单位：秒")
    signature: str = Field(..., title="参数签名字符串", description="将token相关参数生成签名字符串")
    data: TokenParams = Field(..., title="token数据")

    def verify_signature(self, password: str) -> bool:
        """校验签名
        Returns:
            bool: 签名校验是否成功
        """
        return md5_signature_verify(dict_serialize(self.data.dict()), password, self.signature)


class TokenGenerateResp(BaseModel):
    """token生成接口输出参数"""
    token: str = Field(..., title="生成后的token")
    user_id: int = Field(..., title="用户ID")
    # 下面这两个权限参数和输入的不一定一致，因为这还和用户的权限相关
    auth_tags: List[str] = Field(..., title="授权tags", description="如果为空则允许访问所有接口")
    path_params: List[Tuple[str, List]] = Field(..., title="需要匹配的路由参数", description="路由参数的校验，如果路由参数在参数里则是通过校验，列表的每个参数是一个元组，如参数：(\"task_id\", [12, 13]), 其表示task_id参数的值需要为12或者13")
