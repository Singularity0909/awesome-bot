import hashlib
import json
import string
import time
from random import randint
from typing import Optional
from urllib.parse import urlencode

import aiohttp
from nonebot import CommandSession
from nonebot.helpers import context_id


def get_nonce_str():
    nonce_str_example = 'fa577ce340859f9fe'
    nonce_str = ''
    len_str = string.digits + string.ascii_letters
    for i in range(len(nonce_str_example)):
        nonce_str += len_str[randint(0, len(len_str) - 1)]
    return nonce_str


def sign(req_data, app_key):
    new_list = sorted(req_data.items())
    encode_list = urlencode(new_list)
    req_data = encode_list + "&" + "app_key" + "=" + app_key
    md5 = hashlib.md5()
    md5.update(req_data.encode('utf-8'))
    data = md5.hexdigest()
    return data.upper()


async def call_txchat_api(session: CommandSession, text: str) -> Optional[str]:
    app_id = session.bot.config.APP_ID
    app_key = session.bot.config.APP_KEY
    api_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
    req_data = {
        'app_id': app_id,
        'time_stamp': int(time.time()),
        'nonce_str': get_nonce_str(),
        'session': context_id(session.ctx, use_hash=True),
        'question': text,
    }
    print('Now Session: ' + context_id(session.ctx, use_hash=True) + '\n')
    req_data['sign'] = sign(req_data, app_key)
    req_data = sorted(req_data.items())
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(api_url, params=req_data) as response:
                try:
                    data = json.loads(await response.text())
                    if data['ret'] == 0:
                        print('Answer: ' + data['data']['answer'] + '\n')
                        return data['data']['answer']
                    else:
                        return None
                except:
                    print(await response.text())
                    return None
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        return None
