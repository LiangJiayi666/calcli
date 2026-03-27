---
name: calcli-assistant
description: CalCLI命令行日历任务管理工具的辅助技能，提供命令使用指导、参数说明、开发规范提醒和最佳实践。当用户需要了解或使用CalCLI工具时使用，包括创建任务、更新任务、查看任务、标记任务状态等操作。
---

# CalCLI Assistant

CalCLI命令行日历任务管理工具的辅助技能，帮助用户理解和使用CalCLI工具。

<!-- ## 命令行限制

只能使用以下CalCLI命令，不得创建或使用其他命令：

1. `calcli create` - 创建新任务
2. `calcli update` - 更新任务属性
3. `calcli done` - 标记任务为已完成
4. `calcli pending` - 标记任务为进行中
5. `calcli todo` - 标记任务为待办
6. `calcli view` - 查看任务

## 声明与禁止
- 不得创建`delete`命令或其他新命令
- 不得删改项目文件夹
- 所有开发必须遵循CLAUDE.md中的规范
- 有任何更新要写入.log/

## 操作确认流程（严格执行）
1. **所有命令操作前必须确认**：每次执行calcli命令行操作前，必须先把完整命令和解释发给用户
2. **等待用户明确确认**：用户必须回复"确认"、"同意"或类似的明确确认语句后才能执行
3. **批量操作单独确认**：即使是批量操作，也要先展示所有命令，等待用户确认
4. **修改后重新确认**：如果用户要求修改命令，修改后必须再次展示并等待确认
5. **禁止跳过确认**：绝对不允许在未获得用户明确确认的情况下执行任何calcli命令 -->


## 快速参考

### 创建任务（千万不要改动expiration，只需要让expiration保持默认）
#### 创建重复性任务（千万不要改动expiration，只需要让expiration保持默认）
```bash
calcli create --name "任务名" --description "描述" \
  --begin "2026-03-18 00:00:00" --end "2026-03-18 23:59:59"
```

#### 创建一次性任务（设置expiration为end时间）
```bash
calcli create --name "一次性任务" --description "描述" \
  --begin "2026-03-27 00:00:00" --end "2026-03-27 23:59:59" \
  --expiration "2026-03-27 23:59:59"
```

## 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--name` | 任务名称 | 是 | - |
| `--description` | 任务描述 | 是 | - |
| `--begin` | 开始时间 (YYYY-MM-DD HH:MM:SS) | 是 | - |
| `--end` | 结束时间 (YYYY-MM-DD HH:MM:SS) | 是 | - |
| `--repeat` | 重复类型: daily, weekly, monthly, yearly | 否 | yearly |
| `--x` | 重复间隔值，正整数 | 否 | 1 |
| `--expiration` | 消逝时间 (YYYY-MM-DD HH:MM:SS) | 否 | 2121-02-01 21:21:00 |

### 更新任务
```bash
# 更新任务属性（可更新任意字段组合）
calcli update A1B2C3 --name "新名称" --repeat monthly --x 2
```

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



