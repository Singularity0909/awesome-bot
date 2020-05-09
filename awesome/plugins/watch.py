import random
from dataclasses import dataclass
from typing import Dict

import nonebot.permission as perm
from awesome import trie
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id


@dataclass
class Record:
    last_msg: str
    last_user_id: int
    repeat_count: int = 0


records: Dict[str, Record] = {}


@on_natural_language(only_to_me=False, permission=perm.GROUP)
async def _(session: NLPSession):
    group_ctx_id = context_id(session.ctx, mode='group')
    user_id = session.ctx['user_id']
    msg = session.msg
    record = records.get(group_ctx_id)
    match = trie.iter(msg)
    if len(list(match)):
        return IntentCommand(
            90.0,
            'automaton',
            args={'message': '[CQ:at,qq=' + str(user_id) + '] 不许说脏话'}
        )
    if record is None or msg != record.last_msg:
        record = Record(msg, user_id, repeat_count=1)
        records[group_ctx_id] = record
        return
    if record.last_user_id == user_id:
        return
    record.last_user_id = user_id
    record.repeat_count += 1
    if record.repeat_count == 2:
        return IntentCommand(
            90.0,
            'repeater',
            args={'delay': random.randint(5, 20) / 10, 'message': msg}
        )
