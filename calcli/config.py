"""
配置管理
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """配置管理器"""

    # 默认配置
    DEFAULT_DATA_DIR = os.path.expanduser("~/.calcli")
    DEFAULT_TASKS_FILE = "tasks.json"
    DEFAULT_TIMESTAMPS_FILE = "timestamps.json"

    # 临时文件命名格式
    TEMP_FILE_FORMAT = "view_{date}_{time}.txt"

    # 支持的重复类型
    REPEAT_TYPES = ["daily", "weekly", "monthly", "yearly"]

    # 支持的状态类型
    STATUS_TYPES = ["done", "pending", "todo"]

    # 查看命令的筛选选项
    VIEW_FILTERS = ["all", "todo", "todopending"]

    # 默认消逝时间
    DEFAULT_EXPIRATION_TIME = "2121-02-01T21:21:00"

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化配置

        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir) if data_dir else Path(self.DEFAULT_DATA_DIR)

        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @property
    def tasks_file(self) -> Path:
        """任务文件路径"""
        return self.data_dir / self.DEFAULT_TASKS_FILE

    @property
    def timestamps_file(self) -> Path:
        """时间戳文件路径"""
        return self.data_dir / self.DEFAULT_TIMESTAMPS_FILE

    def get_temp_file_path(self, date_str: str, time_str: str) -> Path:
        """
        获取临时文件路径

        Args:
            date_str: 日期字符串 (YYYYMMDD)
            time_str: 时间字符串 (HHMMSS)

        Returns:
            临时文件路径
        """
        filename = self.TEMP_FILE_FORMAT.format(date=date_str, time=time_str)
        return self.data_dir / filename

    def validate_repeat_type(self, repeat_type: str) -> bool:
        """
        验证重复类型是否有效

        Args:
            repeat_type: 重复类型

        Returns:
            是否有效
        """
        return repeat_type.lower() in self.REPEAT_TYPES

    def validate_status_type(self, status_type: str) -> bool:
        """
        验证状态类型是否有效

        Args:
            status_type: 状态类型

        Returns:
            是否有效
        """
        return status_type.lower() in self.STATUS_TYPES

    def validate_view_filter(self, filter_type: str) -> bool:
        """
        验证查看筛选器是否有效

        Args:
            filter_type: 筛选器类型

        Returns:
            是否有效
        """
        return filter_type.lower() in self.VIEW_FILTERS

    @classmethod
    def get_repeat_types(cls) -> list:
        """获取支持的重复类型列表"""
        return cls.REPEAT_TYPES.copy()

    @classmethod
    def get_status_types(cls) -> list:
        """获取支持的状态类型列表"""
        return cls.STATUS_TYPES.copy()

    @classmethod
    def get_view_filters(cls) -> list:
        """获取支持的查看筛选器列表"""
        return cls.VIEW_FILTERS.copy()
