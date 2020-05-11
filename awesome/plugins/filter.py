from nonebot import on_command, CommandSession


@on_command('filter')
async def automaton(session: CommandSession):
    user_id = session.current_arg
    await session.send('[CQ:at,qq=' + user_id + '] 言语违规')
