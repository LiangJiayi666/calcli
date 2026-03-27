"""
update命令实现
更新现有任务
"""

import argparse
from datetime import datetime
from typing import Any

from ..data.models import Task
from ..data.storage import Storage
from ..config import Config


def update_command(args: argparse.Namespace, storage: Storage, config: Config) -> int:
    """
    执行update命令

    Args:
        args: 命令行参数
        storage: 存储管理器
        config: 配置管理器

    Returns:
        退出代码 (0表示成功，非0表示失败)
    """
    try:
        # 检查任务是否存在
        task = storage.get_task(args.task_id)
        if not task:
            print(f"错误: 任务ID '{args.task_id}' 不存在")
            return 1

        # 验证颜色编码格式
        from ..utils.color_code import validate_color_code

        if not validate_color_code(args.task_id):
            print(f"错误: 任务ID '{args.task_id}' 格式无效")
            print("任务ID必须是6位大写字母(A-F)和数字(0-9)的组合")
            return 1

        # 记录是否有更新
        updated = False

        # 更新任务名称
        if args.name is not None:
            if args.name.strip():
                task.name = args.name.strip()
                updated = True
            else:
                print("警告: 任务名称不能为空，已忽略")

        # 更新任务描述
        if args.description is not None:
            task.description = args.description
            updated = True

        # 更新开始时间
        if args.begin is not None:
            try:
                begin_time = datetime.fromisoformat(args.begin)
                task.first_start = begin_time
                task.recent_start = begin_time  # 同时更新最近开始时间
                updated = True
            except ValueError as e:
                print(f"错误: 开始时间格式无效 - {str(e)}")
                print("请使用格式: YYYY-MM-DD HH:MM:SS")
                return 1

        # 更新结束时间
        if args.end is not None:
            try:
                end_time = datetime.fromisoformat(args.end)
                task.first_end = end_time
                task.recent_end = end_time  # 同时更新最近结束时间
                updated = True
            except ValueError as e:
                print(f"错误: 结束时间格式无效 - {str(e)}")
                print("请使用格式: YYYY-MM-DD HH:MM:SS")
                return 1

        # 验证时间顺序
        # 如果同时更新了开始和结束时间
        if args.begin is not None and args.end is not None:
            if task.first_start >= task.first_end:
                print("错误: 开始时间必须早于结束时间")
                return 1
        # 如果只更新开始时间，检查是否比现有的结束时间晚
        elif args.begin is not None:
            if task.first_start >= task.first_end:
                print("错误: 更新后的开始时间不能晚于或等于现有的结束时间")
                return 1
        # 如果只更新结束时间，检查是否比现有的开始时间早
        elif args.end is not None:
            if task.first_start >= task.first_end:
                print("错误: 更新后的结束时间不能早于或等于现有的开始时间")
                return 1

        # 更新重复类型
        if args.repeat is not None:
            if not config.validate_repeat_type(args.repeat):
                print(f"错误: 无效的重复类型 '{args.repeat}'")
                print(f"支持的重复类型: {', '.join(config.get_repeat_types())}")
                return 1
            task.repeat_type = args.repeat
            updated = True

        # 更新重复间隔值
        if args.x is not None:
            if args.x <= 0:
                print(f"错误: 重复间隔值必须为正整数，当前为 {args.x}")
                return 1
            task.repeat_value = args.x
            updated = True

        # 更新消逝时间
        if args.expiration is not None:
            try:
                expiration_time = datetime.fromisoformat(args.expiration)
                task.expiration_time = expiration_time
                updated = True
            except ValueError as e:
                print(f"错误: 消逝时间格式无效 - {str(e)}")
                print("请使用格式: YYYY-MM-DD HH:MM:SS")
                return 1
        # 如果更新了begin或end，且没有更新expiration，检查expiration是否比更新后的end更早
        elif args.begin is not None or args.end is not None:
            # 获取更新后的end时间（如果更新了end就用新的，否则用现有的）
            current_end = task.first_end
            # 如果expiration比更新后的end更早，则对齐到end
            if task.expiration_time < current_end:
                task.expiration_time = current_end
                updated = True

        # 如果没有提供任何更新参数
        if not updated:
            print("警告: 没有提供任何更新参数")
            print("使用 --help 查看可用参数")
            return 0

        # 更新修改时间
        task.updated_at = datetime.now()

        # 保存更新后的任务
        storage.save_task(task)

        # 输出成功信息
        print(f"任务更新成功!")
        print(f"任务ID: {task.id}")
        print(f"任务名称: {task.name}")
        print(f"开始时间: {task.first_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"结束时间: {task.first_end.strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"重复类型: {task.repeat_type} (每{task.repeat_value}个{'天' if task.repeat_type == 'daily' else '周' if task.repeat_type == 'weekly' else '月' if task.repeat_type == 'monthly' else '年'})"
        )
        print(f"更新时间: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

        return 0

    except Exception as e:
        print(f"更新任务时发生错误: {str(e)}")
        return 1


def validate_update_args(args: argparse.Namespace) -> bool:
    """
    验证update命令的参数

    Args:
        args: 命令行参数

    Returns:
        参数是否有效
    """
    # 检查任务ID
    if not args.task_id:
        print("错误: 必须提供任务ID")
        return False

    # 检查是否提供了至少一个更新参数
    update_params = ["name", "description", "begin", "end", "repeat", "x"]
    has_update = any(getattr(args, param) is not None for param in update_params)

    if not has_update:
        print("错误: 必须提供至少一个更新参数")
        print("可用参数: --name, --description, --begin, --end, --repeat, --x")
        return False

    return True
