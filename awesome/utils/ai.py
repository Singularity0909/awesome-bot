import hashlib
import string
import time
from random import randint
from urllib.parse import urlencode

import requests
import httpx
import nonebot


class AI(object):
    url_textchat = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    url_img_porn = 'https://api.ai.qq.com/fcgi-bin/vision/vision_porn'
    url_img_terrorism = 'https://api.ai.qq.com/fcgi-bin/image/image_terrorism'
    app_id = nonebot.get_bot().config.APP_ID
    app_key = nonebot.get_bot().config.APP_KEY
    nonce_str_example = 'fa577ce340859f9fe'
    ct = lambda: time.time()

    @classmethod
    def get_nonce_str(self):
        nonce_str = ''
        len_str = string.digits + string.ascii_letters
        for i in range(len(self.nonce_str_example)):
            nonce_str += len_str[randint(0, len(len_str) - 1)]
        return nonce_str

    @classmethod
    def sign(self, req_data):
        new_list = sorted(req_data.items())
        encode_list = urlencode(new_list)
        req_data = encode_list + "&" + "app_key" + "=" + self.app_key
        md5 = hashlib.md5()
        md5.update(req_data.encode('utf-8'))
        data = md5.hexdigest()
        return data.upper()

    @classmethod
    async def text_request(self, text):
        req_data = {
            'app_id': self.app_id,
            'time_stamp': int(self.ct()),
            'nonce_str': self.get_nonce_str(),
            'session': 10000,
            'question': text,
        }
        req_data['sign'] = self.sign(req_data)
        req_data = sorted(req_data.items())
        requests = httpx.AsyncClient()
        result = await requests.get(self.url_textchat, params=req_data)
        await requests.aclose()
        result = result.json()
        print(result)
        if result['ret'] == 0:
            return result['data']['answer']
        return None

    @classmethod
    async def img_request(self, img):
        req_data = {
            'app_id': self.app_id,
            'time_stamp': int(self.ct()),
            'nonce_str': self.get_nonce_str(),
            'image': img,
        }
        req_data['sign'] = self.sign(req_data)
        req_data = sorted(req_data.items())
        result = requests.post(self.url_img_porn, data=req_data).json()
        print(result)
        if result['ret'] == 0:
            for tag in result['data']['tag_list']:
                if tag.get('tag_name') == 'porn' and tag.get('tag_confidence') > 83:
                    return 1
        result = requests.post(self.url_img_terrorism, data=req_data).json()
        print(result)
        tag_list = ['terrorists', 'knife', 'guns', 'blood', 'fire']
        if result['ret'] == 0:
            for tag in result['data']['tag_list']:
                if tag.get('tag_name') in tag_list and tag.get('tag_confidence') >= 83:
                    return 2
        return 0
