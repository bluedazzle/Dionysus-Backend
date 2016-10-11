# coding: utf-8
from qiniu import Auth
from qiniu import BucketManager
import requests

access_key = "vh2MauzMWeMyo87-WSrcvN46JBU3WWqpZdgtZypl"
secret_key = "HXh3wAnb3vo0zQDut5-tJlX-5abF5Qyr_tKhen1g"


def delete_file(key):
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'flippy'
    ret, info = bucket.delete(bucket_name, key)
    return True


def generate_upload_token():
    q = Auth(access_key, secret_key)
    token = q.upload_token('flippy')
    return token

def add_water_mask(key):
    data = '/pfop?bucket=flippy&key={0}&fops=avthumb%2fmp4%2fwmImage%2faHR0cDovL2Rpb255c3VzLmZpYmFyLmNuL3MvaW1hZ2Uvd2F0ZXIucG5n%2fwmGravity%2fNorthWest&notifyURL=http%3A%2F%2Fdionysus.fibar.cn%2Fapi%2Fv1%2Fnotify\n'.format(key)
    q = Auth(access_key, secret_key)
    sign = q.token(data)
    sign = 'QBox {0}'.format(sign)
    url = 'http://api.qiniu.com/pfop?bucket=flippy&key={0}&fops=avthumb%2fmp4%2fwmImage%2faHR0cDovL2Rpb255c3VzLmZpYmFyLmNuL3MvaW1hZ2Uvd2F0ZXIucG5n%2fwmGravity%2fNorthWest&notifyURL=http%3A%2F%2Fdionysus.fibar.cn%2Fapi%2Fv1%2Fnotify'.format(key)
    res = requests.post(url, headers={'Authorization': sign})
    print res.content