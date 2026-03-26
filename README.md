# CalCLI

命令行日历任务管理工具

## 功能特性

- **任务管理**: 创建、更新、删除任务
- **重复任务**: 支持每日、每周、每月、每年重复
- **状态标记**: 标记任务为已完成(done)、进行中(pending)、待办(todo)
- **智能查看**: 按日期范围查看任务，支持状态筛选
- **颜色编码**: 6位唯一颜色编码标识任务
- **数据持久化**: JSON格式存储，自动备份
- **临时文件**: 查看结果自动保存到临时文件

## 安装

### 从源码安装

```bash
git clone <repository-url>
cd calcli
pip install -e .
```

### 直接使用

```bash
python -m calcli.calcli --help
```

## 使用方法

### 创建任务

```bash
calcli create --name "任务名" --description "描述" \
  --begin "2026-03-18 09:00:00" --end "2026-03-18 10:00:00" \
  --repeat weekly --x 1
```

参数说明:
- `--name`: 任务名称 (必需)
- `--description`: 任务描述 (必需)
- `--begin`: 开始时间，格式: YYYY-MM-DD HH:MM:SS (必需)
- `--end`: 结束时间，格式: YYYY-MM-DD HH:MM:SS (必需)
- `--repeat`: 重复类型: daily, weekly, monthly, yearly (默认: daily)
- `--x`: 重复间隔值，正整数 (默认: 1)

### 更新任务

```bash
calcli update A1B2C3 --name "新名称" --repeat monthly --x 2
```

可以更新任意字段组合。

### 标记任务状态

```bash
# 标记为已完成
calcli done A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为进行中
calcli pending A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为待办
calcli todo A1B2C3 --begin "2026-03-25" --end "2026-03-25"
```

### 查看任务

```bash
# 查看所有任务
calcli view "2026-03-25" "2026-03-30" --all

# 只查看待办任务
calcli view "2026-03-25" "2026-03-30" --todo

# 查看待办和进行中任务
calcli view "2026-03-25" "2026-03-30" --todopending
```

## 数据存储

所有数据存储在 `~/.calcli/` 目录下:

- `tasks.json`: 任务数据
- `timestamps.json`: 时间戳数据
- `view_YYYYMMDD_HHMMSS.txt`: 临时输出文件

## 重复任务逻辑

### 支持的类型
- **daily**: 每x天重复
- **weekly**: 每x周重复
- **monthly**: 每x月重复（自动处理不同月份的天数差异）
- **yearly**: 每x年重复（自动处理闰年）

### 状态判断规则
1. 获取任务的所有时间戳
2. 筛选包含目标日期的时间戳（start <= date <= end）
3. 按创建时间排序，取最新的
4. 无时间戳返回"todo"

## 项目结构

```
calcli/
├── calcli.py                    # 主程序入口
├── __init__.py
├── config.py                    # 配置管理
├── data/
│   ├── __init__.py
│   ├── storage.py               # JSON存储管理
│   └── models.py                # Task/Timestamp模型
├── core/
│   ├── __init__.py
│   ├── task_logic.py            # 重复任务计算
│   └── date_utils.py            # 日期处理
├── commands/
│   ├── __init__.py
│   ├── create.py
│   ├── update.py
│   ├── status.py                # done/pending/todo
│   └── view.py
├── utils/
│   ├── __init__.py
│   ├── color_code.py            # 颜色编码生成
│   └── output.py                # 格式化输出
└── tests/                       # 测试目录
```

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 代码规范

- 使用 Python 3.8+
- 遵循 PEP 8 规范
- 使用类型注解
- 中文错误提示

## 许可证

MIT License