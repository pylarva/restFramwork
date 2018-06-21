from restful01 import models
from rest_framework import exceptions


class MyAuthentication(object):
    """
    RestFramework 认证模块
    """
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UsersToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败...')
        # 默认不设置返回元祖 则返回匿名用户
        # return (token_obj.user, token_obj)
        return

    def authenticate_header(self, v):
        pass