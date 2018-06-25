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
    user_type = serializers.CharField(source="get_user_type_display")
    username = serializers.CharField()
    group = serializers.CharField(source='group.title')
    rls = serializers.SerializerMethodField()

    def get_rls(self, row):
        """ 取数据库ManyToManyField字段 """
        role_obj_list = row.role.all()
        ret = []
        for item in role_obj_list:
            ret.append({'id': item.id, 'title': item.title})
        return ret


class BRolesSerializer(serializers.ModelSerializer):
    """
    同serializers.Serializer简化字段编写
    """
    user_type = serializers.CharField(source="get_user_type_display")

    class Meta:
        model = models.UsersInfo
        # fields = ['id', 'username', 'ooo']
        fields = "__all__"
        depth = 1


class CRolesSerializer(serializers.ModelSerializer):
    """
    同serializers.Serializer JSON中生成带链接的反向URL
    """
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = models.UsersInfo
        fields = ['id', 'username', 'group', 'role']


class ParserView(APIView):
    """
    6 序列化
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
        # ser = RolesSerializer(instance=ret, many=True)

        ser = CRolesSerializer(instance=ret, many=True, context={'request': request})
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


class GRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = "__all__"


class GroupView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        group_obj = models.Group.objects.filter(id=pk).first()
        ser = GRolesSerializer(instance=group_obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


from restful.utils.pager import PagerSerializer
# API渲染
from rest_framework.response import Response
# page分页
from rest_framework.pagination import PageNumberPagination
# offset分页
from rest_framework.pagination import LimitOffsetPagination
# 加密分页
from rest_framework.pagination import CursorPagination


class MyPageNumberPagination(PageNumberPagination):
    """ 自定义分页(?page=1) """
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'

    max_page_size = 5


class MyLimitOffsetPagination(LimitOffsetPagination):
    """ 自定义位移分页(http://127.0.0.1:8000/v1/pager1/?offset=0&limit=3) """
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 5


class MyCursorPagination(CursorPagination):
    """ 加密分页(http://127.0.0.1:8000/v1/pager1/?cursor=cD0y) """
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = 'id'


class PapersView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        roles = models.Roles.objects.all()

        # 创建分页对象
        # pg = MyPageNumberPagination()
        # pg = MyLimitOffsetPagination()
        pg = MyCursorPagination()

        # 在数据库中获取分页的对象
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(pager_roles)

        # 对数据进行序列化
        ser = PagerSerializer(instance=pager_roles, many=True)
        # ser = PagerSerializer(instance=roles, many=True)

        # return Response(ser.data)
        # 更多respoonse 自动上页 下页
        return pg.get_paginated_response(ser.data)


# 高级视图实现增删改查
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin


class View1View(ModelViewSet):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser, FormParser]

    queryset = models.Roles.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination
