"""
重复任务计算逻辑
"""

from datetime import datetime, date, timedelta
from typing import List, Tuple, Dict, Any
import calendar

from ..data.models import Task
from .date_utils import add_days, add_weeks, add_months, add_years


def generate_task_occurrences(
    task: Task, start_date: date, end_date: date
) -> List[Tuple[date, date]]:
    """
    计算在指定日期范围内的所有任务出现日期

    Args:
        task: 任务对象
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        任务出现日期列表，每个元素为(开始日期, 结束日期)
    """
    occurrences = []

    # 检查消逝时间：如果当前日期在消逝时间之后，完全跳过该任务
    current_date = datetime.now().date()
    expiration_date = task.expiration_time.date()
    if current_date > expiration_date:
        return occurrences  # 返回空列表，完全跳过

    # 获取任务的开始和结束时间（只取日期部分）
    task_start_date = task.first_start.date()
    task_end_date = task.first_end.date()

    # 计算任务持续时间（天数）
    task_duration = (task_end_date - task_start_date).days

    # 根据重复类型生成出现日期
    if task.repeat_type == "daily":
        occurrences = _generate_daily_occurrences(
            task_start_date, task_duration, start_date, end_date, task.repeat_value
        )
    elif task.repeat_type == "weekly":
        occurrences = _generate_weekly_occurrences(
            task_start_date, task_duration, start_date, end_date, task.repeat_value
        )
    elif task.repeat_type == "monthly":
        occurrences = _generate_monthly_occurrences(
            task_start_date, task_duration, start_date, end_date, task.repeat_value
        )
    elif task.repeat_type == "yearly":
        occurrences = _generate_yearly_occurrences(
            task_start_date, task_duration, start_date, end_date, task.repeat_value
        )
    else:
        # 非重复任务，只检查是否在日期范围内
        if _is_date_in_range(task_start_date, start_date, end_date):
            occurrences.append((task_start_date, task_end_date))

    return occurrences


def _generate_daily_occurrences(
    task_start_date: date,
    task_duration: int,
    start_date: date,
    end_date: date,
    interval: int,
) -> List[Tuple[date, date]]:
    """生成每日重复的任务出现日期"""
    occurrences = []

    # 找到第一个在日期范围内的出现
    current_date = task_start_date
    while current_date < start_date:
        current_date = add_days(current_date, interval)

    # 生成所有在日期范围内的出现
    while current_date <= end_date:
        occurrence_end = add_days(current_date, task_duration)
        occurrences.append((current_date, occurrence_end))
        current_date = add_days(current_date, interval)

    return occurrences


def _generate_weekly_occurrences(
    task_start_date: date,
    task_duration: int,
    start_date: date,
    end_date: date,
    interval: int,
) -> List[Tuple[date, date]]:
    """生成每周重复的任务出现日期"""
    occurrences = []

    # 找到第一个在日期范围内的出现
    current_date = task_start_date
    while current_date < start_date:
        current_date = add_weeks(current_date, interval)

    # 生成所有在日期范围内的出现
    while current_date <= end_date:
        occurrence_end = add_days(current_date, task_duration)
        occurrences.append((current_date, occurrence_end))
        current_date = add_weeks(current_date, interval)

    return occurrences


def _generate_monthly_occurrences(
    task_start_date: date,
    task_duration: int,
    start_date: date,
    end_date: date,
    interval: int,
) -> List[Tuple[date, date]]:
    """生成每月重复的任务出现日期"""
    occurrences = []

    # 找到第一个在日期范围内的出现
    current_date = task_start_date
    while current_date < start_date:
        current_date = add_months(current_date, interval)

    # 生成所有在日期范围内的出现
    while current_date <= end_date:
        occurrence_end = add_days(current_date, task_duration)
        occurrences.append((current_date, occurrence_end))
        current_date = add_months(current_date, interval)

    return occurrences


def _generate_yearly_occurrences(
    task_start_date: date,
    task_duration: int,
    start_date: date,
    end_date: date,
    interval: int,
) -> List[Tuple[date, date]]:
    """生成每年重复的任务出现日期"""
    occurrences = []

    # 找到第一个在日期范围内的出现
    current_date = task_start_date
    while current_date < start_date:
        current_date = add_years(current_date, interval)

    # 生成所有在日期范围内的出现
    while current_date <= end_date:
        occurrence_end = add_days(current_date, task_duration)
        occurrences.append((current_date, occurrence_end))
        current_date = add_years(current_date, interval)

    return occurrences


def _is_date_in_range(target_date: date, start_date: date, end_date: date) -> bool:
    """检查日期是否在范围内"""
    return start_date <= target_date <= end_date


def get_tasks_for_date_range(
    tasks: List[Task], start_date: date, end_date: date, storage: Any
) -> Dict[date, List[Dict[str, Any]]]:
    """
    获取指定日期范围内的所有任务（按日期分组）

    Args:
        tasks: 任务列表
        start_date: 开始日期
        end_date: 结束日期
        storage: 存储管理器（用于获取任务状态）

    Returns:
        按日期分组的任务字典
    """
    from ..commands.status import get_task_status

    date_tasks = {}

    # 初始化日期字典
    current_date = start_date
    while current_date <= end_date:
        date_tasks[current_date] = []
        current_date += timedelta(days=1)

    # 处理每个任务
    for task in tasks:
        # 生成任务在日期范围内的所有出现
        occurrences = generate_task_occurrences(task, start_date, end_date)

        # 处理每个出现
        for occ_start, occ_end in occurrences:
            # 获取出现日期范围内的所有日期
            occ_current = occ_start
            while occ_current <= occ_end and occ_current <= end_date:
                if occ_current >= start_date:
                    # 获取任务状态
                    status = get_task_status(task.id, occ_current, storage)

                    # 添加到日期任务列表
                    date_tasks[occ_current].append(
                        {
                            "task": task,
                            "status": status,
                            "occurrence_start": occ_start,
                            "occurrence_end": occ_end,
                        }
                    )

                occ_current += timedelta(days=1)

    return date_tasks


def update_recent_dates(task: Task, target_date: date) -> Task:
    """
    更新任务的最近日期

    Args:
        task: 任务对象
        target_date: 目标日期

    Returns:
        更新后的任务对象
    """
    # 如果目标日期晚于最近开始日期，更新最近日期
    if target_date > task.recent_start.date():
        # 计算新的最近开始和结束日期
        time_delta = task.first_end - task.first_start

        # 根据重复类型计算下一个出现
        if task.repeat_type == "daily":
            new_recent_start = datetime.combine(
                add_days(task.recent_start.date(), task.repeat_value),
                task.recent_start.time(),
            )
        elif task.repeat_type == "weekly":
            new_recent_start = datetime.combine(
                add_weeks(task.recent_start.date(), task.repeat_value),
                task.recent_start.time(),
            )
        elif task.repeat_type == "monthly":
            new_recent_start = datetime.combine(
                add_months(task.recent_start.date(), task.repeat_value),
                task.recent_start.time(),
            )
        elif task.repeat_type == "yearly":
            new_recent_start = datetime.combine(
                add_years(task.recent_start.date(), task.repeat_value),
                task.recent_start.time(),
            )
        else:
            # 非重复任务，不更新
            return task

        new_recent_end = new_recent_start + time_delta

        task.recent_start = new_recent_start
        task.recent_end = new_recent_end

    return task
