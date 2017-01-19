# coding: utf-8
from __future__ import unicode_literals

import copy
import hashlib

import datetime
import re

import requests
import time

import srt
from PIL import Image

from Dionysus.settings import BASE_DIR
from core.models import Secret

import random
import string

UPLOAD_PATH = BASE_DIR + '/static'


def create_secret(count=64):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def create_token(count=32):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def check_sign(timestamp, sign):
    secret = Secret.objects.all()[0].secret
    check = unicode(hashlib.md5('{0}{1}'.format(timestamp, secret)).hexdigest()).upper()
    if check == unicode(sign).upper():
        return True
    return False


def save_image(url, type='upload', name="default.jpg"):
    try:
        dir_path = '/image/{0}/{1}'.format(type, name)
        save_path = '{0}{1}'.format(UPLOAD_PATH, dir_path)
        response = requests.get(url, stream=True)
        image = response.content
        with open(save_path, "wb") as jpg:
            jpg.write(image)
            return True, '/s{0}'.format(dir_path)
    except IOError:
        print("IO Error\n")
        return False, None
    except Exception, e:
        return False, None


def upload_picture(pic_file):
    pic_name = "{0}{1}".format(unicode(time.time()).replace('.', ''), pic_file.name)
    pic_path = '/image/upload/{0}'.format(pic_name)
    save_path = UPLOAD_PATH + pic_path
    img = Image.open(pic_file)
    img.save(save_path)
    return '/s{0}'.format(pic_path), save_path


def create_game_id(type='01'):
    return '{0}{1}{2}'.format(unicode(time.time()).replace('.', ''), type, random.randint(1000, 9999))


def create_tournament_id(type='02'):
    return '{0}{1}{2}'.format(unicode(time.time()).replace('.', ''), type, random.randint(1000, 9999))


def serialize_srt(srt_data):
    # subs = srt.parse(srt_data)
    # sub_list = []
    # for sub in subs:
    #     sub_dict = {'index': sub.index,
    #                 'start_time': unicode(sub.start),
    #                 'end_time': unicode(sub.end),
    #                 'content': sub.content}
    #     sub_list.append(sub_dict)
    # return sub_list
    block_list = []
    subs = []
    start = 0
    for i, line in enumerate(srt_data):
        if line == '\r\n':
            block_list.append(srt_data[start: i])
            start = i + 1
    for block in block_list:
        sub = {}
        if len(block) == 3:
            block = map(lambda x: x.decode('utf-8').replace('\r\n', ''), block)
            sub['index'] = block[0]
            start, end = block[1].replace(',', '.').split('-->')
            sub['start_time'] = start.strip()
            sub['end_time'] = end.strip()
            sub['content'] = block[2]
            subs.append(sub)
    return subs
