import json
from django.views import View
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework import exceptions


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


class MyAuthentication(object):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败...')
        return ('Success', None)

    def authenticate_header(self, v):
        pass


class StudentsView(APIView):
    # rest framework 自定义用户认证
    authentication_classes = [MyAuthentication, ]

    # 通过反射实现CBV
    # def dispatch(self, request, *args, **kwargs):
    #     func = getattr(self, request.method.lower())
    #     ret = func(request, *args, **kwargs)
    #     return ret

    def get(self, request, *args, **kwargs):
        ret = {
            'code': 10000,
            'msg': 'xxx'
        }
        return HttpResponse(json.dumps(ret))

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