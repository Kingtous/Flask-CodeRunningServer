def set_up_api(app):
    from flask_restful import Api

    from api.code.code_runner import CodeRunnerSubmitAPI, CodeRunningQueryAPI
    from api.thread.comments_handler import SubmitComment, DeleteComment, GetComment
    from api.file.file_upload import UploadFile, GetFile, GetCodeList, DelFile
    from api.test.test_response import TestResponse
    from api.thread.threads_handler import ThreadsHandler, DeleteThread, GetUserThread
    from api.qiniu.token import UploadTokenAPI
    from api.user.profile import AlterProfile, UserStatistic, UserLikeApi
    from api.user.user_login_register import Login, Register, GetToken, UserSignIn, GetCredits
    from api.mail.mail_handler import MailHandler
    from api.user.user_login_register import UserResetPassword
    api = Api(app)
    # 1: 用户登录注册资料点赞
    api.add_resource(Login, '/auth/login')  # 登录
    api.add_resource(Register, '/auth/register')  # 注册
    from api.mail.mail_handler import RegisterMail
    api.add_resource(RegisterMail, '/auth/sendRegisterMail')  # 发送注册验证码
    api.add_resource(GetToken, '/auth/getToken')  # 获取新的token
    api.add_resource(UserSignIn, '/user/signIn')  # 签到
    api.add_resource(GetCredits, '/user/myCredits')  # 查询自己的点数
    api.add_resource(AlterProfile, '/user/profile/alter')  # 修改自己的资料
    api.add_resource(UserStatistic, '/user/profile/<id>')  # 查询统计数据
    api.add_resource(UserLikeApi, '/user/profile/like/<user_id>')  # 点赞
    api.add_resource(MailHandler, '/auth/mail/reset_password')  # 发送重置邮件
    api.add_resource(UserResetPassword, '/auth/profile/reset_password')  # 重置密码接口

    # 2: 上传文件
    api.add_resource(UploadTokenAPI, '/file/getUploadToken')  # 获取上传token使用的是七牛云
    api.add_resource(UploadFile, '/file/upload')  # 用于上传代码啥的小文件
    api.add_resource(GetFile, '/uploaded/<file_name>')
    api.add_resource(GetCodeList, '/file/get_code/<offset>')
    api.add_resource(DelFile, '/file/delete/<id>')

    # 3: 获取结果
    api.add_resource(TestResponse, '/test')
    api.add_resource(CodeRunnerSubmitAPI, '/code/run')
    api.add_resource(CodeRunningQueryAPI, '/code/getResult')

    # 4. 帖子
    api.add_resource(ThreadsHandler, '/threads/push_show')
    api.add_resource(DeleteThread, '/threads/delete')
    api.add_resource(GetUserThread, '/threads/me')
    api.add_resource(SubmitComment, '/threads/comment/submit')
    api.add_resource(DeleteComment, '/threads/comment/del')
    api.add_resource(GetComment, '/threads/comment/get')

    # 5: 商城
    from api.mall.items import GetItems
    api.add_resource(GetItems, '/mall/get_items')
    from api.mall.items import AddItems
    api.add_resource(AddItems, '/mall/add_items')
    from api.mall.items import DeleteItems
    api.add_resource(DeleteItems, '/mall/delete_items')
    from api.mall.cart import GetCart
    api.add_resource(GetCart, '/mall/my_cart')
    from api.mall.cart import AddCart
    api.add_resource(AddCart, '/mall/cart/add')
    from api.mall.cart import DelCart
    api.add_resource(DelCart, '/mall/cart/del')
    from api.mall.cart import BuyCarts
    api.add_resource(BuyCarts, '/mall/cart/buy')
    from api.mall.repository import GetRepositoryItems
    api.add_resource(GetRepositoryItems, '/repository/get')
