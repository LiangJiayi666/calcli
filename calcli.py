#!/usr/bin/env python3
"""
CalCLI 主程序入口
命令行日历任务管理工具
"""

import sys
import argparse
from datetime import datetime

from .config import Config
from .data.storage import Storage
from .utils.color_code import ColorCodeGenerator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="CalCLI - 命令行日历任务管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  calcli create --name "任务名" --description "描述" --begin "2026-03-18 09:00:00" --end "2026-03-18 10:00:00" --repeat weekly --x 1
  calcli update A1B2C3 --name "新名称" --repeat monthly --x 2
  calcli done A1B2C3 --begin "2026-03-25" --end "2026-03-25"
  calcli view "2026-03-25" "2026-03-30" --all
        """,
    )

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新任务")
    create_parser.add_argument("--name", required=True, help="任务名称")
    create_parser.add_argument("--description", required=True, help="任务描述")
    create_parser.add_argument(
        "--begin", required=True, help="开始时间 (YYYY-MM-DD HH:MM:SS)"
    )
    create_parser.add_argument(
        "--end", required=True, help="结束时间 (YYYY-MM-DD HH:MM:SS)"
    )
    create_parser.add_argument(
        "--repeat",
        choices=["daily", "weekly", "monthly", "yearly"],
        default="daily",
        help="重复类型",
    )
    create_parser.add_argument("--x", type=int, default=1, help="重复间隔值")

    # update 命令
    update_parser = subparsers.add_parser("update", help="更新任务")
    update_parser.add_argument("task_id", help="任务ID")
    update_parser.add_argument("--name", help="新任务名称")
    update_parser.add_argument("--description", help="新任务描述")
    update_parser.add_argument("--begin", help="新开始时间 (YYYY-MM-DD HH:MM:SS)")
    update_parser.add_argument("--end", help="新结束时间 (YYYY-MM-DD HH:MM:SS)")
    update_parser.add_argument(
        "--repeat", choices=["daily", "weekly", "monthly", "yearly"], help="新重复类型"
    )
    update_parser.add_argument("--x", type=int, help="新重复间隔值")

    # status 命令 (done/pending/todo)
    for status in ["done", "pending", "todo"]:
        status_parser = subparsers.add_parser(status, help=f"标记任务为{status}")
        status_parser.add_argument("task_id", help="任务ID")
        status_parser.add_argument(
            "--begin", required=True, help="开始日期 (YYYY-MM-DD)"
        )
        status_parser.add_argument("--end", required=True, help="结束日期 (YYYY-MM-DD)")

    # view 命令
    view_parser = subparsers.add_parser("view", help="查看任务")
    view_parser.add_argument("start_date", help="开始日期 (YYYY-MM-DD)")
    view_parser.add_argument("end_date", help="结束日期 (YYYY-MM-DD)")
    view_parser.add_argument(
        "--filter",
        choices=["all", "todo", "todopending"],
        default="all",
        help="筛选显示的任务",
    )

    # 解析参数
    args = parser.parse_args()

    # 如果没有提供命令，显示帮助
    if not args.command:
        parser.print_help()
        return 1

    try:
        # 初始化配置和存储
        config = Config()
        storage = Storage()

        # 根据命令执行相应操作
        if args.command == "create":
            from .commands.create import create_command

            return create_command(args, storage, config)

        elif args.command == "update":
            from .commands.update import update_command

            return update_command(args, storage, config)

        elif args.command in ["done", "pending", "todo"]:
            from .commands.status import status_command

            return status_command(args, storage, config)

        elif args.command == "view":
            from .commands.view import view_command

            return view_command(args, storage, config)

        else:
            print(f"错误: 未知命令 '{args.command}'")
            return 1

    except Exception as e:
        print(f"错误: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
