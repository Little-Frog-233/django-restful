import hashlib


def md5(text):
    '''
    md5加密字符串
    '''
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()