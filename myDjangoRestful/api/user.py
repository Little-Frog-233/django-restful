import os
import sys
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache #引入缓存模块

from myDjangoRestful.model.mysql import User as _User
from myDjangoRestful.utils.other.token import generateToken, generatePayload, generateSign, getPayloadFromToken, getToken
from myDjangoRestful.utils.other.des import des_encrypt
from myDjangoRestful.utils.other.token import token

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) # write_only只需要前端向后端提交，后端不返回给前端
    userpicture = serializers.CharField(required=False, default='user_undefined.png')
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def create(self, validated_data):
        return _User.objects.create(**validated_data)

class UserLoginApi(APIView):
    '''
    用户登录接口
    '''
    def post(self, request, format=None):
        '''
        验证用户信息
        '''
        form_data = request.data
        username = form_data.get('username', '')
        try:
            # 查询用户
            user = _User.objects.get(username=username)
        except _User.DoesNotExist:
            data = {
                'status_code': 404,
                'message': '用户不存在'
            }
            return Response(data, status=404)
        # 验证密码
        if des_encrypt(form_data.get('password', '')) == user.password:
            # 构造jwt的payload
            payload_str_64 = generatePayload(user_id=user.id, user_picture=user.userpicture)
            # 构造jwt的sign
            sign = generateSign(payload_str_64)
            # 构造jwt
            token = generateToken(payload_str_64, sign=sign)
            data = {
                'status_code': 200,
                'message': '用户验证成功',
                'data': {
                    'token': token
                }
            }
            return Response(data, status=200)
        else:
            data = {
                'status_code': 404,
                'message': '用户名和密码不匹配'
            }
            return Response(data, status=404)

class UserRegisterApi(APIView):
    '''
    用户注册接口
    '''
    def post(self, request, format=None):
        try:
            form_data = request.data
            serializer = UserSerializer(data=form_data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'status_code': 200,
                    'message': '注册成功'
                }
                return Response(data)
            else:
                data = {
                    'status_code': 400,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            data = {
                'status_code': 500,
                'message': msg
            }
            return Response(data, status=500)

class UserApi(APIView):
    '''
    用户
    '''
    @token
    def get(self, request, format=None):
        token = getToken(request=request)
        payload = getPayloadFromToken(token)
        user_id = payload['user_id']
        user = _User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        user_data = serializer.data
        data = {
            'status_code': 200,
            'message': '',
            'data': user_data
        }
        return Response(data)

