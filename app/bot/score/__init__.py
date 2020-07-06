from loguru import logger
from nonebot import CommandSession, on_command

from .service import ScoreService

__plugin_name__ = "查询成绩"
__plugin_short_description__ = "命令：score"
__plugin_usage__ = r"""
帮助链接：https://bot.artin.li/guide/score.html

输入 查询成绩/成绩
    使用方法：
    成绩"""


@on_command("score", aliases=("查询成绩", "成绩"))
async def score(session: CommandSession):
    sender_qq = session.event.get("user_id")
    try:
        await ScoreService.send_score(sender_qq)
    except Exception as e:
        logger.exception(e)
        await session.send("查询出错")


@score.args_parser
async def _(session: CommandSession):
    pass