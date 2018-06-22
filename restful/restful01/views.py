import json
import time
import hashlib
from restful01 import models
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework import exceptions

from rest_framework.versioning import BaseVersioning
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning


@csrf_exempt
def users(request):
    users_list = ['tom', 'jon']
    return HttpResponse(json.dumps((users_list)))


class MyBaseView(object):
    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(MyBaseView, self).dispatch(request, *args, **kwargs)
        print('after')
        return ret


def UserMD5(username):
    """
    加密用户字符串
    :param username:
    :return:
    """
    c_time = str(time.time())
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(c_time, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    API用户认证
    """

    def get(self, request, *args, **kwargs):
        # self.dispatch
        # MyAuthentication 认证返回两个对象user和auth (未设置返回对象则默认为匿名用户)
        # request.user -> token_obj.user
        # request.auth -> token_obj
        print(request.user)
        ret = {
            'code': 1000,
            'msg': 'success'
        }
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': None
        }

        user = request._request.POST.get('username')
        pwd = request._request.POST.get('pwd')
        obj = models.UsersInfo.objects.filter(username=user, pwd=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = 'username or password error...'
            return JsonResponse(ret)

        token = UserMD5(user)
        models.UsersToken.objects.update_or_create(user=obj, defaults={'token': token})
        ret['token'] = token
        return JsonResponse(ret)


class StudentsView(APIView):
    # rest framework 自定义用户认证(空即不参与全局认证)
    authentication_classes = []

    # 通过反射实现CBV
    # def dispatch(self, request, *args, **kwargs):
    #     func = getattr(self, request.method.lower())
    #     ret = func(request, *args, **kwargs)
    #     return ret

    def get(self, request, *args, **kwargs):
        ret = {
            'code': 1000,
            'msg': 'xxx'
        }
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')

    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('DELETE')


class TeachersView(View):

    # CBV免除csrf认证
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print('before')
        ret = super(MyBaseView, self).dispatch(request, *args, **kwargs)
        print('after')
        return ret

    def get(self, request, *args, **kwargs):
        return HttpResponse('GET')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST')

    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('DELETE')


class UsersView(APIView):
    # 版本控制类
    # URL地址传参版本方式一 如http://127.0.0.1:8000/user_view/?version=v2
    # versioning_class = QueryParameterVersioning

    # URL地址传参版本方式二 如http://127.0.0.1:8000/v2/users/
    # versioning_class = URLPathVersioning

    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        print(request.version)
        return HttpResponse('UsersView..')


from restful01 import models
from rest_framework.request import Request
from rest_framework.parsers import JSONParser, FormParser
from rest_framework import serializers


class RolesSerializer(serializers.Serializer):
    """
    序列化指定字段
    """
    id = serializers.IntegerField()
    username = serializers.CharField()


class ParserView(APIView):
    """
    允许用户发送JSON数据
        a. content-type: application/json
        b. {'name': 'admin', age='22' }
    """
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        # 方式一
        # ret = models.UsersInfo.objects.filter().all().values()
        # ret = list(ret)
        # ret = json.dumps(ret, ensure_ascii=False)

        # 方式二
        ret = models.UsersInfo.objects.filter().all()
        # 单个Queryset对象时 many=False
        ser = RolesSerializer(instance=ret, many=True)
        # ser.data此时已经是转换完成的结果 dumps是为了页面展示
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

    def post(self, request, *args, **kwargs):
        # 1 获取用户请求
        # 2 获取用户请求体
        # 3 parser_classes 对请求头匹配
        # 4 Request.data 触发
        print(request.data)
        return HttpResponse('parser')