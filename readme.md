# Dionysus API


---

**host: http://dionysus.fibar.cn**

**api_version: v1**

#概要

 2. API请求格式：host + "api" + api_version + 请求地址。
 3. API返回格式：`json:{"status":1,"body":{}}`status返回操作结果码,body包含返回信息，如果无返回信息，body为空。
 4. status结果码对照表： 
 
|status结果码|状态|
| --------------  | :---: |
|0|未知错误|
|1|成功|
|2|权限不足|
|3|帐号不存在|
|4|数据错误|
|5|密码错误|
|6|已存在|
|7|不存在|
|8|已过期|
|10|验证码为空|
|11|验证码错误| 


#API安全

为保证接口调用安全，所有接口都需要：`timestamp`与`sign`两个参数，用来验证接口请求的合法性。其中： 


 1. `timestamp`是类型为数字的10位的时间戳，代表发生请求时的时间。
 2. `sign` 是类型为字符串的32位验证字符串，具体生成方式为`MD5(timestamp + secret)`，其中`secret` 从系统申请后分配。请保证`secret` 的安全性，如果不慎泄露请及时更换。
 3. 验证合法性请均使用`get`方式构造参数请求，即在所有请求地址后构造类似`?timestamp=xx&sign=xx`的参数

#文档

#视频
##**获取视频列表**
```
GET /videos
```
###**Parameters**
* type(_Required_|integer)-视频类别
* like(_Optional_|integer)-最热视频
* search(-Optional_|string)-搜索内容
* page(_Optional_|integer)-分页

|type码|状态|
| --------------  | :---: |
|1|电影|
|2|mv|
|3|搞笑|

###**Return**
成功
```
{
  "body": {
    "page_obj": {},
    "is_paginated": false,
    "video_list": [
      {
        "classification": 1,
        "thumb_nail": "http://oda176fz0.bkt.clouddn.com/WeChatSight2.mp4?vframe/jpg/offset/1/w/200/h/200/",
        "reference": "dd",
        "title": "WeChatSight2",
        "url": "http://oda176fz0.bkt.clouddn.com/WeChatSight2.mp4",
        "author": "pp",
        "create_time": "2016-09-12 15:31:52",
        "modify_time": "2016-09-12 15:31:52",
        "id": 1,
        "like": 0
      },
      {
        "classification": 1,
        "thumb_nail": "http://oda176fz0.bkt.clouddn.com/别担心，我罩着你呢.avi?vframe/jpg/offset/1/w/200/h/200/",
        "reference": "女间谍",
        "title": "别担心，我罩着你呢",
        "url": "http://oda176fz0.bkt.clouddn.com/别担心，我罩着你呢.avi",
        "author": "皮皮",
        "create_time": "2016-09-12 15:44:27",
        "modify_time": "2016-09-12 15:44:27",
        "id": 2,
        "like": 0
      }
    ]
  },
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}
```

##**获取视频详细信息**
```
GET /video/<id>
```

###**Return**
成功
```
{
  "body": {
    "video": {
      "classification": 1,
      "thumb_nail": "http://oda176fz0.bkt.clouddn.com/WeChatSight2.mp4?vframe/jpg/offset/1/w/200/h/200/",
      "reference": "dd",
      "author": "pp",
      "url": "http://oda176fz0.bkt.clouddn.com/WeChatSight2.mp4",
      "title": "WeChatSight2",
      "tracks": [
        {
          "create_time": "2016-09-12 15:31:52",
          "data": "{\"0\":{\"x\":540,\"y\":122,\"size\":-1},\"2.67\":{\"x\":548,\"y\":130,\"size\":-1},\"4.09\":{\"x\":540,\"y\":104,\"size\":-1},\"4.63\":{\"x\":540,\"y\":104,\"size\":-1},\"5.76\":{\"x\":525,\"y\":150,\"size\":-1},\"6.55\":{\"x\":532,\"y\":109,\"size\":-1}}",
          "id": 1,
          "video_id": 1
        }
      ],
      "create_time": "2016-09-12 15:31:52",
      "id": 1,
      "like": 0
    }
  },
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}

```

##**分享视频**
```
POST /share
```
###**Parameters**
* url(_Required_|string)-视频链接
* uid(_Required_|string)-用户识别码
* vid(_Required_|string)-被变脸视频id

###**Return**
成功
```
{
  "body": {},
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}

```

##**获取上传token**
```
get /upload
```

###**Return**
成功
```
{
  "body": {"uptoken": "xxx"},
  "status": 1,
  "msg": "success"
}
```
失败
```
{
  "body": {},
  "status": 4,
  "msg": "数据缺失"
}

```