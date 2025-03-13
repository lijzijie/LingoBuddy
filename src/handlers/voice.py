"""
语音处理模块
负责处理语音相关功能，包括:
- 语音请求识别
- TTS语音生成
- 语音文件管理
- 清理临时文件
"""

import os
import logging
import requests
import json
from datetime import datetime
from typing import Optional
# from pydub import AudioSegment

logger = logging.getLogger(__name__)

class VoiceHandler:
    def __init__(self, root_dir, minimax_settings):
        self.root_dir = root_dir
        self.settings = minimax_settings
        self.voice_dir = os.path.join(root_dir, "data", "voices")

        # 确保语音目录存在
        os.makedirs(self.voice_dir, exist_ok=True)

    def is_voice_request(self, text: str) -> bool:
        """
        判断是否为语音请求
        支持的场景：
        1. 直接请求语音
        2. 要求朗读/发音
        3. 英语学习场景
        4. 发音纠正请求
        """
        voice_keywords = [
            # 中文语音请求关键词
            "语音", "朗读", "读一下", "念一下", "说一下",
            "发音", "读给我听", "怎么读", "怎么说",

            # 英语学习相关关键词
            "pronunciation", "speak", "read", "say",
            "how to pronounce", "how to say",

            # 发音练习相关
            "读音", "跟读", "复述", "重复",
            "repeat after me", "listen and repeat",

            # 语音输出请求
            "用语音回答", "语音回复", "voice message",
            "speak out", "say it out loud"
        ]

        # 转换为小写进行匹配
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in voice_keywords)

    # def convert_to_amr(self, input_file: str) -> Optional[str]:
    #     """将音频文件转换为AMR格式"""
    #     try:
    #         output_file = input_file.rsplit('.', 1)[0] + '.amr'

    #         # 加载音频文件
    #         audio = AudioSegment.from_file(input_file)

    #         # 将采样率转换为 8000Hz（AMR 编码器要求）
    #         audio = audio.set_frame_rate(8000)

    #         # 导出为 AMR 格式
    #         audio.export(output_file, format="amr", codec="libopencore_amrnb")
    #         logger.info(f"音频转换成功: {output_file}")

    #         # 删除原始文件
    #         os.remove(input_file)

    #         return output_file
    #     except Exception as e:
    #         logger.error(f"音频转换失败: {str(e)}")
    #         return None

    def generate_voice(self, text: str, language: str = "zh") -> Optional[str]:
        """调用MiniMax API生成语音"""
        try:
            # 确保语音目录存在
            if not os.path.exists(self.voice_dir):
                os.makedirs(self.voice_dir)

            # 生成唯一的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            voice_path = os.path.join(self.voice_dir, f"voice_{timestamp}.wav")

            # 准备请求数据
            payload = {
                **self.settings["MINIMAX_VOICE_SETTINGS"],
                "text": text,
                "language_boost": "en" if language == "en" else "zh"
            }

            headers = {
                'Authorization': f'Bearer {self.settings["MINIMAX_API_KEY"]}',
                'Content-Type': 'application/json'
            }

            # 发送请求
            response = requests.post(
                self.settings["MINIMAX_TTS_URL"],
                headers=headers,
                data=json.dumps(payload)
            )

            # 解析响应
            parsed_json = response.json()

            # 添加详细的调试信息
            if 'extra_info' in parsed_json:
                extra_info = parsed_json['extra_info']
                logger.info(f"音频信息: "
                          f"时长={extra_info.get('audio_length', 0)}ms, "
                          f"采样率={extra_info.get('audio_sample_rate', 0)}Hz, "
                          f"大小={extra_info.get('audio_size', 0)}字节, "
                          f"比特率={extra_info.get('bitrate', 0)}bps")
                logger.info(f"音频格式: {extra_info.get('audio_format', 'unknown')}, "
                          f"声道数: {extra_info.get('audio_channel', 1)}")
                logger.info(f"非法字符占比: {extra_info.get('invisible_character_ratio', 0):.2%}, "
                          f"计费字符数: {extra_info.get('usage_characters', 0)}")

            if parsed_json.get('base_resp', {}).get('status_code') == 0:
                audio_value = bytes.fromhex(parsed_json['data']['audio'])
                with open(voice_path, 'wb') as f:
                    f.write(audio_value)

                # 转换为AMR格式 AMR格式也无法发送语音
                # amr_path = self.convert_to_amr(voice_path)
                # if amr_path:
                #     logger.info(f"语音生成并转换成功: {amr_path}")
                #     return amr_path
                # else:
                #     logger.error("AMR转换失败")
                #     return None

                logger.info(f"语音生成成功: {voice_path}")
                return voice_path
            else:
                error_msg = parsed_json.get('base_resp', {}).get('status_msg', '未知错误')
                logger.error(f"语音生成失败: {error_msg}")
                return None

        except Exception as e:
            logger.error(f"语音生成失败: {str(e)}")
            return None

    def cleanup_voice_dir(self):
        """清理语音目录中的旧文件"""
        try:
            if os.path.exists(self.voice_dir):
                for file in os.listdir(self.voice_dir):
                    file_path = os.path.join(self.voice_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            logger.info(f"清理旧语音文件: {file_path}")
                    except Exception as e:
                        logger.error(f"清理语音文件失败 {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"清理语音目录失败: {str(e)}")