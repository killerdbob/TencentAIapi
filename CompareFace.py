import base64
import md5util
import requests
import urllib.parse
import hashlib

class TencentAPI():
    def __init__(self, appid='huangwei', appkey='huangwei'):
        self.appid = appid
        self.appkey = appkey
        self.params = {}

    def getReqSign(self, params):
        keys = sorted(params.keys())
        print(keys)
        tmpstr = ''
        for key in keys:
            if params[key] != '':
                print(urllib.parse.quote(params[key]))
                tmpstr += key + '=' + urllib.parse.quote(params[key], safe='') + '&'
        tmpstr += 'app_key=' + self.appkey
        sign = md5util.md5(tmpstr)
        return sign.upper()

    def FaceCompareAPI(self, imgA, imgB):
        url = 'https://api.ai.qq.com/fcgi-bin/face/face_facecompare'
        imgA = self.readImg(imgA)
        imgB = self.readImg(imgB)
        import time
        import random
        head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        params = {
            'app_id': self.appid,
            'image_a': imgA.encode('utf-8'),
            'image_b': imgB.encode('utf-8'),
            'time_stamp': str(int(time.time())),
            'nonce_str': str(random.random()),
            'sign': ''
        }
        params['sign'] = self.getReqSign(params)
        # data = str(params).replace("+", "%2B")
        # print('params:',data)
        response = requests.post(url=url,data=params)
        # response = requests.post(headers=head ,url=url,data=data,verify=True)
        return response

    def readImg(self, path):
        with open(path, 'rb') as f:
            img = f.read()
            img = base64.b64encode(img,)
        return img.decode()


if __name__ == '__main__':
    T = TencentAPI()
    a = T.FaceCompareAPI('test.png','test.png')
    print(a.json())
