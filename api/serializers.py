from django.conf import settings
from rest_framework import serializers, exceptions

# 每个模型需要单独定义一个序列化器
from api.models import Employee


class EmployeeSerializer(serializers.Serializer):
    print()
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    phone = serializers.CharField()
    # pic = serializers.ImageField()

    # def get_username(self):
    # 自定义字段
    # 定义models中不存在的字段
    salt = serializers.SerializerMethodField()
    # 自定义一下已有的字段也要用到他
    gender = serializers.SerializerMethodField()

    # 自定义字段属性名可以随意写但是下面的get要和它对应get_它
    # 自定字段在数据库中没有对应值，所以要定义此函数获取对应值

    def get_salt(self, obj):
        print("9999", self)
        return 'salt'

    def get_gender(self, obj):
        # if obj.gender == 0:
        #     return 'male'
        # elif obj.gender == 1:
        #     return "female"
        # else:
        #     return "other"
        # 简单方法
        return obj.get_gender_display()

    # 自定义图片链接使用户能直接访问到图片
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        # return "%s%s%s" % ("http://127.0.0.1:8000",settings.MEDIA_ROOT,obj)

        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, obj.pic)


# 反序列化，存入库
# 反序列化不存在自定义字段
class EmployeeDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        # 做限制条件
        max_length=8,
        min_length=1,
        # 为规则自定义错误信息
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了",
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField(min_length=11, required=True)
    re_pwd = serializers.CharField()

    # 局部钩子

    # 验证单个字段
    # def validate_username(self, values):
    #     print(values)

    # 定义全局钩子
    def validate(self, attrs):
        print(attrs)  # 获取到前端发送的所有参数字典类型
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        # 自定义校验规则
        if pwd != re_pwd:
            raise exceptions.ValidationError('两次密码不一致')
        return attrs

    def create(self, validated_data):
        """
        在保存用户对象时需要重写此方法完成保存
        :param validated_data: 前端传递的需要保存的数据
        :return:
        """
        print(validated_data)
        return Employee.objects.create(**validated_data)
