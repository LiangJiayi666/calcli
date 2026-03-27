"""
view命令实现
查看任务
"""

import argparse
from datetime import date
from typing import Any

from ..data.storage import Storage
from ..config import Config
from ..core.date_utils import parse_date
from ..core.task_logic import get_tasks_for_date_range, update_recent_dates
from ..utils.output import generate_view_output, print_with_temp_file


def view_command(args: argparse.Namespace, storage: Storage, config: Config) -> int:
    """
    执行view命令

    Args:
        args: 命令行参数
        storage: 存储管理器
        config: 配置管理器

    Returns:
        退出代码 (0表示成功，非0表示失败)
    """
    try:
        # 验证筛选类型
        if not config.validate_view_filter(args.filter):
            print(f"错误: 无效的筛选类型 '{args.filter}'")
            print(f"支持的筛选类型: {', '.join(config.get_view_filters())}")
            return 1

        # 解析日期字符串
        try:
            start_date = parse_date(args.start_date)
            end_date = parse_date(args.end_date)
        except ValueError as e:
            print(f"错误: 日期格式无效 - {str(e)}")
            print("请使用格式: YYYY-MM-DD")
            return 1

        # 验证日期顺序
        if start_date > end_date:
            print("错误: 开始日期不能晚于结束日期")
            return 1

        # 检查日期范围是否合理（不超过90天）
        date_range_days = (end_date - start_date).days
        if date_range_days > 90:
            print(f"警告: 日期范围较大 ({date_range_days + 1} 天)")
            confirm = input("确认要查看这么多天的任务吗？(y/N): ")
            if confirm.lower() != "y":
                print("操作已取消")
                return 0

        # 获取所有任务
        tasks = storage.get_all_tasks()

        if not tasks:
            print("没有找到任何任务")
            print("使用 'calcli create --help' 查看如何创建任务")
            return 0

        # 获取日期范围内的任务
        date_tasks = get_tasks_for_date_range(tasks, start_date, end_date, storage)

        # 更新任务的最近日期
        _update_tasks_recent_dates(tasks, date_tasks, storage)

        # 生成输出
        output_text = generate_view_output(
            date_tasks, start_date, end_date, args.filter
        )

        # 打印输出并保存到临时文件
        print_with_temp_file(output_text, config)

        return 0

    except Exception as e:
        print(f"查看任务时发生错误: {str(e)}")
        return 1


def _update_tasks_recent_dates(tasks: list, date_tasks: dict, storage: Storage) -> None:
    """
    更新任务的最近日期

    Args:
        tasks: 任务列表
        date_tasks: 按日期分组的任务字典
        storage: 存储管理器
    """
    updated_tasks = []

    for task in tasks:
        # 找到任务出现的最大日期
        max_date = None
        for d, task_infos in date_tasks.items():
            for task_info in task_infos:
                if task_info["task"].id == task.id:
                    if max_date is None or d > max_date:
                        max_date = d

        # 如果找到了出现日期，更新任务的最近日期
        if max_date:
            updated_task = update_recent_dates(task, max_date)
            if updated_task != task:
                updated_tasks.append(updated_task)

    # 保存更新后的任务
    for task in updated_tasks:
        storage.save_task(task)


def validate_view_args(args: argparse.Namespace) -> bool:
    """
    验证view命令的参数

    Args:
        args: 命令行参数

    Returns:
        参数是否有效
    """
    # 检查开始日期
    if not args.start_date:
        print("错误: 必须提供开始日期")
        return False

    # 检查结束日期
    if not args.end_date:
        print("错误: 必须提供结束日期")
        return False

    return True
