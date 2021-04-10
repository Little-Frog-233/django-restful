import os
import sys
import json
import datetime
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from myDjangoRestful.model.mysql import Datasource as _Datasource
from myDjangoRestful.utils.other.md5 import md5

# class DatasourceSerializer(serializers.ModelSerializer):
class DatasourceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hash_id = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)
    options = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    tips = serializers.CharField(required=False, allow_blank=True)
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def create(self, vaildated_data):
        name = vaildated_data.get('name', 'unknown')
        user_id = vaildated_data.get('user_id', '0')
        vaildated_data['hash_id'] = md5("%s_%s_%s" %(name, user_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return _Datasource.objects.create(**vaildated_data)

    # class Meta:
    #     model = _Datasource
    #     fields = ('id', 'user_id', 'type', 'options', 'create_time', 'update_time', 'name', 'tips', 'hash_id',)


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, status_code, data, message='', **kwargs):
#         res = {
#             'status_code': status_code,
#             'message': message,
#             'data': data
#         }
#         content = JSONRenderer().render(res)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


# def datasourceList(request):
#     '''
#     '''
#     if request.method == 'GET':
#         dss = _Datasource.objects.all()
#         serializer = DatasourceSerializer(dss, many=True) #当序列化值为列表的时候，many=True
#         return JSONResponse(200, serializer.data)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = DatasourceSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(201, [], status=201)
#         else:
#             return JSONResponse(400, serializer.errors, status=400)
#     else:
#         return JSONResponse(404, [], status=404)

# def datasourceDetail(request, id):
#     '''
#     '''
#     try:
#         ds = _Datasource.objects.get(id=id)
#     except _Datasource.DoesNotExist:
#         return HttpResponse(status=404)
    
#     if request.method == 'GET':
#         serializer = DatasourceSerializer(ds)
#         return JSONResponse(200, serializer.data)
#     else:
#         return JSONResponse(404, [], status=404)

class DatasourceApiView(APIView):
    '''
    '''
    def get(self, request, format=None):
        # print(request.query_params.get('page'))
        # print(request.query_params.get('size'))
        dss = _Datasource.objects.all()
        serializer = DatasourceSerializer(dss, many=True)
        for item in serializer.data:
            item['options_dict'] = json.loads(item['options'])
        data = {
            'status_code': 200,
            'message': '',
            'data': serializer.data
        }
        return Response(data)
    
    def post(self, request, format=None):
        try:
            form_data = request.data
            print(form_data)
            print(form_data['type'])
            serializer = DatasourceSerializer(data=form_data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
            data = {
                'status_code': 200,
                'message': '',
            }
            return Response(data)
        except Exception as e:
            msg = 'On line {} - {}'.format(sys.exc_info()[2].tb_lineno, e)
            data = {
                'status_code': 500,
                'message': msg,
            }
            return Response(data, status=500)

class DatasourceDetailApiView(APIView):
    '''
    '''
    def get(self, request, hash_id, format=None):
        try:
            ds = _Datasource.objects.get(hash_id=hash_id)
        except _Datasource.DoesNotExist:
            data = {
                'status_code': 404,
                'message': 'not exist'
            }
            return Response(data, status=404)
        serializer = DatasourceSerializer(ds)
        data = {
            'status_code': 200,
            'message': '',
            'data': serializer.data
        }
        return Response(data)

# class DatasourceApi(viewsets.ModelViewSet):
#     '''
#     '''
#     queryset = _Datasource.objects.all()
#     serializer_class = DatasourceSerializer