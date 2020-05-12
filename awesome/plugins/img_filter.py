from nonebot import on_command, CommandSession


@on_command('img_filter')
async def img_filter(session: CommandSession):
    user_id = session.args.get('user_id')
    type = session.args.get('type')
    await session.send('[CQ:at,qq=' + str(user_id) + '] 图片违规: ' + type)
