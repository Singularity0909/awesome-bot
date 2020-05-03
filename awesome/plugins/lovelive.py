import requests
from nonebot import on_command, CommandSession


@on_command('lovelive', aliases=('土味情话'))
async def lovelive(session: CommandSession):
    lovelive_send = await get_lovelive()
    await session.send(lovelive_send)


async def get_lovelive():
    url = 'https://api.lovelive.tools/api/SweetNothings'
    return requests.get(url).text
