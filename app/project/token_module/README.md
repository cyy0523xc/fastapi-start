# token模块说明

token的生成与校验模块: 该模块的目标是对外生成访问token，可以指定该token只能访问某些页面。

关于数据权限校验：

- 通过路径参数校验：如路由`/task/{task_id}`这种可以通过路由中的参数就能控制；
- 但是数据权限不是说在路由参数中定义就可以了，还应该结合该用户的实际权限，也就是说该用户是否具有访问该资源的权限；
- 数据权限更多是需要在接口的依赖(Depends)中实现。

## 1. 使用说明

### 1.1 生成token接口

接口参数（含签名参数）生成token（其实就是一个key值，真正的数据通常存储到redis中），而token可以额外指定允许访问的权限tag或者指定的路径参数，从而实现功能权限及详情页数据权限。

注：通过这个通常只能实现部分数据权限，主要是针对某个具体资源的访问权限，这要求我们在设置路由的时候，应该要遵循restful规范，例如查询某个任务的数据时，接口url应该是类似：`/task/{task_id}`，这样就可以在生成token参数中指定相应的允许的`task_id`。
如token接口参数如下：

```sh
{
    "username": "test",
    "expire": 86400,
    "signature": "xxxxxxxx",
    "data": {
        "auth_tags": ["任务详情页"],
        "tasks_id", [123, 45]
    }
}
```

对这个参数说明一下，这次访问的用户名是test，生成token的有效期是一天（86400秒），参数签名是xxxxxxxx（这个签名用来保障data中的数据没有被篡改），token参数有两个数据：

- `auth_tags`: 这个定义这个token能够访问的tag有哪些，这里定义了至多只能访问任务详情页这个tag，也就是说接口定义时，tags参数必须包含该tag才能访问。
- `tasks_id`: 这个用来限制token能够访问的路径参数，如上限制了如果当前url中包含了task_id参数，则其值只能时123/45中的一个。

这里需要重点说明的是，并不是接口满足了`auth_tags`和`tasks_id`就一定能访问对应的接口，因为还要看该用户是否有相应的权限，例如该用户本身是否具有访问任务详情页这个tag的权限，是否具有访问123/45这两个任务的权限，如果其中一项不满足，那这个token也无法访问。

#### 1.1.1 关于嵌套参数的数据权限

例如任务是由某部门的用户创建的，而且部门还是树型结构，这时路由应该这样定义：`/dept/{dept_id}/task/{task_id}`（获取某部门某任务的详细数据），而不只是`/task/{task_id}`（把部门id作为参数传递）。

这时生成token的参数应该类似这样：

```json
{
    "dept_id": "xxxxx001",
    "tasks_id": [1,2,3]
}
```

需要注意的是，如当前访问的路径为`/dept/xxxxx001/task/3`（dept_id=xxxxx001, task_id=3），则是token校验是通过的。而对于路径`/dept/xxxxx001`也应该是通过的。

但是这也无法解决复杂权限的嵌套问题，例如某用户有A部门的任务ID为3的权限以及B部门的任务ID为4的权限，这种复杂的嵌套就无法通过路径参数来定义这个权限控制。

### 1.1.2 不支持列表页的数据权限

在列表页，用户能够访问哪些数据，这通常是在SQL查询时通过where参数来定义的，因此列表页的数据权限需要独立实现。

### 1.2 校验token

对于需要token校验的接口，应该类似如下:

```python
from fastapi import Depends, Path
from .utils import valid_data

@app.post(path="/task/{task_id}", summary="获取单个任务的详细数据", ...)
async def task_detail_api(
    task_id: int = Path(..., title="任务id"),
    # ...,
    token_data=Depends(valid_data)
):
```

这里主要就是：`token_data=Depends(valid_data)`，这在获取token的时候，就自动完成了token校验。

## 2. 模块开发者

- alex cai
