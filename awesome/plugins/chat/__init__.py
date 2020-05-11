from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import render_expression

from .chat import Chat

EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    '唔……等会再告诉你'
)


@on_command('chat')
async def chat(session: CommandSession):
    message = session.state.get('message')
    if message.strip() == '':
        return
    reply = await Chat.request(text=message)
    if reply:
        await session.send(escape(reply), at_sender=True)
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND), at_sender=True)


@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(80.0, 'chat', args={'message': session.msg_text})
