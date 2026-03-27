"""
JSON存储管理
负责任务的持久化存储
"""

import json
import os
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from .models import Task, Timestamp


class Storage:
    """存储管理器"""

    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化存储管理器

        Args:
            data_dir: 数据目录路径，默认为 ~/.calcli/
        """
        if data_dir is None:
            data_dir = os.path.expanduser("~/.calcli")

        self.data_dir = Path(data_dir)
        self.tasks_file = self.data_dir / "tasks.json"
        self.timestamps_file = self.data_dir / "timestamps.json"

        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 初始化文件
        self._init_files()

    def _init_files(self):
        """初始化存储文件"""
        if not self.tasks_file.exists():
            self._write_json(self.tasks_file, {"tasks": []})

        if not self.timestamps_file.exists():
            self._write_json(self.timestamps_file, {"timestamps": []})

    def _read_json(self, filepath: Path) -> Dict[str, Any]:
        """读取JSON文件"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_json(self, filepath: Path, data: Dict[str, Any]):
        """写入JSON文件"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # 任务管理方法
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        data = self._read_json(self.tasks_file)
        tasks_data = data.get("tasks", [])
        return [Task.from_dict(task_data) for task_data in tasks_data]

    def get_task(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def save_task(self, task: Task):
        """保存任务（创建或更新）"""
        tasks = self.get_all_tasks()

        # 查找是否已存在
        existing_index = -1
        for i, t in enumerate(tasks):
            if t.id == task.id:
                existing_index = i
                break

        if existing_index >= 0:
            # 更新现有任务
            tasks[existing_index] = task
        else:
            # 添加新任务
            tasks.append(task)

        # 保存到文件
        self._write_json(self.tasks_file, {"tasks": [t.to_dict() for t in tasks]})



    # 时间戳管理方法
    def get_all_timestamps(self) -> List[Timestamp]:
        """获取所有时间戳"""
        data = self._read_json(self.timestamps_file)
        timestamps_data = data.get("timestamps", [])
        return [Timestamp.from_dict(ts_data) for ts_data in timestamps_data]

    def get_timestamps_by_task(self, task_id: str) -> List[Timestamp]:
        """获取指定任务的所有时间戳"""
        all_timestamps = self.get_all_timestamps()
        return [ts for ts in all_timestamps if ts.task_id == task_id]


        for ts in all_timestamps:
            # 检查时间戳是否与日期范围有重叠
            if not (ts.end < start_date or ts.start > end_date):
                result.append(ts)

        return result

    def save_timestamp(self, timestamp: Timestamp):
        """保存时间戳"""
        timestamps = self.get_all_timestamps()
        timestamps.append(timestamp)

        # 保存到文件
        self._write_json(
            self.timestamps_file, {"timestamps": [ts.to_dict() for ts in timestamps]}
        )


    def get_task_ids(self) -> List[str]:
        """获取所有任务ID"""
        tasks = self.get_all_tasks()
        return [task.id for task in tasks]

