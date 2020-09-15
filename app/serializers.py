from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer

from api.models import Book, Press


class PressModelSerializer(ModelSerializer):
    class Meta:
        model = Press
        fields = ('press_name', 'address', "pic")


class BookModelSerializer(ModelSerializer):
    # book_name = serializers.CharField()
    # price = serializers.CharField()
    # ModelSerializer的使用，不用再一个一个的罗列出来

    # 自定义字段写在外面   不推荐使用
    # 在fields 里加上想要添加的字段， 然后写在model中写获取他的方法能
    # a = serializers.SerializerMethodField()
    #
    # def get_a(self, obj):
    #     return 'aaa'

    publish = PressModelSerializer()

    class Meta:
        # 指定序列化哪个模型
        model = Book
        # 通过fields指定需要里面的哪个字段

        # publish 查询外键的字段必须和外键保持一致
        # depth 显示出来的东西太多，我们需要指定外键返回的值的话，需要在序列化器里面嵌套一个序列化器
        # fields = ('book_name', 'price', 'pic', 'a', 'press_name', 'press_address', 'authors_list', 'publish')
        fields = ('book_name', 'price', 'pic', 'a', 'publish')
        # 查里面所有
        # fields = "__all__"
        # 不展示哪些字段
        # exclude = ('is_delete', 'status', 'id')

        # 指定查询深度  默认为没有深度
        # 1 的意思是一层外键  2 两层外键
        # depth = 1


class BookModelDeSerializer(ModelSerializer):
    """"
    图书的反序列化
    """

    class Meta:
        # 指定操作模型
        model = Book
        # 指定模型里面操作的参数
        fields = ("book_name", "price", "publish", "authors")
        # 为反序列化填加验证
        extra_kwargs = {
            'book_name': {
                'max_length': 18,
                'min_length': 2,
                'error_messages': {
                    "max_length": '太长了',
                    "min_length": '太短了',
                }
            },
            'price': {
                'required': True,
                "decimal_places": 2
            }
        }

        # 全局钩子 同样适用于Modelserializer

    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')
        return attrs

    def validate_price(self, obj):
        print(type(obj), "1111")
        # 价格不能超过1000
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过1000")
        return obj


class BookModelSerializerV2(ModelSerializer):
    """
    序列化器整合
    """

    class Meta:
        model = Book
        # 指定的字段  填序列化与反序列所需字段并集
        fields = ("book_name", "price", "pic", "publish", "authors")

        # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
        extra_kwargs = {
            "book_name": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
            },
            # 只参与反序列化
            "publish": {
                "write_only": True,  # 指定此字段只参与反序列化
            },
            "authors": {
                "write_only": True,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            }
        }

        # 全局钩子 同样适用于Modelserializer

        def validate(self, attrs):
            name = attrs.get("book_name")
            book = Book.objects.filter(book_name=name)
            if len(book) > 0:
                raise exceptions.ValidationError('图书名已存在')
            return attrs

        def validate_price(self, obj):
            print(type(obj), "1111")
            # 价格不能超过1000
            if obj > 1000:
                raise exceptions.ValidationError("价格最多不能超过1000")
            return obj
