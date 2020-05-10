from awesome.plugins.bullshit.generator import 狗屁不通
from nonebot import on_command, CommandSession


@on_command('bullshit', aliases=('狗屁不通', '狗屁不通生成器'), only_to_me=False)
async def bullshit(session: CommandSession):
    theme = session.get('theme', prompt='你想得到什么主题的内容呢？')
    bullshit_send = await get_bullshit(theme)
    await session.send(bullshit_send)


@bullshit.args_parser
async def _(session: CommandSession):
    user_id = session.event.user_id
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['theme'] = stripped_arg
        return
    if not stripped_arg:
        session.pause('主题不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg


async def get_bullshit(theme):
    return '    ' + 狗屁不通(theme)
