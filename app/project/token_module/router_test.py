# -*- coding: utf-8 -*-
#
# 接口单元测试脚本（使用pytest）
#     sudo docker exec -ti container_name pytest token_module/router_test.py
#
# Author: __author__
# Email: __email__
# Created Time: __created_time__
import sys
from pathlib import Path

run_path = Path(__file__).parent.parent.as_posix()
if run_path not in sys.path:
    print(f"增加路径: {run_path}")
    sys.path.insert(0, run_path)
print("运行目录:", run_path)


def test_api():
    """单元测试代码"""
    assert 1 == 1
