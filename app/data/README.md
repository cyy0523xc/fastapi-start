# __title__

本项目使用[`fastapi-start`](https://github.com/ibbd-dev/fastapi-start)工具进行初始化，该工具的帮助可以使用命令：`fas --help`。

__desc__

## 1. 功能介绍

## 2. 安装与部署

部署前需要先复制配置文件：

```sh
cd app/
cp settings-example.py settings.py

# 根据实际情况修改配置文件
vim settings.py

# 启动
# FastAPI文档：https://fastapi.tiangolo.com/
uvicorn main:app --reload
```

## 3. 开发规范

### 3.1 目录规范

```text
project-name
├── app                      # 项目根目录
│   ├── logs                 # 日志保存目录
│   ├── static               # 静态文件目录，主要是FastAPI使用的静态文件
│   ├── common               # 项目公共基础函数和类库目录
│   │   ├── connection.py    # 常用的链接对象，如redis
│   │   ├── encrypt.py       # 常用的加解密函数，如md5/RSA等
│   │   ├── http.py          # http请求基础工具函数
│   │   └── logger.py        # 日志基础工具库
│   ├── example_module       # 接口样例模块，目录名后缀统一为_module
│   │   ├── router.py        # 模块的路由入口
│   │   ├── schema.py        # 模块的 pydantic的模型
│   │   ├── router_test.py   # 模块入口单元测试
│   │   └── README.md        # 模块说明文件
│   ├── schema.py            # 基础接口数据类型
│   ├── readme.md            # FastAPI 接口文档的使用说明
│   ├── main.py              # 项目入口，用于启动 FastAPI 应用程序
│   ├── schema.py            # 基础的pydantic模型
│   ├── init_app.py          # 应用程序初始化相关函数
│   ├── settings_base.py     # 应用程序配置（这里的配置通常是在开发时就固定了）
│   ├── settings-example.py  # 配置的样例文件，实际部署时需要先将该文件复制为：settings.py
│   ├── settings.py          # 项目配置文件（该文件的常量继承自settings_base.py，跟环境相关的常量可以在这个文件中重新定义）
│   ├── database.py          # 数据库相关的基础代码
│   ├── dependencies.py      # 公共路由依赖(Depends)
│   ├── exceptions.py        # 异常处理
│   └── utils.py             # 基础的函数库
├── docs                     # 文档目录
├── vevn                     # 虚拟环境
├── .gitignore
├── requirements.txt
├── Dockerfile
├── README.md
```

说明：

- 所有代码都放到/app目录下
- 所有接口模块的目录名都以_module为后缀
  - 每个接口模块都包含router.py/schema.py/readme.md文件
- 目录名使用全小写英文单词命名，使用下划线连接在一起

### 3.2 命名规范

- 配置文件中的配置都以常量的形式命名，常量使用全大写的方式；
- 普通变量使用小写驼峰命名；

### 3.3 路由规范

- 路由中使用小写英文单词；
- 使用单数形式；
- 如果是多个单词，则使用斜杠/实现，不使用下划线或其他，如`/dept/{dept_id}/user/{user_id}`；

### 3.4 数据库规范

- `lower_case_snake` (小写驼峰命名)
- 每个表名使用统一的前缀；
- 单数形式 (例如. post, post_like, user_playlist)
- `_at` 作为 datetime 类型的后缀，创建时间`created_at`（插入时自动写入）/更新时间`updated_at`（更新时自动更新）
- `_date` 作为 date 类型的后缀
- `remark` 备注字段名
- `id` 自增主键字段名，在其他表作为外键时命名`tablename_id`

## 4. fas工具使用说明

```sh
# 添加一个模块
# test是模块名称，可以设定
fas module new --name=test

# 添加模块之后，要使模块生效，需要手动在app/main.py文件中注册该路由
# prefix: 该参数定义路由的前缀，每个模块的路由前缀必须是唯一的
from test_module.router import router as test_router
app.include_router(test_router, prefix="/test", tags=["测试模块"])

# 在当前目录增加一个test.py文件
# python是文件类型，test是文件名
fas file python test

# 代码风格检测（可以优先使用ruff）
fas check ruff
fas check mypy
fas check flake8
```

fas也支持一些内置模块：

```sh
# 支持的内置模块列表
fas module list

# 查看某内置模块的帮助文档
fas module help captcha
```

## 5. 附录

## 6. 项目相关人员

- __author__
