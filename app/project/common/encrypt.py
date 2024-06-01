# -*- coding: utf-8 -*-
#
# 加解密模块
#
# Author: alex cai
# Email: caiyingyao@ibbd.net
# Created Time: 2024-06-01
import json
import base64
import hashlib
import random
import string
from typing import Tuple
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKC
from Crypto.Signature import PKCS1_v1_5 as Signature_PKC


def generate_random_string(length: int) -> str:
    # 定义可能的字符集
    characters = string.ascii_letters + string.digits
    # 使用random.choices从字符集中随机选择字符，形成指定长度的字符串
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def dict_serialize(params: dict) -> str:
    """将字典数据序列化
    Args:
        params (dict): 字典参数数据
    Returns:
        str: 序列化后的字符串
    """
    params_list = sorted(params.items())
    # print("将参数键值对列表按下标进行排序: ", params_list)
    params_str = json.dumps(params_list)
    params_str = params_str.replace(" ", "")
    # print("参数转成json字符串并去除空格: ", params_str)
    return params_str


def md5(plain_text: str) -> str:
    """md5加密函数
    Args:
        plain_text (str): 明文字符串
    Returns:
        str: md加密后的字符串
    """
    # 创建md5对象
    md5_hash = hashlib.md5()
    # 需要确保输入的是字节串，因此对字符串进行编码
    md5_hash.update(plain_text.encode('utf-8'))
    # 返回MD5哈希值的十六进制表示
    return md5_hash.hexdigest()


def md5_signature(message: str, password: str) -> str:
    """使用md5生成签名字符串
    Args:
        message (str): 待签名字符串
    Returns:
        str: 签名后的字符串
    """
    salt = generate_random_string(16)
    md5_str = md5(salt + message + password)
    return salt + md5_str


def md5_signature_verify(message: str, password: str, sign_text: str) -> bool:
    """md5签名字符串校验
    Args:
        message (str): 待签名字符串
    Returns:
        bool: 签名字符串检验是否成功
    """
    salt, md5_str = sign_text[:16], sign_text[16:]
    return md5_str == md5(salt + message + password)


def create_rsa_key(key_length: int = 1024) -> Tuple[str, str]:
    """生成RSA公私钥
    Args:
        key_length (int, optional): RSA key 长度. Defaults to 1024.
    Returns:
        Tuple[str, str]: 私钥, 公钥
    """
    # 伪随机数生成器
    random_gen = Random.new().read
    # 生成秘钥对实例对象：1024是秘钥的长度
    rsa = RSA.generate(key_length, random_gen)
    # 生成公私钥
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return private_pem.decode(encoding="utf8"), public_pem.decode(encoding="utf8")


def rsa_encrypt(plain_text: str, public_pem: str) -> str:
    """RSA公钥加密
    Args:
        plain_text (str): 加密前明文
        public_pem (str): 公钥字符串
    Returns:
        str: 加密后字符串
    """
    # 加载公钥
    rsa_key = RSA.import_key(public_pem)
    # 加密
    cipher_rsa = Cipher_PKC.new(rsa_key)
    en_data = cipher_rsa.encrypt(plain_text.encode("utf-8"))  # 加密
    # base64 进行编码
    base64_text = base64.b64encode(en_data)
    return base64_text.decode(encoding="utf8")  # 返回字符串


def rsa_decrypt(encrypted_text: str, private_pem: str) -> str:
    """解密函数
    Args:
        encrypted_text (str): 加密后的字符串
        private_pem (str): 私钥字符串
    Returns:
        str: 返回解密之后的明文字符串
    """
    # base64 解码
    base64_data = base64.b64decode(encrypted_text.encode("utf-8"))
    # 读取私钥
    private_key = RSA.import_key(private_pem)
    # 解密
    cipher_rsa = Cipher_PKC.new(private_key)
    data = cipher_rsa.decrypt(base64_data, None)
    return data.decode(encoding="utf8")


def dict_signature(data: dict, private_pem: str) -> str:
    """对字典进行签名
    Args:
        data (dict): 待签名的字典数据
        private_pem (str): 私钥字符串
    Returns:
        str: 签名后的字符串
    """


def rsa_signature(message: str, private_pem: str) -> str:
    """RSA签名函数
    Args:
        message (str): 待签名字符串
        private_pem (str): 私钥字符串
    Returns:
        str: 签名字符串
    """
    # 读取私钥
    private_key = RSA.import_key(private_pem)
    # 根据SHA256算法处理签名内容message
    sha_data = SHA256.new(message.encode("utf-8"))

    # 私钥进行签名
    signer = Signature_PKC.new(private_key)
    sign = signer.sign(sha_data)
    # 将签名后的内容，转换为base64编码
    sign_base64 = base64.b64encode(sign)
    return sign_base64.decode(encoding="utf8")


def rsa_verify(message: str, signature: str, public_pem: str) -> bool:
    """RSA签名校验
    Args:
        message (str): 待签名字符串
        signature (str): 签名字符串
        public_pem (str): 公钥字符串
    Returns:
        bool: 签名校验是否成功
    """
    # 接收到的sign签名 base64解码
    sign_data = base64.b64decode(signature.encode("utf-8"))

    # 加载公钥
    piblic_key = RSA.importKey(public_pem)

    # 根据SHA256算法处理签名之前内容message
    sha_data = SHA256.new(message.encode("utf-8"))  # b类型

    # 验证签名
    signer = Signature_PKC.new(piblic_key)
    ok = signer.verify(sha_data, sign_data)
    return ok


if __name__ == '__main__':
    password = "123456"
    plain_text = "hello client, this is a message"
    md5_sign = md5_signature(plain_text, password)
    print(md5_sign)
    assert md5_signature_verify(plain_text, password, md5_sign)

    priv_pem, pub_pem = create_rsa_key()
    e = rsa_encrypt(plain_text, pub_pem)
    d = rsa_decrypt(e, priv_pem)
    assert plain_text == d

    plain_text = "a"*1000
    sign_text = rsa_signature(plain_text, priv_pem)
    print("sign len:", len(sign_text), sign_text)
    assert rsa_verify(plain_text, sign_text[:10]+"bb"+sign_text[12:], pub_pem) is False
    assert rsa_verify(plain_text, sign_text, pub_pem) is True
