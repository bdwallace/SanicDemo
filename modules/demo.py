from tortoise import Model, fields


class Demo(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=40, null=False, verbose_name='名字')
    password = fields.CharField(max_length=40, null=False, verbose_name="密码")
    remark = fields.CharField(max_length=245, null=True, verbose_name='备注')

    class Meta:
        table = 'demo'
        db = 'Demo'