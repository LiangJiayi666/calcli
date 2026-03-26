"""
日期处理工具
"""

from datetime import datetime, date, timedelta
from typing import List, Tuple
import calendar


def parse_date(date_str: str) -> date:
    """
    解析日期字符串

    Args:
        date_str: 日期字符串 (YYYY-MM-DD)

    Returns:
        date对象

    Raises:
        ValueError: 日期格式无效
    """
    return date.fromisoformat(date_str)


def parse_datetime(datetime_str: str) -> datetime:
    """
    解析日期时间字符串

    Args:
        datetime_str: 日期时间字符串 (YYYY-MM-DD HH:MM:SS)

    Returns:
        datetime对象

    Raises:
        ValueError: 日期时间格式无效
    """
    return datetime.fromisoformat(datetime_str)


def format_date(d: date) -> str:
    """
    格式化日期为字符串

    Args:
        d: date对象

    Returns:
        日期字符串 (YYYY-MM-DD)
    """
    return d.isoformat()


def format_datetime(dt: datetime) -> str:
    """
    格式化日期时间为字符串

    Args:
        dt: datetime对象

    Returns:
        日期时间字符串 (YYYY-MM-DD HH:MM:SS)
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_weekday_name(d: date) -> str:
    """
    获取日期的星期名称

    Args:
        d: date对象

    Returns:
        星期名称 (Monday, Tuesday, etc.)
    """
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return weekdays[d.weekday()]


def get_weekday_name_chinese(d: date) -> str:
    """
    获取日期的星期名称（中文）

    Args:
        d: date对象

    Returns:
        星期名称（周一、周二等）
    """
    weekdays_chinese = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return weekdays_chinese[d.weekday()]


def date_range(start_date: date, end_date: date) -> List[date]:
    """
    生成日期范围内的所有日期列表

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        日期列表（包含开始和结束日期）
    """
    if start_date > end_date:
        return []

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)

    return dates


def get_month_range(year: int, month: int) -> Tuple[date, date]:
    """
    获取指定年月的日期范围

    Args:
        year: 年份
        month: 月份

    Returns:
        (开始日期, 结束日期)
    """
    # 获取该月的第一天
    first_day = date(year, month, 1)

    # 获取该月的最后一天
    _, last_day_num = calendar.monthrange(year, month)
    last_day = date(year, month, last_day_num)

    return first_day, last_day


def is_valid_date_string(date_str: str) -> bool:
    """
    检查日期字符串是否有效

    Args:
        date_str: 日期字符串

    Returns:
        是否有效
    """
    try:
        date.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def is_valid_datetime_string(datetime_str: str) -> bool:
    """
    检查日期时间字符串是否有效

    Args:
        datetime_str: 日期时间字符串

    Returns:
        是否有效
    """
    try:
        datetime.fromisoformat(datetime_str)
        return True
    except ValueError:
        return False


def get_current_date() -> date:
    """
    获取当前日期

    Returns:
        当前日期
    """
    return date.today()


def get_current_datetime() -> datetime:
    """
    获取当前日期时间

    Returns:
        当前日期时间
    """
    return datetime.now()


def add_days(d: date, days: int) -> date:
    """
    在日期上添加天数

    Args:
        d: 原始日期
        days: 要添加的天数

    Returns:
        新日期
    """
    return d + timedelta(days=days)


def add_weeks(d: date, weeks: int) -> date:
    """
    在日期上添加周数

    Args:
        d: 原始日期
        weeks: 要添加的周数

    Returns:
        新日期
    """
    return d + timedelta(weeks=weeks)


def add_months(d: date, months: int) -> date:
    """
    在日期上添加月数

    Args:
        d: 原始日期
        months: 要添加的月数

    Returns:
        新日期
    """
    year = d.year
    month = d.month + months

    # 处理月份溢出
    while month > 12:
        month -= 12
        year += 1
    while month < 1:
        month += 12
        year -= 1

    # 获取该月的天数
    _, last_day = calendar.monthrange(year, month)

    # 确保日期不超过该月的最后一天
    day = min(d.day, last_day)

    return date(year, month, day)


def add_years(d: date, years: int) -> date:
    """
    在日期上添加年数

    Args:
        d: 原始日期
        years: 要添加的年数

    Returns:
        新日期
    """
    year = d.year + years
    month = d.month

    # 处理闰年2月29日的情况
    if d.month == 2 and d.day == 29:
        # 检查目标年是否是闰年
        if not calendar.isleap(year):
            # 如果不是闰年，使用2月28日
            return date(year, 2, 28)

    return date(year, month, d.day)
