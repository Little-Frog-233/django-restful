from myDjangoRestful.model.mysql import Chart as _Chart
from rest_framework import serializers
from rest_framework import viewsets
from myDjangoRestful.dao.mysql import *


class ChartSerializer(serializers.HyperlinkedModelSerializer):
    '''
    序列化
    '''
    # 时间格式化
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = _Chart
        fields = ('id', 'creater_id', 'hash_id', 'options', 'create_time',
                  'update_time')


class ChartApi(viewsets.ModelViewSet):
    queryset = getAllChart()
    serializer_class = ChartSerializer