from django.conf.urls import url, include
from restful01 import views

# 自动路由
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'rt', views.View1View)
router.register(r'rt1', views.View1View)

urlpatterns = [
    url(r'^users/', views.StudentsView.as_view()),
    url(r'^api/v1/auth/$', views.AuthView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$', views.GroupView.as_view(), name='gp'),
    url(r'^(?P<version>[v1|v2]+)/pager1/$', views.PapersView.as_view(), name='pa'),
    # url(r'^(?P<version>[v1|v2]+)/v1/$', views.View1View.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^(?P<version>[v1|v2]+)/v1/(?P<pk>\d+)$', views.View1View.as_view({'get': 'retrieve',
    #                                                                         'delete': 'destroy',
    #                                                                         'put': 'update',
    #                                                                         'patch': 'partial_update'})),
    url(r'^(?P<version>[v1|v2]+)/', include(router.urls))
]