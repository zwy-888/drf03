from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book
from .serializers import BookModelSerializer, BookModelDeSerializer, BookModelSerializerV2


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        查询图书接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        book_id = kwargs.get('id')
        if book_id:
            # 查询单个图书
            book_obj = Book.objects.get(pk=book_id)
            data = BookModelSerializer(book_obj).data
            return Response({
                'status': 200,
                'message': "查询单个成功",
                'result': data
            })
        else:
            object_all = Book.objects.all()
            book_list = BookModelSerializer(object_all, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有成功",
                "result": book_list
            })

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = BookModelDeSerializer(data=data)
        # 检验数据是否合法 ,一旦失败立即跳出异常
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()
        return Response({
            "status": 200,
            'message': "添加成功",
            'result': BookModelSerializer(book_obj).data
        })


class BookAPIViewV2(APIView):
    def get(self, request, *args, **kwargs):
        """
        查询图书接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        book_id = kwargs.get('id')
        if book_id:
            # 查询单个图书`-
            book_obj = Book.objects.get(pk=book_id)
            data = BookModelSerializerV2(book_obj).data
            return Response({
                'status': 200,
                'message': "查询单个成功",
                'result': data
            })
        else:
            object_all = Book.objects.all()
            book_list = BookModelSerializerV2(object_all, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有成功",
                "result": book_list
            })

    def post(self, request, *args, **kwargs):
        """
               新增单个：传递参数的格式 字典
               新增多个：[{},{},{}]  列表中嵌套字典  每一个字典是一个图书对象
               :param request:
               :return:
               """
        request_data = request.data
        if isinstance(request_data, dict):  # 代表添加单个对象
            many = False
        elif isinstance(request_data, list):  # 代表添加多个对象
            many = True
        else:
            return Response({
                "status": 400,
                "message": "数据格式有误"
            })

        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        save = book_ser.save()

        return Response({
            "status": 200,
            "message": '添加图书成功',
            "results": BookModelSerializerV2(save, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个以及删除多个
        单个删除：获取删除的id  根据id删除  通过动态路由传参 v2/books/1/  {ids:[1,]}
        删除多个：有多个id的时候 {ids:[1,2,3]}
        """
        book_id = kwargs.get("id")

        if book_id:
            # 删除单个  将删除单个转换为删除多个的参数形式
            ids = [book_id]
        else:
            # 删除多个
            ids = request.data.get("ids")

        # 判断传递过来的图书的id是否在数据库中  且还未删除
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        # 查到他并把他的删除状态更新为true
        print(response)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或者图书不存在",
        })

    # def put(self, request, *args, **kwargs):
    #     """
    #     整体修改单个：修改一个对象的全部字段
    #     :return 修改后的对象
    #     """
    #     # 修改的参数
    #     request_data = request.data
    #     # 要修改的图书的id
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #         # 查到数据
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在",
    #         })
    #
    #     # 前端发送的修改的值需要做安全校验
    #     # 更新参数的时候使用序列化器完成数据的校验
    #     # TODO 如果当前要修改某个对象则需要通过instance来指定你要修改的对象
    #     # 查到数据放进序列化器并发返回序列化后的数据  ，通过instance指定要修改的对象
    #     book_ser = BookModelSerializerV2(data=request_data, instance=book_obj)
    #     book_ser.is_valid(raise_exception=True)  # 检验校验是否成功
    #     save = book_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": BookModelSerializerV2(save).data
    #     })
    #
    # def patch(self, request, *args, **kwargs):
    #     """
    #     局部更新
    #     """
    #     # 修改的参数
    #     request_data = request.data
    #     # 要修改的图书的id
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id)
    #     except:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": "图书不存在",
    #         })
    #
    #     # 前端发送的修改的值需要做安全校验
    #     # 更新参数的时候使用序列化器完成数据的校验
    #     # TODO 如果当前要局部修改则需指定 partial = True即可
    #     book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     # book_ser 返回序列化器类
    #     book_ser.is_valid(raise_exception=True)
    #     save = book_ser.save()  # 使用save方法后将序列化器类转化为model
    #     print("111", save, type(save))
    #     print("222", book_ser.save(), type(book_ser.save()))
    #
    #     print("333", book_ser, type(book_ser))
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         "results": BookModelSerializerV2(save).data  # 返回前端再序列化json
    #     })

    def patch(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        # 路由传递id 如果修改多个就不用传id根据这一点来区分单个修改还是多个修改
        request_data = request.data
        # 如果id存在且是字典格式单个修改
        if book_id and isinstance(request_data, dict):
            # 为了实现单个修改也改为群改，把book_id放入列表里使格式与群改一样
            book_ids = [book_id, ]  # []
            request_data = [request_data]  # [{}]
        elif not book_id and isinstance(request_data, list):
            book_ids = []
            # 将要修改的id 放入到列表book_ids 里
            # {id：1, book_name: 222}, {id：2, book_name: 111}
            for dic in request_data:  # 遍历得到的数据从而拿到id
                pk = dic.pop('id', None)  # 后面写上NONE是为了不报错，报错就不能执行到else
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        'message': "id不存在",
                    })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': "格式有误",
            })

        # 对传递过来的id 和 reuest_data进行筛选 看id对应的图书是否存在
        # 如果id对应的图书不存在将id删除对应的值一并删除
        # 存在就查询图书进行修改

        book_list = []  # 所有图书对象
        for pk in book_ids:
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
            except:
                # 如果id不存在将id与对应数据删除
                index = book_ids.index(pk)
                request_data.pop(index)

                # 参数处理完了进行反序列化将数据保存入库
        book_ser = BookModelSerializerV2(data=request_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": 200,
            'message': "ok"
        })


"""
查询单个1  查询所有 1 新增单个  1更新单个1  删除单个 1 局部更新单个1
群体增加1    群体删除1    群体更新  群体局部更新
"""

# 自恋
# class BookAPIView1(APIView):
#     # class Meta:
#     #     model = Book
#     #     fields = ("book_name",)
#     def get(self, reuest, *args, **kwargs):
#         book_id = kwargs.get("id")
#
