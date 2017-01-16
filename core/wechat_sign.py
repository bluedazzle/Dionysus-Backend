# -*- coding: utf-8 -*-
import time
import random
import string
import hashlib


class Sign:
    def __init__(self, appId, appSecret):
        self.appId = appId
        self.appSecret = appSecret
        self.ret = {}

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self, url, ticket):
        self.ret['url'] = url
        self.ret['timestamp'] = self.__create_timestamp()
        self.ret['timestamp'] = self.__create_nonce_str()
        self.ret['jsapi_ticket'] = ticket
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret


wechat_sign = Sign('wx8f04e633e9b5d33c', 'f5f8353ac90c783fdf71a05f9ee0c835')
