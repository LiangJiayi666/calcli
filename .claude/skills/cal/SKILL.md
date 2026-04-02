---
name: cal
description: CalCLI命令行日历任务管理工具的辅助技能，提供命令使用指导、参数说明、开发规范提醒和最佳实践。当用户需要了解或使用CalCLI工具时使用，包括创建任务、更新任务、查看任务、标记任务状态等操作。
---

# CalCLI Assistant

CalCLI命令行日历任务管理工具的辅助技能，帮助用户理解和使用CalCLI工具。


## 快速参考

### 创建任务
#### 创建重复性任务（设置expiration为用户指定的任务结束时间）
- 设置expiration为用户指定的任务结束时间；若用户未指定任务结束时间，则询问用户；若用户回答永不结束，则不设置expiration参数
```bash
calcli create --name "任务名" --description "描述" \
  --begin "2026-03-18 00:00:00" --end "2026-03-18 23:59:59"
  --repeat daily --x 1 \
  --expiration "2026-03-27 23:59:59"
```

#### 创建一次性任务（设置expiration为end时间）
```bash
calcli create --name "一次性任务" --description "描述" \
  --begin "2026-03-18 00:00:00" --end "2026-03-18 23:59:59" \
  --expiration "2026-03-18 23:59:59"
```
#### 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--name` | 任务名称 | 是 | - |
| `--description` | 任务描述 | 是 | - |
| `--begin` | 开始时间 (YYYY-MM-DD HH:MM:SS) | 是 | - |
| `--end` | 结束时间 (YYYY-MM-DD HH:MM:SS) | 是 | - |
| `--repeat` | 重复类型: daily, weekly, monthly, yearly | 否 | yearly |
| `--x` | 重复间隔值，正整数 | 否 | 1 |
| `--expiration` | 消逝时间 (YYYY-MM-DD HH:MM:SS) | 否 | 2121-02-01 21:21:00 |


### 查看任务
```bash
# 一般直接查看待办和进行中任务
calcli view "2026-03-25" "2026-03-30" --filter todopending

# 只查看待办任务
calcli view "2026-03-25" "2026-03-30" --filter todo

# 查看所有任务
calcli view "2026-03-25" "2026-03-30" --filter all
```

### 更新任务
- 先查看所有任务，找出任务编号，再更新任务属性
```bash
# 查看所有任务，找出任务编号
calcli list
# 更新任务属性（可更新任意字段组合）
calcli update A1B2C3 --name "新名称" --repeat monthly --x 2
```

### 标记任务状态
- 先查看所有任务，找出任务编号，再标记任务状态
```bash
# 查看所有任务，找出任务编号
calcli list

# 标记为已完成
calcli done A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为进行中
calcli pending A1B2C3 --begin "2026-03-25" --end "2026-03-25"

# 标记为待办
calcli todo A1B2C3 --begin "2026-03-25" --end "2026-03-25"
```





