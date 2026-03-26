"""
CalCLI 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="calcli",
    version="1.0.0",
    author="CalCLI Team",
    author_email="",
    description="命令行日历任务管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "calcli=calcli.calcli:main",
        ],
    },
)
