import requests
from nonebot import on_command, CommandSession


@on_command('hitokoto', aliases=('一言'))
async def hitokoto(session: CommandSession):
    hitokoto_send = await get_hitokoto()
    await session.send(hitokoto_send)


async def get_hitokoto():
    info = get_info()
    str = info[0] + ' —— ' + info[1]
    return str


def get_info():
    url = 'https://v1.hitokoto.cn'
    res = requests.get(url)
    info_sen = res.json()['hitokoto']
    info_src = res.json()['from']
    return [info_sen, info_src]
