# CalCLI

命令行日历任务管理工具

## 🚀 快速开始

### 安装
```bash
git clone https://github.com/LiangJiayi666/calcli.git
cd calcli
pip install -e .
```

## 🤖 智能使用指南

**强烈推荐使用 `/cal` 技能来智能管理您的任务！**

使用 Claude 的 `/cal` 技能可以：
- 智能解析自然语言指令
- 自动处理日期和时间格式
- 生成正确的 calcli 命令
- 避免手动输入复杂的参数

### 如何使用 `/cal` 技能

在 Claude 对话中，只需输入 `/cal` 后跟您的需求，例如：

```
/cal 创建一个每周一次的会议任务，从下周一开始，每周一上午9点到10点
```

```
/cal 查看下周的所有任务
```

```
/cal 我已经开完周三团队会议，请标记为已完成
```

## 📋 命令示范

### 创建任务

**使用 `/cal` 技能（推荐）：**
```
/cal 创建一个每周三下午2点的团队会议，持续1小时
```

**手动命令：**
```bash
# 创建每周重复任务
calcli create --name "团队会议" --description "每周团队同步" \
  --begin "2026-03-26 14:00:00" --end "2026-03-26 15:00:00" \
  --repeat weekly --x 1

# 创建一次性任务
calcli create --name "项目评审" --description "季度项目评审会议" \
  --begin "2026-03-28 10:00:00" --end "2026-03-28 12:00:00" \
  --expiration "2026-03-28 23:59:59"
```

### 查看任务

**使用 `/cal` 技能（推荐）：**
```
/cal 查看下周一到周五的所有任务
```

**手动命令：**
```bash
# 查看指定日期范围的所有任务
calcli view "2026-03-25" "2026-03-31" --all

# 只查看待办任务
calcli view "2026-03-25" "2026-03-31" --todo

# 查看待办和进行中任务
calcli view "2026-03-25" "2026-03-31" --todopending
```

### 更新任务状态

**使用 `/cal` 技能（推荐）：**
```
/cal 我已经开完周三团队会议，请标记为已完成
```

**手动命令：**
```bash
# 标记为已完成
calcli done A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为进行中
calcli pending A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为待办
calcli todo A1B2C3 --begin "2026-03-25" --end "2026-03-25"
```

### 更新任务信息

**使用 `/cal` 技能（推荐）：**
```
/cal 把每周团队会议改为每月重复，间隔2个月
```

**手动命令：**
```bash
calcli update A1B2C3 --name "新任务名称" --repeat monthly --x 2
```

## 🔧 参数说明

- `--name`: 任务名称 (必需)
- `--description`: 任务描述 (必需)
- `--begin`: 开始时间，格式: `YYYY-MM-DD HH:MM:SS` (必需)
- `--end`: 结束时间，格式: `YYYY-MM-DD HH:MM:SS` (必需)
- `--repeat`: 重复类型: `daily`, `weekly`, `monthly`, `yearly` (默认: `yearly`)
- `--x`: 重复间隔值，正整数 (默认: `1`)
- `--expiration`: 消逝时间，格式: `YYYY-MM-DD HH:MM:SS` (默认: `2121-02-01 21:21:00`)

## 💡 使用技巧

1. **优先使用 `/cal` 技能** - 让 Claude 智能处理您的需求
2. **自然语言描述** - 用日常语言描述您的任务需求
3. **日期智能识别** - `/cal` 能理解"明天"、"下周"、"下个月"等相对时间
4. **批量操作** - 可以一次性描述多个任务需求

## 📄 文档

- **开发规范**: [CLAUDE.md](CLAUDE.md) - 项目开发规则和流程
- **辅助技能**: [.claude/skills/calcli-assistant/](.claude/skills/calcli-assistant/) - 智能使用指南
- **技能手稿**: [../scripts/技能手稿.md](../scripts/技能手稿.md) - 详细使用示例

## 📝 许可证

MIT License