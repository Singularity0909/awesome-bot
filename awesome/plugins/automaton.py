from nonebot import on_command, CommandSession
from nonebot.command import call_command


@on_command('automaton')
async def automaton(session: CommandSession):
    user_id = session.state.get('user_id')
    message = '[CQ:at,qq=' + str(user_id) + '] 言语违规'
    args = {'message': message}
    await call_command(session.bot, session.ctx, 'echo',
                       current_arg=session.current_arg,
                       args=args)
