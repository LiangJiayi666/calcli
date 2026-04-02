"""
数据模型定义
包含Task和Timestamp类
"""

from datetime import datetime, date
from typing import Optional
from dataclasses import dataclass, field
import json


@dataclass
class Task:
    """任务模型"""

    id: str  # 6位颜色编码，如"A1B2C3"
    name: str  # 任务名称
    description: str  # 任务描述
    first_start: datetime  # 首次任务开始时间（含具体时间）
    first_end: datetime  # 首次任务结束时间（含具体时间）
    recent_start: datetime  # 最近一次任务开始时间（含具体时间）
    recent_end: datetime  # 最近一次任务结束时间（含具体时间）
    repeat_type: str  # "daily", "weekly", "monthly", "yearly"
    repeat_value: int  # x值，正整数
    expiration_time: datetime  # 消逝时间，默认2121-02-01 21:21:00
    created_at: datetime  # 创建时间
    updated_at: datetime  # 更新时间

    def to_dict(self) -> dict:
        """转换为字典格式，用于JSON序列化"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "first_start": self.first_start.isoformat(),
            "first_end": self.first_end.isoformat(),
            "recent_start": self.recent_start.isoformat(),
            "recent_end": self.recent_end.isoformat(),
            "repeat_type": self.repeat_type,
            "repeat_value": self.repeat_value,
            "expiration_time": self.expiration_time.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典创建Task实例"""
        # 处理旧数据：如果没有expiration_time字段，使用默认值
        if "expiration_time" not in data:
            from config import Config

            expiration_time = datetime.fromisoformat(Config.DEFAULT_EXPIRATION_TIME)
        else:
            expiration_time = datetime.fromisoformat(data["expiration_time"])

        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            first_start=datetime.fromisoformat(data["first_start"]),
            first_end=datetime.fromisoformat(data["first_end"]),
            recent_start=datetime.fromisoformat(data["recent_start"]),
            recent_end=datetime.fromisoformat(data["recent_end"]),
            repeat_type=data["repeat_type"],
            repeat_value=data["repeat_value"],
            expiration_time=expiration_time,
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )


@dataclass
class Timestamp:
    """时间戳模型"""

    task_id: str  # 关联的任务ID
    type: str  # "done", "pending", "todo"
    start: date  # 开始日期（只包含日期）
    end: date  # 结束日期（只包含日期）
    created_at: datetime  # 创建时间

    def to_dict(self) -> dict:
        """转换为字典格式，用于JSON序列化"""
        return {
            "task_id": self.task_id,
            "type": self.type,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Timestamp":
        """从字典创建Timestamp实例"""
        return cls(
            task_id=data["task_id"],
            type=data["type"],
            start=date.fromisoformat(data["start"]),
            end=date.fromisoformat(data["end"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
