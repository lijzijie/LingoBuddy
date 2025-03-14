"""
数据库读取工具
用于读取和分析聊天历史数据
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from database import ChatMessage, Base

logger = logging.getLogger(__name__)

class ChatHistoryReader:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # 使用默认数据库路径
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(project_root, 'data', 'database', 'chat_history.db')

        if not os.path.exists(db_path):
            raise FileNotFoundError(f"数据库文件不存在: {db_path}")

        self.engine = create_engine(f'sqlite:///{db_path}')
        self.Session = sessionmaker(bind=self.engine)

    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """获取最近的聊天记录"""
        try:
            session = self.Session()
            messages = session.query(ChatMessage)\
                .order_by(desc(ChatMessage.created_at))\
                .limit(limit)\
                .all()

            return [{
                'id': msg.id,
                'sender_name': msg.sender_name,
                'message': msg.message,
                'reply': msg.reply,
                'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for msg in messages]
        except Exception as e:
            logger.error(f"获取最近消息失败: {str(e)}")
            return []
        finally:
            session.close()

    def get_user_history(self, sender_id: str) -> List[Dict]:
        """获取特定用户的聊天历史"""
        try:
            session = self.Session()
            messages = session.query(ChatMessage)\
                .filter(ChatMessage.sender_id == sender_id)\
                .order_by(desc(ChatMessage.created_at))\
                .all()

            return [{
                'message': msg.message,
                'reply': msg.reply,
                'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for msg in messages]
        except Exception as e:
            logger.error(f"获取用户历史失败: {str(e)}")
            return []
        finally:
            session.close()

    def get_daily_stats(self, days: int = 7) -> List[Dict]:
        """获取每日统计数据"""
        try:
            session = self.Session()
            start_date = datetime.now() - timedelta(days=days)

            daily_counts = session.query(
                func.date(ChatMessage.created_at).label('date'),
                func.count().label('message_count')
            ).filter(
                ChatMessage.created_at >= start_date
            ).group_by(
                func.date(ChatMessage.created_at)
            ).all()

            return [{
                'date': str(date),
                'message_count': count
            } for date, count in daily_counts]
        except Exception as e:
            logger.error(f"获取每日统计失败: {str(e)}")
            return []
        finally:
            session.close()

    def get_active_users(self, limit: int = 10) -> List[Dict]:
        """获取最活跃的用户"""
        try:
            session = self.Session()
            active_users = session.query(
                ChatMessage.sender_id,
                ChatMessage.sender_name,
                func.count().label('message_count')
            ).group_by(
                ChatMessage.sender_id
            ).order_by(
                desc('message_count')
            ).limit(limit).all()

            return [{
                'sender_id': user[0],
                'sender_name': user[1],
                'message_count': user[2]
            } for user in active_users]
        except Exception as e:
            logger.error(f"获取活跃用户失败: {str(e)}")
            return []
        finally:
            session.close()

    def search_messages(self, keyword: str) -> List[Dict]:
        """搜索包含关键词的消息"""
        try:
            session = self.Session()
            messages = session.query(ChatMessage)\
                .filter(ChatMessage.message.like(f'%{keyword}%'))\
                .order_by(desc(ChatMessage.created_at))\
                .all()

            return [{
                'sender_name': msg.sender_name,
                'message': msg.message,
                'reply': msg.reply,
                'created_at': msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for msg in messages]
        except Exception as e:
            logger.error(f"搜索消息失败: {str(e)}")
            return []
        finally:
            session.close()

# 使用示例
def main():
    try:
        # 创建读取器实例
        reader = ChatHistoryReader()

        # 1. 获取最近的消息
        print("\n最近的消息:")
        recent_messages = reader.get_recent_messages(5)
        for msg in recent_messages:
            print(f"[{msg['created_at']}] {msg['sender_name']}: {msg['message']}")
            print(f"回复: {msg['reply']}\n")

        # 2. 获取每日统计
        print("\n每日统计:")
        daily_stats = reader.get_daily_stats()
        for stat in daily_stats:
            print(f"日期: {stat['date']}, 消息数: {stat['message_count']}")

        # 3. 获取活跃用户
        print("\n活跃用户:")
        active_users = reader.get_active_users()
        for user in active_users:
            print(f"用户: {user['sender_name']}, 消息数: {user['message_count']}")

        # 4. 搜索特定关键词
        keyword = "你好"
        print(f"\n搜索包含 '{keyword}' 的消息:")
        search_results = reader.search_messages(keyword)
        for msg in search_results:
            print(f"[{msg['created_at']}] {msg['sender_name']}: {msg['message']}")
            print(f"回复: {msg['reply']}\n")

    except Exception as e:
        logger.error(f"读取数据库失败: {str(e)}")

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()