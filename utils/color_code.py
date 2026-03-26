"""
颜色编码生成器
生成6位大写字母+数字组合的颜色编码
"""

import random
import string
from typing import List, Optional


class ColorCodeGenerator:
    """颜色编码生成器"""

    # 允许的字符：大写字母A-F和数字0-9
    ALLOWED_CHARS = string.ascii_uppercase[:6] + string.digits  # A-F, 0-9

    def __init__(self, existing_codes: Optional[List[str]] = None):
        """
        初始化颜色编码生成器

        Args:
            existing_codes: 已存在的颜色编码列表，用于避免重复
        """
        self.existing_codes = set(existing_codes) if existing_codes else set()

    def generate_code(self) -> str:
        """
        生成一个唯一的6位颜色编码

        Returns:
            6位颜色编码字符串
        """
        while True:
            # 生成6位随机字符
            code = "".join(random.choice(self.ALLOWED_CHARS) for _ in range(6))

            # 检查是否唯一
            if code not in self.existing_codes:
                self.existing_codes.add(code)
                return code

    def generate_multiple(self, count: int) -> List[str]:
        """
        生成多个唯一的颜色编码

        Args:
            count: 要生成的编码数量

        Returns:
            颜色编码列表
        """
        codes = []
        for _ in range(count):
            codes.append(self.generate_code())
        return codes

    def is_valid_code(self, code: str) -> bool:
        """
        检查颜色编码是否有效

        Args:
            code: 要检查的编码

        Returns:
            是否有效
        """
        # 检查长度
        if len(code) != 6:
            return False

        # 检查所有字符是否在允许的范围内
        for char in code:
            if char not in self.ALLOWED_CHARS:
                return False

        return True

    @classmethod
    def get_allowed_chars(cls) -> str:
        """
        获取允许的字符集

        Returns:
            允许的字符字符串
        """
        return cls.ALLOWED_CHARS

    @classmethod
    def get_code_pattern(cls) -> str:
        """
        获取颜色编码的正则表达式模式

        Returns:
            正则表达式模式字符串
        """
        return f"^[{cls.ALLOWED_CHARS}]{{6}}$"


# 工具函数
def generate_color_code(existing_codes: Optional[List[str]] = None) -> str:
    """
    生成单个颜色编码的便捷函数

    Args:
        existing_codes: 已存在的颜色编码列表

    Returns:
        6位颜色编码
    """
    generator = ColorCodeGenerator(existing_codes)
    return generator.generate_code()


def validate_color_code(code: str) -> bool:
    """
    验证颜色编码的便捷函数

    Args:
        code: 要验证的编码

    Returns:
        是否有效
    """
    return ColorCodeGenerator().is_valid_code(code)


def generate_unique_codes(
    count: int, existing_codes: Optional[List[str]] = None
) -> List[str]:
    """
    生成多个唯一颜色编码的便捷函数

    Args:
        count: 要生成的编码数量
        existing_codes: 已存在的颜色编码列表

    Returns:
        颜色编码列表
    """
    generator = ColorCodeGenerator(existing_codes)
    return generator.generate_multiple(count)
