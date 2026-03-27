"""
配置管理
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any


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

    # 环境配置
    ENVIRONMENTS = {
        "production": {
            "name": "production",
            "data_dir": os.path.expanduser("~/.calcli"),
            "description": "生产环境",
            "is_production": True,
            "test_prefix": None,
        },
        "test": {
            "name": "test",
            "data_dir": os.path.expanduser("~/.calcli_test"),
            "description": "测试环境",
            "is_production": False,
            "test_prefix": "[TEST]",
        },
        "development": {
            "name": "development",
            "data_dir": os.path.expanduser("~/.calcli_dev"),
            "description": "开发环境",
            "is_production": False,
            "test_prefix": "[DEV]",
        },
    }

    def __init__(self, env: Optional[str] = None, data_dir: Optional[str] = None):
        """
        初始化配置

        Args:
            env: 环境名称 (production/test/development)
            data_dir: 数据目录路径 (覆盖环境配置)
        """
        self.env_name = self._detect_environment(env)
        self.env_config = self.ENVIRONMENTS[self.env_name]

        # 如果指定了data_dir，则覆盖环境配置
        if data_dir:
            self.data_dir = Path(data_dir)
            # 更新环境配置中的data_dir
            self.env_config = self.env_config.copy()
            self.env_config["data_dir"] = str(self.data_dir)
        else:
            self.data_dir = Path(self.env_config["data_dir"])

        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 初始化环境日志目录
        self._init_environment_logs()

    def _detect_environment(self, env: Optional[str] = None) -> str:
        """
        检测当前环境

        优先级:
        1. 显式传入的env参数
        2. 命令行参数 --env
        3. 环境变量 CALCLI_ENV
        4. 默认生产环境

        Args:
            env: 环境名称

        Returns:
            环境名称
        """
        # 1. 显式参数
        if env:
            if env not in self.ENVIRONMENTS:
                raise ValueError(
                    f"未知环境: {env}，可用环境: {list(self.ENVIRONMENTS.keys())}"
                )
            return env

        # 2. 命令行参数
        if "--env" in sys.argv:
            try:
                env_index = sys.argv.index("--env")
                if env_index + 1 < len(sys.argv):
                    cmd_env = sys.argv[env_index + 1]
                    if cmd_env in self.ENVIRONMENTS:
                        return cmd_env
            except (ValueError, IndexError):
                pass

        # 3. 环境变量
        env_var = os.environ.get("CALCLI_ENV")
        if env_var and env_var in self.ENVIRONMENTS:
            return env_var

        # 4. 默认生产环境
        return "production"

    def _init_environment_logs(self):
        """初始化环境日志目录"""
        logs_dir = self.data_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

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
