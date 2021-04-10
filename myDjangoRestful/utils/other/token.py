'''
生产token
解析token
验证token
'''
import json
import datetime
from functools import wraps
from rest_framework.response import Response

from myDjangoRestful.utils.other.des import des_descrypt, des_encrypt
import myDjangoRestful.utils.other.base64 as base64

TOKEN_HEADER = 'HTTP_ACCEPT_TOKEN'

def generateHeader():
    '''
    生成header
    '''
    header = {
        "alg": "DES",
        "typ": "JWT"
    }
    header_str = json.dumps(header, ensure_ascii=False)
    header_str_64 = base64.encode(header_str)
    return header_str_64

def getHeader(header_str_64):
    '''
    获取header
    '''
    header_str = base64.decode(header_str_64)
    header = json.loads(header_str)
    return header

def generatePayload(**kwargs):
    '''
    生成payload
    '''
    payload = {}
    for key in kwargs.keys():
        payload[key] = kwargs[key]
    effective_time = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    payload['effective_time'] = effective_time
    payload_str = json.dumps(payload, ensure_ascii=False)
    payload_str_64 = base64.encode(payload_str)
    return payload_str_64

def getPayload(payload_str_64):
    '''
    获取payload
    '''
    payload_str = base64.decode(payload_str_64)
    payload = json.loads(payload_str)
    return payload

def getPayloadFromToken(token):
    '''
    从token中获取payload
    '''
    token = token.split('.')
    payload_str_64 = token[1]
    payload_str = base64.decode(payload_str_64)
    payload = json.loads(payload_str)
    return payload

def generateSign(payload_str_64):
    '''
    生成sign
    '''
    sign = des_encrypt(payload_str_64)
    return sign

def generateToken(payload_str_64, sign: str):
    '''
    生成token
    '''
    header_str_64 = generateHeader()
    return header_str_64 + '.' + payload_str_64 + '.' + sign

def getToken(request):
    '''
    获取token
    '''
    return request.META.get(TOKEN_HEADER)

def verifyToken(token):
    '''
    验证token
    '''
    token = token.split('.')
    header_str_64 = token[0]
    payload_str_64 = token[1]
    sign = token[2]
    header = getHeader(header_str_64)
    if header['alg'] == 'DES':
        sign_des = generateSign(payload_str_64)
        if sign_des != sign:
            return False, '信息被篡改'
    payload = getPayload(payload_str_64)
    if datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") > payload['effective_time']:
        return False, '登陆过期'
    return True, ''


def token(f):
    '''
    验证token的装饰器
    '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        request = args[1]
        token = getToken(request=request)
        if not token:
            data = {
                'status_code': 404,
                'message': '访问有误'
            }
            return Response(data, status=404)
        ok, msg = verifyToken(token=token)
        if ok:
            return f(*args, **kwargs)
        else:
            data = {
                'status_code': 404,
                'message': msg
            }
            return Response(data, status=404)
    return wrapper