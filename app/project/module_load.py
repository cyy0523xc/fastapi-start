# -*- coding: utf-8 -*-
#
# 模块自动加载
# Author: alex cai
# Email: caiyingyao@ibbd.net
# Created Time: 2024-07-05
from enum import Enum
from glob import glob
from fastapi import FastAPI
from importlib import import_module

from common.logger import logger


class ModuleAttr(Enum):
    # [必须] 模块对象
    router = "MODULE_ROUTER"
    # [可选] 是否开启该模块，默认为True
    enable = "MODULE_ENABLE"
    # [可选] 模块名
    name = "MODULE_NAME"
    # [可选] 模块路由Tags
    tags = "MODULE_ROUTE_TAGS"


def module_auto_load(app: FastAPI):
    """模块自动加载"""
    module_paths = glob("*_module")
    for path in module_paths:
        logger.info(f"加载模块: {path}")
        __load_module(app, path)
        logger.info(f"成功加载工具: {path}")


def __load_module(app: FastAPI, module_name: str):
    """加载模块，实现类似效果：
    from token_module import router
    app.include_router(router, prefix="/token", tags=["token"])

    Args:
        module_name (str): token_module
    Raises:
        ValueError: _description_
    """
    assert module_name.endswith('_module')
    try:
        # 动态导入模块
        module = import_module(module_name)
    except Exception as e:
        raise Exception(f"模块 {module_name} 导入异常: {e}")

    # 模块是否开启
    try:
        module_enable = getattr(module, ModuleAttr.enable.value)
    except Exception as e:
        module_name = True
    if not module_enable:
        logger.info(f"该模块处于关闭状态：{module_name}")
        return

    # 获取模块中的路由器
    try:
        router = getattr(module, ModuleAttr.router.value)
    except Exception as e:
        raise Exception(f"Module {module_name} does not have a '{ModuleAttr.router.value}' attribute: {e}")

    # 获取模块的tags
    try:
        router_tags = getattr(module, ModuleAttr.tags.value)
    except Exception as e:
        router_tags = []

    # 将路由器添加到FastAPI应用中
    route_prefix = "/" + module_name[:-len("_module")]
    app.include_router(router, prefix=route_prefix, tags=router_tags)


if __name__ == "__main__":
    pass
