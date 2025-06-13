# -*- coding: utf-8 -*-
#
# 工具函数库
# Author: alex
# Created Time: 2021年06月09日 星期三
import os

# 版本
# 0.6.7: add virtualenv
# 0.6.8: 优化config命令
# 0.6.10: 优化项目名字的长度限制；允许在已有目录中创建项目
# 0.6.11: 优化项目初始化及创建命令
# 0.7.0: 增加快速从已有数据库或者表中生成模型文件功能
# 0.8.0: 增加http的post和get统一封装，增加logger日志统一封装，优化配置文件
# 0.8.1: 完善异常与日志记录
# 0.8.2: 增加token内置模块
# 0.8.3: 实现自定义模块的自动加载
# 0.8.4: 规范化代码；创建文件时，文件名支持-符号；增加 ruff 代码风格检查
VERSION = "0.8.4"

# 包跟目录
package_path = os.path.dirname(os.path.realpath(__file__))
