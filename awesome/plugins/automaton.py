from awesome import trie
from nonebot import on_command, CommandSession


@on_command('automaton', aliases=('ac', '我要开始说脏话啦'), only_to_me=False)
async def automaton(session: CommandSession):
    text = session.get('text')
    user_id = str(session.ctx['user_id'])
    match = trie.iter(text)
    bot = session.bot
    for each in match:
        await session.send(str(each))
    if match:
        await session.send('[CQ:at,qq=' + user_id + '] 不许说脏话')


@automaton.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['text'] = stripped_arg
        return
    session.state[session.current_key] = stripped_arg