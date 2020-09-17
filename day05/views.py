from django.shortcuts import render

# Create your views here.

from rest_framework import views, status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, \
    UpdateModelMixin
# 四大视图组件
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Employee2
from .serializers import BookModelSerializer, EmpModelSerializer

from api.models import Book


class BookAPIView(APIView):
    def get(self, reuqest, *args, **kwargs):
        # id = kwargs.get('id')
        # if id:
        objects_all = Book.objects.all()
        serializer = BookModelSerializer(objects_all, many=True).data
        return Response({
            "result": serializer
        })


class BookGenericsAPIView(GenericAPIView, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                          CreateModelMixin):
    # 获取操作模型（数据）和序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if id in kwargs:
            return self.retrieve(request, *args, **kwargs)  # 查询单个 用谁就继承谁

        return self.list(request, *args, **kwargs)  # list 查询所有

    # def get(self, reuqest, *args, **kwargs):
    #     # objects_all = Book.objects.filter(is_delete=False)
    #     # 同样是获取所有  需要指定一个queryset = Book.objects.filter(is_delete=False)
    #     objects_all = self.get_queryset()
    #     # 里面封装的self.get_queryset() = queryset
    #     # serializer = BookModelSerializer(objects_all, many=True).data
    #     # serializer = self.get_serializer(objects_all, many=True)
    #     serializer = self.get_serializer(objects_all, many=True).data
    #     return Response({
    #         "result": serializer
    #     })

    # def get(self, request, *args, **kwargs):
    #     # id = kwargs.get('id')
    #     # book_obj = Book.objects.get(pk=id)
    #     # book_ser = BookModelSerializer(book_obj).data
    #     book_obj = self.get_object()
    #     book_ser = self.get_serializer(book_obj).data
    #     return Response({
    #         "result": book_ser
    #     })
    # 新增图书
    def post(self, request, *args, **kwargs):
        create = self.create(request, *args, **kwargs)
        return Response()

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response()

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return Response()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BookGenericMixinView(ListAPIView, RetrieveAPIView, CreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"


class BookModelViewSet(ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    """定义登录操作"""

    def user_login(self, request, *args, **kwargs):
        # 可以再此方法中完成用户登录
        request_data = request.data
        print(request_data)
        return self.list(request, *args, **kwargs)
        # return Response('666')


class EmpModelViewSet(ModelViewSet):
    queryset = Employee2.objects.all()
    serializer_class = EmpModelSerializer
    lookup_field = "id"
    print(queryset)

    """定义登录操作"""

    def user_login(self, request, *args, **kwargs):
        # 可以再此方法中完成用户登录

        request_data = request.data
        print(request_data)
        username = request_data.get('username')
        pwd = request_data.get('password')
        print(request_data.get('username'))
        print(request_data.get('password'))
        try:
            A = Employee2.objects.get(username=username)
            print('111', A)
            # return Response('OK')
            if A:
                if pwd == A.password:
                    print('222', A.password)
                    return Response('登录成功')
                return Response('密码错误')
        except:
            return Response('用户不存在')

        # return self.list(request, *args, **kwargs)

    def register(self, request, *args, **kwargs):
        request_data = request.data
        username = request_data.get('username')
        pwd = request_data.get('password')
        print(request_data)
        A = Employee2.objects.get(username=username)
        if A:
            return Response('用户名已存在')
        else:
            Employee2.objects.create(username=username, password=pwd)
            return Response('注册成功')

    def patch(self, request, *args, **kwargs):
        print('我进来了')
        emp_id = kwargs.get('id')

        # 路由传递id 如果修改多个就不用传id根据这一点来区分单个修改还是多个修改
        request_data = request.data
        print(request_data)
        # 如果id存在且是字典格式单个修改
        if emp_id and isinstance(request_data, dict):
            # 为了实现单个修改也改为群改，把book_id放入列表里使格式与群改一样
            emp_ids = [emp_id, ]  # []
            request_data = [request_data]  # [{}]
        elif not emp_id and isinstance(request_data, list):
            emp_ids = []
            # 将要修改的id 放入到列表book_ids 里
            # {id：1, book_name: 222}, {id：2, book_name: 111}
            for dic in request_data:  # 遍历得到的数据从而拿到id
                pk = dic.pop('id', None)  # 后面写上NONE是为了不报错，报错就不能执行到else
                if pk:
                    emp_ids.append(pk)
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

        emp_list = []  # 所有图书对象
        for pk in emp_ids:
            try:
                emp_obj = Employee2.objects.get(pk=pk)
                emp_list.append(emp_obj)
            except:
                # 如果id不存在将id与对应数据删除
                index = emp_ids.index(pk)
                request_data.pop(index)

                # 参数处理完了进行反序列化将数据保存入库
        emp_ser = EmpModelSerializer(data=request_data, instance=emp_list, partial=True, many=True)
        emp_ser.is_valid(raise_exception=True)
        emp_ser.save()

        return Response({
            "status": 200,
            'message': "ok"
        })


class EmpGenericsAPIView(GenericAPIView, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                         CreateModelMixin):
    # 获取操作模型（数据）和序列化器类
    queryset = Employee2.objects.all()
    print(queryset)
    serializer_class = EmpModelSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if id in kwargs:
            return self.retrieve(request, *args, **kwargs)  # 查询单个 用谁就继承谁

        return self.list(request, *args, **kwargs)  # list 查询所有

    # def get(self, request, *args, **kwargs):
    #     """
    #     查询图书接口
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     if id in kwargs:
    #         return self.retrieve(request, *args, **kwargs)  # 查询单个 用谁就继承谁
    #
    #     return self.list(request, *args, **kwargs)  # list 查询所有
    #
    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return Response()

    # def patch(self, request, *args, **kwargs):
    #     response = self.partial_update(request, *args, **kwargs)
    #     return Response()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
