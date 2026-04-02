"""
status命令实现
标记任务状态（done/pending/todo）
"""

import argparse
from datetime import datetime, date
from typing import Any

from data.models import Timestamp
from data.storage import Storage
from config import Config


def status_command(args: argparse.Namespace, storage: Storage, config: Config) -> int:
    """
    执行status命令（done/pending/todo）

    Args:
        args: 命令行参数
        storage: 存储管理器
        config: 配置管理器

    Returns:
        退出代码 (0表示成功，非0表示失败)
    """
    try:
        # 从命令名获取状态类型
        status_type = args.command  # 'done', 'pending', 或 'todo'

        # 检查任务是否存在
        task = storage.get_task(args.task_id)
        if not task:
            print(f"错误: 任务ID '{args.task_id}' 不存在")
            return 1

        # 验证颜色编码格式
        from utils.color_code import validate_color_code

        if not validate_color_code(args.task_id):
            print(f"错误: 任务ID '{args.task_id}' 格式无效")
            print("任务ID必须是6位大写字母(A-F)和数字(0-9)的组合")
            return 1

        # 解析日期字符串
        try:
            start_date = date.fromisoformat(args.begin)
            end_date = date.fromisoformat(args.end)
        except ValueError as e:
            print(f"错误: 日期格式无效 - {str(e)}")
            print("请使用格式: YYYY-MM-DD")
            return 1

        # 验证日期顺序
        if start_date > end_date:
            print("错误: 开始日期不能晚于结束日期")
            return 1

        # 检查日期范围是否合理（不超过30天）
        date_range = (end_date - start_date).days
        if date_range > 30:
            print(f"警告: 日期范围较大 ({date_range + 1} 天)")
            confirm = input("确认要标记这么多天的状态吗？(y/N): ")
            if confirm.lower() != "y":
                print("操作已取消")
                return 0

        # 获取当前时间
        current_time = datetime.now()

        # 创建时间戳对象
        timestamp = Timestamp(
            task_id=args.task_id,
            type=status_type,
            start=start_date,
            end=end_date,
            created_at=current_time,
        )

        # 保存时间戳
        storage.save_timestamp(timestamp)

        # 输出成功信息
        status_display = {"done": "已完成", "pending": "进行中", "todo": "待办"}

        print(f"任务状态标记成功!")
        print(f"任务ID: {args.task_id}")
        print(f"任务名称: {task.name}")
        print(f"状态: {status_display.get(status_type, status_type)}")
        print(f"日期范围: {start_date} 至 {end_date}")
        print(f"标记时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 如果是单日标记，显示详细信息
        if start_date == end_date:
            print(
                f"已成功标记 {start_date} 的状态为 {status_display.get(status_type, status_type)}"
            )
        else:
            print(
                f"已成功标记 {start_date} 至 {end_date} 共{date_range + 1}天的状态为 {status_display.get(status_type, status_type)}"
            )

        return 0

    except Exception as e:
        print(f"标记任务状态时发生错误: {str(e)}")
        return 1


def validate_status_args(args: argparse.Namespace) -> bool:
    """
    验证status命令的参数

    Args:
        args: 命令行参数

    Returns:
        参数是否有效
    """
    # 检查任务ID
    if not args.task_id:
        print("错误: 必须提供任务ID")
        return False

    # 检查开始日期
    if not args.begin:
        print("错误: 必须提供开始日期 (--begin)")
        return False

    # 检查结束日期
    if not args.end:
        print("错误: 必须提供结束日期 (--end)")
        return False

    return True


def get_task_status(task_id: str, target_date: date, storage: Storage) -> str:
    """
    获取任务在指定日期的状态

    Args:
        task_id: 任务ID
        target_date: 目标日期
        storage: 存储管理器

    Returns:
        状态字符串: 'done', 'pending', 'todo'
    """
    # 获取任务的所有时间戳
    timestamps = storage.get_timestamps_by_task(task_id)

    # 筛选包含目标日期的时间戳
    relevant_timestamps = []
    for ts in timestamps:
        if ts.start <= target_date <= ts.end:
            relevant_timestamps.append(ts)

    # 如果没有相关时间戳，返回'todo'
    if not relevant_timestamps:
        return "todo"

    # 按创建时间排序，取最新的
    latest_timestamp = max(relevant_timestamps, key=lambda ts: ts.created_at)

    return latest_timestamp.type
