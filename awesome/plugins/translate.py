import time

import requests
from nonebot import on_command, CommandSession


@on_command('translate', aliases=('翻译', '翻译一下'), only_to_me=False)
async def translate(session: CommandSession):
    user_id = session.event.user_id
    origin_text = session.get('text', prompt='你想翻译什么内容呢？')
    translate_send = await get_translation(origin_text)
    await session.send(translate_send, at_sender=True)


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


async def get_translation(source_text):
    url1 = 'https://www.mxnzp.com/api/convert/translate?content='
    source_lan = 'auto'
    target_lan = 'en'
    url2 = source_text + '&from=' + source_lan + '&to=' + target_lan
    url3 = '&app_id=lbeqhqhnhgo22otp&app_secret=OFpUMnhWOEhoVWNkM3dOaVV2dnhQQT09'
    res = requests.get(url1 + url2 + url3)
    time.sleep(0.8)
    source_lan = res.json()['data']['originLanguage']
    if source_lan == 'zh':
        target_lan = 'en'
    else:
        target_lan = 'zh'
    url2 = source_text + '&from=' + source_lan + '&to=' + target_lan
    res = requests.get(url1 + url2 + url3)
    return res.json()['data']['result']
