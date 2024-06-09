# __title__

__desc__

## 目录规范

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

## 接口使用说明

### 统一的接口异常响应值

```json
{
    "code": 10404,
    "message": "异常响应信息",
    "detail": "详细的接口异常信息，通常只用于开发阶段排查定位问题，该值可能为空"
}
```

- code值和http状态码通常是对应的，如该值为10404时，则http状态对应为404（计算方式：10404 % 1000），如果计算得到的http状态码大于600，则会重置为500

### 基础通用接口

- `/version`: 获取接口版本号
- `/status/code`: 获取接口异常状态码列表
