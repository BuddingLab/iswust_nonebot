from nonebot import CommandSession, on_command
from requests import Response

from app.bot.constants.config import api_url
from utils.aio import requests
from utils.tools import bot_hash

__plugin_name__ = '更新课表'
__plugin_usage__ = r"""输入 更新课表或者uc
""".strip()


@on_command('uc', aliases=('更新课表'))
async def uc(session: CommandSession):
    sender = session.ctx.get('sender', {})
    sender_qq = sender.get('user_id')
    await session.send(f'正在更新课表...')
    r: Response = await requests.get(api_url + 'api/v1/course/getCourse',
                                     params={
                                         "qq": sender_qq,
                                         "token": bot_hash(sender_qq),
                                         "update": '1'
                                     })
    if r:
        r = await r.text
        await session.finish(r.encode('utf-8').decode('utf-8'))
    await session.finish('更新出错')