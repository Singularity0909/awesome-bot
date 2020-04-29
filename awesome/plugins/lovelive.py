import requests
from nonebot import on_command, CommandSession


@on_command('lovelive', aliases=('土味情话'))
async def lovelive(session: CommandSession):
    lovelive_send = await get_lovelive()
    await session.send(lovelive_send)


async def get_lovelive():
    info = get_info()
    return info


def get_info():
    url = 'https://api.lovelive.tools/api/SweetNothings'
    res = requests.get(url)
    return res.text
