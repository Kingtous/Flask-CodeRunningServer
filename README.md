#### 代码服务器后端

前端链接（使用`React + dva2`，刚开始开发）：[Github链接](https://github.com/Kingtous/code-running-front)

- 编程语言
    - Python 3.6+

- 目前有等功能（Api）
    - 用户功能
        - 登陆/注册
        - 获取登录令牌（token）
        - 修改用户资料
        - 查看用户统计数据（点赞数、积分数等）
    - 用户活动
        - 签到
        - 资料页点赞
    - 上传功能
        - 上传代码
            - 支持`c/c++/python3/java`代码（需要服务器环境支持）
        - 上传图片等静态资源
            - 支持通过获取七牛云token上传
    - 代码功能
        - 执行代码
            - 先上传代码后可以执行代码
        - 获取代码执行结果
            - 支持将错误流转至输出流
        - 获取代码执行状态
            - 编译、正在运行、出错、结束
    - 论坛系统
        - 发布帖子
            - 支持附带代码
        - 删除帖子
        - 获取我发布的帖子
            - 一页10条
        - 获取评论
            - 一页10条
        - 发布评论
        - 删除评论
    - 商城系统（还未做）
        - 发布售卖信息
        - 购买商品
        - 删除售卖信息
        
#### API文档
代码未完全写好，未做很多优化，代码变动会很大，文档暂时不提供。

若需要，请自己读代码或者发送请求邮件至`me@kingtous.cn`


#### 注意
`flask-cache 0.13.1`使用了过时的flask.ext组件，请手动将：

```python
from flask.ext.cache import make_template_fragment_key
```

改成：

```python
from flask_cache import make_template_fragment_key
```