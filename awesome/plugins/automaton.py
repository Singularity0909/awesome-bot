from nonebot import on_command, CommandSession
from nonebot.command import call_command


@on_command('automaton', only_to_me=False)
async def automaton(session: CommandSession):
    await call_command(session.bot, session.ctx, 'echo',
                       current_arg=session.current_arg,
                       args=session.state)
