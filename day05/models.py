from django.db import models


# Create your models here.
class Employee2(models.Model):
    gender_choices = ((0, "male"), (1, 'female'), (2, 'other'))
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    phone = models.CharField(max_length=11, null=True, blank=True)  # blank = Ture 是针对表单的可以为空，null=ture 是针对数据库的在数据库中可以为空
    pic = models.ImageField(upload_to='pic', default='pic/1.jpg')
    dept = models.ForeignKey(to="Dept", on_delete=models.CASCADE,  # 级联删除
                             db_constraint=False,  # 删除后对应的字段可以为空
                             related_name="books", )  # 反向查询的名称)

    class Meta:
        db_table = 'ba_emp1'  # 数据库中的名字
        verbose_name = '员工'  # admin页面上的名字
        verbose_name_plural = verbose_name


class Dept(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    addr = models.CharField(max_length=100)
