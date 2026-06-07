# Glossary

- worker: 自动工人；每轮启动的短命 Claude 进程。
- wrapper: 启动脚本；负责 lock、日志、调用 Claude、写 RUNS.jsonl。
- scheduler: 外部调度器；例如 Windows Task Scheduler。
- TASKS.md: 任务定义和授权边界。
- STATE.md: 当前运行状态和失败次数权威来源。
- HANDOFF.md: 最近一轮交接。
- FAILURES.md: 失败详情记录。
- RUNS.jsonl: 每轮 wrapper 运行记录，每行一个 JSON。
- logs: 每轮 Claude 输出日志。
- lock: 防并发文件；避免多个 worker 同时写文件。
- validation: 验证；用于确认结构、测试或质量检查通过。
- scaffold: 脚手架；初始化生成的一组目录和文件。
