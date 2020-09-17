from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Book
from day05.models import Employee2


class EmpListSerializer(serializers.ListSerializer):
    """
    使用此序列化器完成同时修改多个对象
    """

    #     # 重写update方法完成批量更新
    def update(self, instance, validated_data):
        # 要修改的对象  要修改的值
        # print(self)     # 当前调用的序列化器类
        # print(instance)  # 要修改的对象
        # print(validated_data)  # 要修改的值
        # print("1111", self.child)

        # 将群改修改成每次修改一个
        for index, obj in enumerate(instance):
            # print(index)
            # print(obj)
            # print(validated_data[index])
            # TODO 每遍历一次 改变一下下标以及对应值和对象
            self.child.update(obj, validated_data[index])

        return instance


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_name', 'price', 'pic', 'publish')
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


class EmpModelSerializer(ModelSerializer):
    class Meta:
        # 为修改多个图书提供ListSerializer
        list_serializer_class = EmpListSerializer
        model = Employee2
        fields = ('username', 'password', 'dept', 'gender')
        extra_kwargs = {
            "username": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
            },
            # 只参与反序列化
            "password": {
                "max_length": 18,
                # 指定此字段只参与反序列化
            },
            "dept": {
                "write_only": True,
            },
            # 只参与序列化
            "gender": {
                "read_only": True
            }
        }
