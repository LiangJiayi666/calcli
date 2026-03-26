"""
create命令实现
创建新任务
"""

import argparse
from datetime import datetime
from typing import Any

from ..data.models import Task
from ..data.storage import Storage
from ..config import Config
from ..utils.color_code import generate_color_code


def create_command(args: argparse.Namespace, storage: Storage, config: Config) -> int:
    """
    执行create命令

    Args:
        args: 命令行参数
        storage: 存储管理器
        config: 配置管理器

    Returns:
        退出代码 (0表示成功，非0表示失败)
    """
    try:
        # 验证重复类型
        if not config.validate_repeat_type(args.repeat):
            print(f"错误: 无效的重复类型 '{args.repeat}'")
            print(f"支持的重复类型: {', '.join(config.get_repeat_types())}")
            return 1

        # 验证重复间隔值
        if args.x <= 0:
            print(f"错误: 重复间隔值必须为正整数，当前为 {args.x}")
            return 1

        # 解析时间字符串
        try:
            begin_time = datetime.fromisoformat(args.begin)
            end_time = datetime.fromisoformat(args.end)
        except ValueError as e:
            print(f"错误: 时间格式无效 - {str(e)}")
            print("请使用格式: YYYY-MM-DD HH:MM:SS")
            return 1

        # 验证时间顺序
        if begin_time >= end_time:
            print("错误: 开始时间必须早于结束时间")
            return 1

        # 解析消逝时间
        try:
            expiration_time = datetime.fromisoformat(args.expiration)
        except ValueError as e:
            print(f"错误: 消逝时间格式无效 - {str(e)}")
            print("请使用格式: YYYY-MM-DD HH:MM:SS")
            return 1

        # 生成唯一的颜色编码
        existing_ids = storage.get_task_ids()
        task_id = generate_color_code(existing_ids)

        # 获取当前时间
        current_time = datetime.now()

        # 创建任务对象
        task = Task(
            id=task_id,
            name=args.name,
            description=args.description,
            first_start=begin_time,
            first_end=end_time,
            recent_start=begin_time,  # 创建时，首次=最近
            recent_end=end_time,  # 创建时，首次=最近
            repeat_type=args.repeat,
            repeat_value=args.x,
            expiration_time=expiration_time,
            created_at=current_time,
            updated_at=current_time,
        )

        # 保存任务
        storage.save_task(task)

        # 输出成功信息
        print(f"任务创建成功!")
        print(f"任务ID: {task_id}")
        print(f"任务名称: {args.name}")
        print(f"开始时间: {begin_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"消逝时间: {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"重复类型: {args.repeat} (每{args.x}个{'天' if args.repeat == 'daily' else '周' if args.repeat == 'weekly' else '月' if args.repeat == 'monthly' else '年'})"
        )
        print(f"创建时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    except Exception as e:
        print(f"创建任务时发生错误: {str(e)}")
        return 1


def validate_create_args(args: argparse.Namespace) -> bool:
    """
    验证create命令的参数

    Args:
        args: 命令行参数

    Returns:
        参数是否有效
    """
    # 检查必需参数
    if not args.name:
        print("错误: 必须提供任务名称 (--name)")
        return False

    if not args.description:
        print("错误: 必须提供任务描述 (--description)")
        return False

    if not args.begin:
        print("错误: 必须提供开始时间 (--begin)")
        return False

    if not args.end:
        print("错误: 必须提供结束时间 (--end)")
        return False

    # 检查重复间隔值
    if args.x <= 0:
        print(f"错误: 重复间隔值必须为正整数，当前为 {args.x}")
        return False

    return True
