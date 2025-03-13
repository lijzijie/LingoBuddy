# 用户列表(请配置要和bot说话的账号的昵称或者群名，不要写备注！)
LISTEN_LIST = ['Ziggy']
# 机器人的微信名称
ROBOT_WX_NAME = 'LingoBuddy'
# DeepSeek API 配置

# 硅基API
# 硅基流动API注册地址，免费15元额度 https://cloud.siliconflow.cn/i/Pt3ookVq
# DEEPSEEK_BASE_URL = 'https://api.siliconflow.cn/v1/'
# MODEL = 'deepseek-ai/DeepSeek-V3'

# 官方API的V3模型
# DEEPSEEK_BASE_URL = https://api.deepseek.com
#  MODEL = deepseek-chat

# 联网功能API
# DEEPSEEK_API_KEY = 'sk-'
# DEEPSEEK_BASE_URL = 'https://search-for-llmapi.dawne.cn/with-search/v1'
# MODEL = 'siliconflow@deepseek-ai/DeepSeek-V2.5'

# 火山引擎API
# 火山引擎 API注册地址，免费15元额度 https://volcengine.com/L/
# 邀请码 9g0KQ6aar60
DEEPSEEK_BASE_URL = 'https://ark.cn-beijing.volces.com/api/v3'
DEEPSEEK_API_KEY = ''
MODEL = 'deepseek-v3-241226'

# 如果要使用本地的ai API，把模型和API地址改成本地的

# 回复最大token
MAX_TOKEN = 1000
#温度
TEMPERATURE = 1.1

#最大的上下文轮数
MAX_GROUPS = 15
#prompt文件名
PROMPT_NAME = 'data/lingobuddy/wango/wango.md'# prompt文件路径
#表情包存放目录
EMOJI_DIR = 'data/lingobuddy/wango/emoji'# 表情包目录

#语音配置（请配置自己的tts服务）
# MiniMax TTS配置
MINIMAX_GROUP_ID = ""
MINIMAX_API_KEY = ""
MINIMAX_TTS_URL = f"https://api.minimax.chat/v1/t2a_v2?GroupId={MINIMAX_GROUP_ID}"
VOICE_DIR = 'data/voices'# 语音文件目录
MINIMAX_VOICE_SETTINGS = {
	"model": "speech-01-hd",
	"timber_weights": [
		{
			"voice_id": "Serene_Woman",
			"weight": 26
		},
		{
			"voice_id": "female-chengshu-jingpin",
			"weight": 13
		},
		{
			"voice_id": "Santa_Claus",
			"weight": 13
		}
	],
	"voice_setting": {
		"voice_id": "",
		"speed": 0.88,
		"pitch": 0,
		"vol": 1,
		"emotion": "happy",
		"latex_read": True
	},
	"audio_setting": {
		"sample_rate": 32000,
		"bitrate": 128000,
		"format": "wav"
	},
	"language_boost": "en"
}

# 自动消息配置
AUTO_MESSAGE = '请你模拟系统设置的角色，在微信上找对方发消息想知道对方在做什么'
MIN_COUNTDOWN_HOURS = 1# 最小倒计时时间（小时）
MAX_COUNTDOWN_HOURS = 3# 最大倒计时时间（小时）

# 消息发送时间限制
QUIET_TIME_START = '00:00'# 安静时间开始
QUIET_TIME_END = '24:00'# 安静时间结束
