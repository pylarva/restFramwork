# Django Rest Framework
> [http://www.lichengbing.com/archivers/914.html](http://www.lichengbing.com/archivers/914.html)

1. 认证流程
2. 权限流程
3. 节流（访问控制）
4. 版本
   - versioning_class = QueryParameterVersioning
   - versioning_class = URLPathVersioning
5. 解析器
   - JSONParser解析content-type:application/json头
   - FormParser解析content-type:x-www-form-urlencoded头
6. 序列化
   - Django自带序列化 QuerySet -> all().values(id='..',val='') -> list -> dumps(ensure_ascii=Flase)
   - Framework -> rest_framework import serializers
   - source参数显示数据库choices、ForeignKey字段
   - SerializerMethodField自定义显示ManyToManyField字段
   - 自动连表查询 depth = 1
   - 生成链接地址
7. 分页
   - PageNumberPagination page分页
   - LimitOffsetPagination offset分页
   - CursorPagination 加密分页
8. 高级路由系统
   - ModelViewSet 改写路由实现简化增删改查
   - from rest_framework import routers 自动路由