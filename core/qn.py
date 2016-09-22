# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from qiniu import Auth
from qiniu import BucketManager

access_key = "vh2MauzMWeMyo87-WSrcvN46JBU3WWqpZdgtZypl"
secret_key = "HXh3wAnb3vo0zQDut5-tJlX-5abF5Qyr_tKhen1g"


def delete_file(key):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'flippy'
    ret, info = bucket.delete(bucket_name, key)
    print(info)
    return True

