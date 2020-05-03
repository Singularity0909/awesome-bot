import requests
from nonebot import on_command, CommandSession


@on_command('hitokoto', aliases=('一言'))
async def hitokoto(session: CommandSession):
    hitokoto_send = await get_hitokoto()
    await session.send(hitokoto_send)


async def get_hitokoto():
    url = 'https://v1.hitokoto.cn'
    res = requests.get(url)
    info_content = res.json()['hitokoto']
    info_from = res.json()['from']
    return info_content + ' —— ' + info_from;