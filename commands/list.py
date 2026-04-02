"""
list命令实现
列出任务及其时间戳
"""

import argparse
from datetime import datetime
from typing import Any

from data.storage import Storage
from config import Config


def list_command(args: argparse.Namespace, storage: Storage, config: Config) -> int:
    """
    执行list命令

    Args:
        args: 命令行参数
        storage: 存储管理器
        config: 配置管理器

    Returns:
        退出代码 (0表示成功，非0表示失败)
    """
    try:
        current_time = datetime.now()

        # 获取所有任务
        all_tasks = storage.get_all_tasks()

        # 筛选未到达expiration的任务
        active_tasks = [
            task for task in all_tasks if task.expiration_time > current_time
        ]

        if not active_tasks:
            print("没有未到达消逝时间的任务")
            return 0

        # 显示所有未到达expiration的任务
        print(f"=== 未到达消逝时间的任务列表 (共{len(active_tasks)}个) ===")
        print()

        for i, task in enumerate(active_tasks, 1):
            print(f"{i}. {task.id} - {task.name}")
            print(f"   描述: {task.description}")
            print(f"   开始时间: {task.first_start.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   结束时间: {task.first_end.strftime('%Y-%m-%d %H:%M:%S')}")
            print(
                f"   重复类型: {task.repeat_type} (每{task.repeat_value}个{get_repeat_unit(task.repeat_type)})"
            )
            print(f"   消逝时间: {task.expiration_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   创建时间: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   更新时间: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

            # 获取任务的时间戳
            timestamps = storage.get_timestamps_by_task(task.id)
            if timestamps:
                print(f"   时间戳 ({len(timestamps)}个):")
                for ts in timestamps:
                    status_text = {
                        "done": "完成",
                        "pending": "进行中",
                        "todo": "待办",
                    }.get(ts.type, ts.type)
                    print(
                        f"     - {status_text}: {ts.start.isoformat()} 到 {ts.end.isoformat()}"
                    )
            else:
                print("   时间戳: 无")

            print()

        return 0

    except Exception as e:
        print(f"列出任务时发生错误: {str(e)}")
        return 1


def get_repeat_unit(repeat_type: str) -> str:
    """获取重复类型的单位"""
    units = {"daily": "天", "weekly": "周", "monthly": "月", "yearly": "年"}
    return units.get(repeat_type, repeat_type)


def validate_list_args(args: argparse.Namespace) -> bool:
    """
    验证list命令的参数

    Args:
        args: 命令行参数

    Returns:
        参数是否有效
    """
    # list命令不需要强制参数，可以不带参数运行
    return True
