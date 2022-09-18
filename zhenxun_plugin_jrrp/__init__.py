from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, Message, MessageSegment
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.event import Event
from nonebot.adapters.onebot.v11 import Bot,Message, MessageEvent
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP
from typing import List
import time

__zx_plugin_name__ = "每日人品"
__plugin_usage__ = """
usage：
    每日人品
    指令：
        jrrp(任意字符串，建议为QQ号)获取你的(任意字符串的)今日人品
        j(任意字符串，建议为QQ号)获取你的(任意字符串的)今日人品
""".strip()
__plugin_des__ = "今日人品"
__plugin_cmd__ = ["jrrp/j"]
__plugin_settings__ = {
    "level": 5,             # 群权限等级，请不要设置为1或999，若无特殊情况请设置为5
    "default_status": True,     # 进群时的默认开关状态
    "limit_superuser": False,   # 开关插件的限制是否限制超级用户
    "cmd": ["每日人品", 'jrrp'],   # 命令别名，主要用于帮助和开关
    "cost_gold": 0,             # 该功能需要花费的金币
}

jrrp = on_command("jrrp", aliases = {"j"}, permission=GROUP, priority=50)
message: List[dict] = [
	{
		"expr": "jrrp == 100",
		"start": "！！！！！你今天的人品值是：",
		"end": "！100！100！！！！！"
	},
	{
		"expr": "jrrp == 99",
		"end": "！但不是 100……"
	},
	{
		"expr": "jrrp >= 90",
		"end": "！好评如潮！"
	},
	{
		"expr": "jrrp >= 60",
		"end": "！是不错的一天呢！"
	},
	{
		"expr": "jrrp > 50",
		"end": "！还行啦还行啦。"
	},
	{
		"expr": "jrrp == 50",
		"end": "！五五开……"
	},
	{
		"expr": "jrrp >= 40",
		"end": "！还……还行吧……？"
	},
	{
		"expr": "jrrp >= 11",
		"end": "！呜哇……"
	},
	{
		"expr": "jrrp >= 1",
		"end": "……（没错，是百分制）"
	},
	{
		"expr": "True",
		"end": "……"
	}
]
@jrrp.handle()
async def _h(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    words = args.extract_plain_text()
    if not words:
        session = event.get_session_id()
        id = session.split('_')[2]
    if words:
        id = words
    jrrp_num = get_jrrp(str(id))
    result = get_msg(jrrp_num)
    reply = MessageSegment.reply(event.message_id)
    await jrrp.send(reply + result)

def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)

def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399

def get_jrrp(string: str):
    now = time.localtime()
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        string,
        "0*8&6",
        str(now.tm_mday),
        "kjhg"
    ])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2

def get_msg(jrrp):
    start: str = "你今天的人品值是："
    end: str = "……"
    for msg_obj in message:
        if eval(msg_obj["expr"]):
            start = msg_obj.get("start") if msg_obj.get("start") else start
            end = msg_obj.get("end") if msg_obj.get("end") else end
            lumsg = start + str(jrrp) + end
            return lumsg
