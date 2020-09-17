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
    # ·
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


# 此序列化器在定义完成后需要使用才生效
class BookListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成同时修改多个对象
    """

    # 重写updata方法完成批量更新
    def update(self, instance, validated_data):
        print(self)
        # 要修改的对象 instanceccc
        # 要修改的值 validated_data
        # self是当前调用的序列化类
        # 群改
        # 每遍历一次改变一下下标以及修改的对象 ，obj在变，index也在变
        # for index, obj in enumerate(instance):
        #     print(obj)
        #     self.child.updata(obj, validated_data[index])
        return instance


class BookModelSerializerV2(ModelSerializer):
    """
    序列化器整合
    """

    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = BookListSerializer
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
# class BookListSerializer(serializers.ListSerializer):
#     """
#     使用此序列化器完成同时修改多个对象
#     """
#
#     # 重写update方法完成批量更新
#     def update(self, instance, validated_data):
#         # 要修改的对象  要修改的值
#         # print(self)     # 当前调用的序列化器类
#         # print(instance)  # 要修改的对象
#         # print(validated_data)  # 要修改的值
#         # print("1111", self.child)
#
#         # 将群改修改成每次修改一个
#         for index, obj in enumerate(instance):
#             # print(index)
#             # print(obj)
#             # print(validated_data[index])
#             # TODO 每遍历一次 改变一下下标以及对应值和对象
#             self.child.update(obj, validated_data[index])
#
#         return instance
#
#
# class BookModelSerializerV2(ModelSerializer):
#     """
#     序列化器与反序列化器整合
#     """
#
#     class Meta:
#
#         # 为修改多个图书提供ListSerializer
#         list_serializer_class = BookListSerializer
#
#         model = Book
#         # 指定的字段  填序列化与反序列所需字段并集
#         fields = ("book_name", "price", "pic", "publish", "authors")
#
#         # 添加DRF的校验规则  可以通过此参数指定哪些字段只参加序列化  哪些字段只参加反序列化
#         extra_kwargs = {
#             "book_name": {
#                 "max_length": 18,  # 设置当前字段的最大长度
#                 "min_length": 2,
#             },
#             # 只参与反序列化
#             "publish": {
#                 "write_only": True,  # 指定此字段只参与反序列化
#             },
#             "authors": {
#                 "write_only": True,
#             },
#             # 只参与序列化
#             "pic": {
#                 "read_only": True
#             }
#         }
#
#     # 全局钩子同样适用于 ModelSerializer
#     def validate(self, attrs):
#         name = attrs.get("book_name")
#         book = Book.objects.filter(book_name=name)
#         if len(book) > 0:
#             raise exceptions.ValidationError('图书名已存在')
#
#         return attrs
#
#     # 局部钩子的使用  验证每个字段
#     def validate_price(self, obj):
#
#         # 可以通过self.context获取到视图中传递过来的request对象
#         request = self.context.get("request")
#         print(request.data)
#         # 价格不能超过1000
#         if obj > 1000:
#             raise exceptions.ValidationError("价格最多不能超过10000")
#         return obj
#
#     # # 重写update方法完成更新
#     # def update(self, instance, validated_data):
#     #     print(instance, "11111")
#     #     print(validated_data)
#     #     book_name = validated_data.get("book_name")
#     #     instance.book_name = book_name
#     #     instance.save()
#     #     return instance
