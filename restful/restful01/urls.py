from django.conf.urls import url
from restful01 import views

urlpatterns = [
    url(r'^users/', views.StudentsView.as_view()),
    url(r'^api/v1/auth/$', views.AuthView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view(), name='ppp')
]