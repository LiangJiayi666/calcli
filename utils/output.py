"""
格式化输出工具
"""

from datetime import date, datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..core.date_utils import get_weekday_name_chinese


def format_task_display(task_info: Dict[str, Any]) -> str:
    """
    格式化单个任务的显示字符串

    Args:
        task_info: 任务信息字典

    Returns:
        格式化后的字符串
    """
    task = task_info["task"]
    status = task_info["status"]

    # 状态显示映射
    status_display = {"done": "[done]", "pending": "[pending]", "todo": "[todo]"}

    status_str = status_display.get(status, f"[{status}]")

    # 构建显示字符串
    display = f"  {status_str} {task.name} {task.id} {task.description}"

    return display


def format_date_header(d: date, task_count: int) -> str:
    """
    格式化日期标题

    Args:
        d: 日期
        task_count: 该日期的任务数量

    Returns:
        格式化后的日期标题
    """
    weekday = get_weekday_name_chinese(d)
    date_str = d.strftime("%Y-%m-%d")

    return f"{date_str} ({weekday}) - {task_count} 个任务"


def generate_view_output(
    date_tasks: Dict[date, List[Dict[str, Any]]],
    start_date: date,
    end_date: date,
    filter_type: str = "all",
) -> str:
    """
    生成查看命令的输出字符串

    Args:
        date_tasks: 按日期分组的任务字典
        start_date: 开始日期
        end_date: 结束日期
        filter_type: 筛选类型 ('all', 'todo', 'todopending')

    Returns:
        格式化后的输出字符串
    """
    output_lines = []

    # 添加标题分隔线
    separator = "=" * 80
    output_lines.append(separator)
    output_lines.append("")

    # 处理每个日期
    current_date = start_date
    while current_date <= end_date:
        tasks = date_tasks.get(current_date, [])

        # 根据筛选类型过滤任务
        if filter_type == "todo":
            tasks = [t for t in tasks if t["status"] == "todo"]
        elif filter_type == "todopending":
            tasks = [t for t in tasks if t["status"] in ["todo", "pending"]]

        # 如果该日期有任务，添加到输出
        if tasks:
            # 添加日期标题
            date_header = format_date_header(current_date, len(tasks))
            output_lines.append(date_header)
            output_lines.append("-" * 40)

            # 添加任务列表
            for i, task_info in enumerate(tasks, 1):
                task_display = format_task_display(task_info)
                output_lines.append(f"  {i}. {task_display}")
                output_lines.append("")

            output_lines.append("")

        current_date = _add_days(current_date, 1)

    # 添加结束分隔线
    output_lines.append(separator)

    return "\n".join(output_lines)


def save_to_temp_file(
    output_text: str, config: Any, timestamp: Optional[datetime] = None
) -> Path:
    """
    将输出保存到临时文件

    Args:
        output_text: 输出文本
        config: 配置管理器
        timestamp: 时间戳（默认为当前时间）

    Returns:
        临时文件路径
    """
    if timestamp is None:
        timestamp = datetime.now()

    # 生成文件名
    date_str = timestamp.strftime("%Y%m%d")
    time_str = timestamp.strftime("%H%M%S")

    # 获取临时文件路径
    temp_file_path = config.get_temp_file_path(date_str, time_str)

    # 保存到文件
    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(output_text)

    return temp_file_path


def print_with_temp_file(output_text: str, config: Any) -> None:
    """
    打印输出并保存到临时文件

    Args:
        output_text: 输出文本
        config: 配置管理器
    """
    # 打印到控制台
    print(output_text)

    # 保存到临时文件
    temp_file_path = save_to_temp_file(output_text, config)

    print(f"\n输出已保存到临时文件: {temp_file_path}")


def _add_days(d: date, days: int) -> date:
    """添加天数（简化版本，避免导入问题）"""
    from datetime import timedelta

    return d + timedelta(days=days)


def format_task_summary(task: Any) -> str:
    """
    格式化任务摘要信息

    Args:
        task: 任务对象

    Returns:
        格式化后的任务摘要
    """
    summary = []
    summary.append(f"任务ID: {task.id}")
    summary.append(f"任务名称: {task.name}")
    summary.append(f"任务描述: {task.description}")
    summary.append(f"开始时间: {task.first_start.strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"结束时间: {task.first_end.strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"重复类型: {task.repeat_type}")
    summary.append(
        f"重复间隔: 每{task.repeat_value}个{'天' if task.repeat_type == 'daily' else '周' if task.repeat_type == 'weekly' else '月' if task.repeat_type == 'monthly' else '年'}"
    )
    summary.append(f"创建时间: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"更新时间: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(summary)
