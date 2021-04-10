# coding:utf-8
from pyDes import des, CBC, PAD_PKCS5
import binascii

# 秘钥
KEY = 'mHAxsLYz'


def des_encrypt(s):
	"""
	DES 加密
	:param s: 原始字符串
	:return: 加密后字符串，16进制
	"""
	secret_key = KEY
	iv = secret_key
	k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
	en = k.encrypt(s, padmode=PAD_PKCS5)
	res = binascii.b2a_hex(en)
	res = res.decode('utf-8')
	return res


def des_descrypt(s):
	"""
	DES 解密
	:param s: 加密后的字符串，16进制
	:return:  解密后的字符串
	"""
	secret_key = KEY
	iv = secret_key
	k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
	de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
	if type(de) is not str:
		de = de.decode('utf-8')
	return de


if __name__ == '__main__':
	print(des_encrypt('eyJ1c2VyX2lkIjogMSwgInVzZXJfcGljdHVyZSI6ICJwaW5nbXVrdWFpemhhb18yMDIwLTA4LTE0\nX3NoYW5nd3UxMC41NC4zMC5wbmciLCAiZWZmZWN0aXZlX3RpbWUiOiAiMjAyMS0wNC0yMyAxNTo0\nODoyNyJ9\n'))
	print(des_descrypt('285f8ddaa524483458f382dc66f79a5e6fe7e01546b03d0d5f76cbdd9cbc741c26b3378ededf1cf417047e24c7e5323a3ac87cc5df4c711a4a76289d41c241d0b83896517f549bfabe6ad42c75602402b31b0217cd9328e0411e01b46568fac31b9af011123dc86193884ae89b6c769e1a2f770e7841f7cb9d6c966a1632e43e09d9578deeca573b4e40d4ff31acb830445702f3951bdb3a60fe42ca79469bfa90bfb6a803151c7c'))
