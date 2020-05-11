import json
import requests
from nonebot import on_command, CommandSession


@on_command('pastebin', aliases=('贴代码', '粘贴代码', '剪切板'), only_to_me=False)
async def pastebin(session: CommandSession):
    lang = session.get('lang', prompt='你想粘贴什么语言的代码呢？')
    code = session.get('code', prompt='你想粘贴什么代码呢？')
    paste_send = await paste(code, lang)
    if not paste_send:
        paste_send = '服务暂不可用'
    await session.send(paste_send, at_sender=True)


@pastebin.args_parser
async def _(session: CommandSession):
    if session.current_key == 'lang':
        stripped_arg = session.current_arg_text.strip()
        if session.is_first_run:
            if stripped_arg:
                session.state['lang'] = stripped_arg
            return
        if not stripped_arg:
            session.pause('要粘贴的代码语言不能为空呢，请重新输入')
        elif not stripped_arg in ['plain', 'cpp', 'java', 'python', 'bash', 'markdown', 'json', 'go']:
            session.pause('目前只支持 plain, cpp, java, python, bash, markdown, json, go 哦，请重新输入')
        session.state['lang'] = stripped_arg
    if session.current_key == 'code':
        stripped_arg = session.current_arg_text.strip()
        if session.is_first_run:
            if stripped_arg:
                session.state['code'] = stripped_arg
            return
        if not stripped_arg:
            session.pause('要粘贴的代码不能为空呢，请重新输入')
        session.state['code'] = stripped_arg


async def paste(code, lang):
    url1 = 'https://api.pasteme.cn/'
    url2 = 'https://pasteme.cn/'
    params = {'lang': lang, 'content': code}
    r = requests.post(url1, json=params)
    status = r.json().get('status')
    return url2 + str(r.json().get('key')) if status == 201 else None
