import time
from restful01 import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
from rest_framework.versioning import BaseVersioning


class MyAuthentication(BaseAuthentication):
    """
    RestFramework 认证模块
    """
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UsersToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败...')
        # 默认不设置返回元祖 则返回匿名用户
        return (token_obj.user, token_obj)
        # return

    def authenticate_header(self, v):
        """ 返回响应头 """
        pass


class Permission(BasePermission):
    """
    RestFramework 权限模块
    """
    message = 'need VIP...'

    def has_permission(self, request, view):
        if request.user.user_type != 1:
            return False
        return True


VISIT_RECORD = {}


class VisitThrottle(BaseThrottle):
    """
    RestFramework 限制访问频率模块(自定制)
    """
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 获取访问者IP
        remote_addr = request.META.get('REMOTE_ADDR')
        c_time = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [c_time, ]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        # 删选出最近10秒的访问记录
        while history and history[-1] < c_time - 10:
            history.pop()

        if len(history) < 3:
            history.insert(0, c_time)
            return True
        return False

    def wait(self):
        """
        还需等待多少秒
        :return:
        """
        c_time = time.time()
        return 10 - (c_time - self.history[-1])


class VisitThrottles(SimpleRateThrottle):
    """
    RestFramework 限制访问频率模块(源码)
    """
    scope = 'SP'

    def get_cache_key(self, request, view):
        return self.get_ident(request)