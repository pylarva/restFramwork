# Django Rest Framework

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
   1）Django自带序列化 QuerySet -> all().values(id='..',val='') -> list -> dumps(ensure_ascii=Flase)
   2）Framework -> rest_framework import serializers