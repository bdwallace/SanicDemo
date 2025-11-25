from tortoise import Model, fields


class Demo(Model):
    id = fields.IntField(pk=True)
    user_name = fields.CharField(max_length=20, null=False, verbose_name="用户名")
    password = fields.CharField(max_length=64, null=False, verbose_name="密码")
    email = fields.CharField(max_length=50, null=False, verbose_name='邮箱')
    login_ip = fields.CharField(max_length=20, null=True, verbose_name='登录IP')
    login_time = fields.DatetimeField(auto_now=True, verbose_name="登录时间")
    create_time = fields.DatetimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = fields.DatetimeField(auto_now=True, verbose_name="更新时间")
    mfa_on = fields.CharField(max_length=10, default="禁用", verbose_name="MFA验证")

    class Meta:
        table = 'demo'
        db = 'Demo'
