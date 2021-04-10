import base64

def encode(text):
    '''
    base64加密
    '''
    text = text.encode('utf-8')
    code = base64.b64encode(text)
    code = code.decode('utf-8')
    return code

def decode(code):
    '''
    base64解密
    '''
    code = code.encode('utf-8')
    code = base64.b64decode(code)
    text = code.decode('utf-8')
    return text