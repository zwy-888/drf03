from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from api.models import Employee
from .serializers import EmployeeSerializer, EmployeeDeSerializer


class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 查询单个

        user_id = kwargs.get("id")
        if user_id:
            # 对象不能直接发到前端
            # 使用序列化器完成序列化
            user_obj = Employee.objects.get(pk=user_id)
            emp_ser = EmployeeSerializer(user_obj).data
            # 想序列化谁就把他放进括号内
            # 后面不跟data返回的是一个序列化器类
            return Response({
                'status': 200,
                'message': "查询单个用户成功",
                'result': emp_ser
            })
        else:
            user_obj = Employee.objects.all()
            emp_ser = EmployeeSerializer(user_obj, many=True).data
            return Response({
                "status": 200,
                'message': "查询所有成功",
                'result': emp_ser
            })

    def post(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, dict) or data == {}:
            return Response('请求格式有误')

        # print(data)
        # return Response('ok')
        # 进行反序列化,将需要反序列化的反到括号里
        serializer = EmployeeDeSerializer(data=data)
        # print(serializer)

        # 对序列化的数据进行校验  通过is_valid() 方法对传递到序列化器类的数据进行校验
        print(serializer.is_valid())
        if serializer.is_valid():
            emp_obj = serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": '用户保存成功',
                "result": EmployeeSerializer(emp_obj).data
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": serializer.errors
        })
