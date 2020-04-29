import requests
from nonebot import on_command, CommandSession


@on_command('joke', aliases=('笑话', '讲个笑话', '烂俗笑话'))
async def joke(session: CommandSession):
    joke_send = await get_joke()
    await session.send(joke_send)


async def get_joke():
    joke = get_info()
    return joke


def get_info():
    url = 'https://www.mxnzp.com/api/jokes/list/random'
    header = {'app_id': 'lbeqhqhnhgo22otp', 'app_secret': 'OFpUMnhWOEhoVWNkM3dOaVV2dnhQQT09'}
    res = requests.get(url, headers=header)
    print(res)
    return res.json()['data'][0]['content']
