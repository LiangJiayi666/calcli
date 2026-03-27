# CalCLI

命令行日历任务管理工具

## 安装

```bash
git clone https://github.com/LiangJiayi666/calcli.git
cd calcli
pip install -e .
```

## 快速开始

```bash
# 创建任务
calcli create --name "任务名" --description "描述" \
  --begin "2026-03-27 00:00:00" --end "2026-03-27 23:59:59"

# 查看任务
calcli view "2026-03-27" "2026-03-31" --all
```

## 详细文档

- **使用规范**: 见 [CLAUDE.md](CLAUDE.md)
- **使用指南**: 见 [.claude/calcli-assistant.md](.claude/calcli-assistant.md)


## 许可证

MIT License