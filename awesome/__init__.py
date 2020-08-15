import random
import re
import base64
from dataclasses import dataclass
from typing import Dict
import requests
import hashlib
from io import BytesIO
from PIL import Image


import nonebot
import nonebot.permission as perm
from nonebot import on_natural_language, NLPSession, IntentCommand
from awesome.utils.ac import AC
from awesome.utils.bayes import Bayes
from awesome.utils.ai import AI


ac_filter = AC()
ac_filter.build()
bayes_filter = Bayes()
bayes_filter.build()


@dataclass
class Record:
    last_msg: str
    last_user_id: int
    repeat_count: int = 0


records: Dict[str, Record] = {}


def parse(msg):
    reg = re.findall('\\[CQ:image,file=.*?,url=(.*?)\\]', msg)
    return len(reg) > 0, reg


def compress(file):
    r = requests.get(file)
    o_size = int(r.headers.get('Content-Length')) / 1024
    ext = r.headers.get('Content-Type').split('/')[-1]
    img_bin = r.content
    im = Image.open(BytesIO(img_bin))
    md5 = hashlib.md5(img_bin).hexdigest()
    while o_size > 500:
        width, height = im.size
        im = im.resize((int(width * 0.5), int(height * 0.5)), Image.ANTIALIAS)
        im.save(f'{IMG_DIR}/{md5}.{ext}')
        with open(f'{IMG_DIR}/{md5}.{ext}', 'rb') as f:
            img_bin = f.read()
            o_size = len(img_bin) / 1024
            im = Image.open(BytesIO(img_bin))
    return base64.b64encode(img_bin).decode('utf-8')


@on_natural_language(only_to_me=False, permission=perm.GROUP)
async def _(session: NLPSession):
    group_id = session.event.group_id
    user_id = session.event.user_id
    msg = session.msg
    bot = nonebot.get_bot()
    has_img, files = parse(msg)
    illegal = 0
    if has_img:
        for file in files:
            illegal = await AI.img_request(img=compress(file))
            if illegal:
                break
    if illegal:
        try:
            await bot.delete_msg(**session.event)
        except:
            pass
        type = '色情' if illegal == 1 else '暴恐'
        return IntentCommand(90.0, 'img_filter', args={'user_id': user_id, 'type': type})
    record = records.get(group_id)
    ac_match = ac_filter.trie.iter(msg)
    bayes_match = bayes_filter.check(msg) if nonebot.get_bot().config.BAYES else None
    if len(list(ac_match)) or bayes_match:
        try:
            await bot.delete_msg(**session.event)
        except:
            pass
        return IntentCommand(90.0, 'text_filter', current_arg=str(user_id))
    if record is None or msg != record.last_msg:
        record = Record(msg, user_id, repeat_count=1)
        records[group_id] = record
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
