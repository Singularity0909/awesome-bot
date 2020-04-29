import time

import requests
from nonebot import on_command, CommandSession


@on_command('translate', aliases=('翻译'))
async def translate(session: CommandSession):
    origin_text = session.get('text', prompt='你想翻译什么内容呢？')
    translate_send = await get_translate(origin_text)
    await session.send(translate_send)


@translate.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['text'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('要翻译的文本不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg


async def get_translate(origin_text):
    info = get_info(origin_text)
    return info


def get_info(origin_text):
    url1 = 'https://www.mxnzp.com/api/convert/translate?content='
    origin_lan = 'auto'
    result_lan = 'en'
    url2 = origin_text + '&from=' + origin_lan + '&to=' + result_lan
    url3 = '&app_id=lbeqhqhnhgo22otp&app_secret=OFpUMnhWOEhoVWNkM3dOaVV2dnhQQT09'
    res = requests.get(url1 + url2 + url3)
    time.sleep(0.8)
    origin_lan = res.json()['data']['originLanguage']
    if origin_lan == 'zh':
        result_lan = 'en'
    else:
        result_lan = 'zh'
    url2 = origin_text + '&from=' + origin_lan + '&to=' + result_lan
    res = requests.get(url1 + url2 + url3)
    return res.json()['data']['result']
