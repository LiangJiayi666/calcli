# CalCLI

命令行日历任务管理工具

## 🚀 快速开始

### 安装
```bash
git clone https://github.com/LiangJiayi666/calcli.git
cd calcli
pip install -e .
```

### 基本使用
```bash
# 创建任务（默认repeat=yearly）
calcli create --name "任务名" --description "描述" \
  --begin "2026-03-27 00:00:00" --end "2026-03-27 23:59:59"

# 查看任务
calcli view "2026-03-27" "2026-03-31" --all
```

## 🤖 使用CalCLI Assistant技能

本项目包含一个智能辅助技能，可帮助您更好地使用CalCLI：

### 技能功能
- **命令指导**：提供所有CalCLI命令的详细用法
- **参数说明**：解释每个参数的作用和格式要求
- **最佳实践**：推荐任务配置方案
- **开发规范**：提醒开发注意事项

### 如何触发技能
当您需要帮助时，可以：
1. 询问CalCLI命令用法
2. 需要创建特定类型的任务
3. 查看任务管理的最佳实践
4. 了解开发规范要求

### 技能限制
技能确保安全使用，限制只能使用以下命令：
- `calcli create` - 创建任务
- `calcli update` - 更新任务
- `calcli done` - 标记完成
- `calcli pending` - 标记进行中
- `calcli todo` - 标记待办
- `calcli view` - 查看任务

## 📚 核心概念

### 重复性任务
- 默认重复类型：`yearly`（每年）
- 默认重复间隔：`1`（每1年）
- 消逝时间：默认`2121-02-01 21:21:00`

### 一次性任务
- 设置`expiration`为任务结束时间
- 任务过期后自动跳过

## 📋 常用命令参考

```bash
# 更新任务
calcli update <任务ID> --name "新名称" --repeat monthly

# 标记任务状态
calcli done <任务ID> --begin "2026-03-25" --end "2026-03-25"

# 查看特定状态任务
calcli view "2026-03-25" "2026-03-30" --todo
```

## 📄 文档

- **开发规范**: [CLAUDE.md](CLAUDE.md) - 项目开发规则和流程
- **辅助技能**: [.claude/skills/calcli-assistant/](.claude/skills/calcli-assistant/) - 智能使用指南
- **技能手稿**: [../scripts/技能手稿.md](../scripts/技能手稿.md) - 详细使用示例

## 📝 许可证

MIT License