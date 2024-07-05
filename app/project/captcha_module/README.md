# 验证码模块-模块说明

## 1. 使用说明

- 1. 增加验证码模块:

```sh
fas module add captcha

# 查看该命令的帮助
fas module add --help
```

- 2. 在系统主入口文件（main.py）注册验证码模块：

```python
# 验证码模块需要使用redis
# 需要初始化redis，可以指定host，port，db等参数
from common.connections import init_redis
init_redis('192.168.1.242')   # 初始化redis

# 如果需要配置验证码的有效期等
from captcha_module.api import config as captcha_config
# 配置验证码有效期，及在redis中的前缀（应该避免和其他业务冲突）
captcha_config(expire=120, prefix='ctc')
```

## 2. 验证码流程

1. 进入登陆页面。
2. 请求验证码，地址应该类型：http://host/captcha/image/{token}?t=时间字符串 ，方法GET（其实就是跟请求一个普通图像一样）。该地址返回的就是一个图片，跟普通请求图片差不多，后面的参数t（每次请求都会变）主要是用来保证每次都能请求到新的图片。token这个参数可以理解为当前这个表单的唯一值（前端直接随机生成一个即可，例如毫秒级时间戳）。
3. 服务器端收到请求，生成一个随机的验证码字符串，请求参数中的token作为key，随机字符串作为value，存入redis（设置有效期，例如五分钟等），并生成图片返回（响应体为二进制图像）。
4. 刷新验证码，只要重新请求即可，重新请求token应该是不变的。
5. 登陆的时候，验证码的token参数也作为参数提交。服务器端根据该参数，就能做到redis中的value，从而判断用户输入的值是否正确。

验证码图像请求地址中的时间字符串主要是用来避免图像被缓存。

## 3. 模块开发者

- caiyingyao
