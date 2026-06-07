# auto-worker

一个用于 Claude Code 的自动化 skill：把长期本地任务变成安全、可恢复、可定时运行的 AI worker 循环。

> 不要再试图让一个巨大的 Claude 会话一直撑下去。让许多个短命 Claude worker 读取状态、完成一个小任务、验证、交接，然后退出。

[English README](README.md)

## 它解决什么问题？

Claude Code 很适合做专注任务，但长期项目经常会遇到这些问题：

- 对话上下文越来越长；
- 中途失败后不好恢复；
- 很难知道当前到底做到哪一步；
- 重复执行的任务又变成手动操作；
- 如果 prompt 写得太宽，自动化容易失控；
- 缺少日志、交接和恢复状态；
- 想让 Claude 定时做事，但不知道怎么设计才安全。

`auto-worker` 提供的是一套可复用模式：

```text
外部调度器
  -> 启动 wrapper 脚本
  -> 新的 claude --print 进程
  -> 读取 TASKS / STATE / HANDOFF / FAILURES
  -> 完成一个小任务
  -> 运行验证
  -> 更新状态和交接
  -> 写入日志
  -> 退出
```

也就是说，它不是让一个 Claude 会话无限变长，而是让很多个短命 Claude worker 接力完成长期任务。

## 适合谁？

如果你想让 Claude Code 持续推进本地文件任务，同时又希望过程可控、可暂停、可检查，这个 skill 就适合你。

适合：

- 写作者：写书、课程、文章、Newsletter、短视频脚本；
- 开发者：低风险代码维护、补测试、补文档、小步迁移、清理；
- 知识工作者：维护笔记、文档、研究资料、知识库；
- 内容创作者：把长期想法拆成内容库；
- 自动化爱好者：想让 Claude Code 定时推进任务，但不想失控。

不适合完全无人值守的高风险操作：

- 自动交易；
- 自动转账；
- 自动公开发布；
- 自动部署生产系统；
- 群发消息；
- 凭证测试；
- 删除未知文件。

这些场景应该人工确认，或者改成本地草稿/分析/待审批清单。

## 它能做什么？

这个 skill 可以帮助 Claude Code：

- 创建新的 auto-worker 脚手架；
- 生成 `TASKS.md`、`STATE.md`、`HANDOFF.md`、`FAILURES.md`、`worker-prompt.md`；
- 创建 PowerShell 和 Git Bash wrapper 脚本；
- 手动试跑一轮；
- 注册或修改 Windows Task Scheduler 计划任务；
- 读取状态文件和日志，查看当前进度；
- 暂停或恢复 worker；
- 用普通语言解释 auto-worker 目录结构；
- 应用保守的安全边界。

## 示例场景

### 1. 长期写一本书

```text
/auto-worker 给我的书稿项目创建一个 writing worker。每轮只写或修订一个章节小节，完成后验证结构、更新交接，然后退出。不要发布任何内容。
```

### 2. 持续维护文档

```text
/auto-worker 创建一个 docs-worker，每轮检查 docs/ 里的一个文件，提升表达清晰度，运行链接或格式检查，然后更新 STATE.md。
```

### 3. 整理个人知识库

```text
/auto-worker 创建一个 notes-worker，每轮读取一篇笔记，提取关键观点，补充相关链接，写入摘要。禁止联网。
```

### 4. 低风险代码维护

```text
/auto-worker 创建一个 test-worker，每轮只新增或改进一个测试文件，然后运行对应测试命令。不要自动 commit，也不要 push。
```

### 5. 查看 worker 当前状态

```text
/auto-worker 看看我的 book worker 现在跑到哪里了。总结最新 STATE、HANDOFF、RUNS 和日志。
```

### 6. 暂停自动化

```text
/auto-worker 暂停这个 worker。不要删除任何已经生成的文件和日志。
```

## 安装

使用 Skills CLI 从 GitHub 安装：

```bash
npx skills add HanGe88/auto-worker
```

或者手动把本仓库复制到 Claude skills 目录：

```text
~/.claude/skills/auto-worker/
```

然后在 Claude Code 里使用：

```text
/auto-worker 创建一个 worker，用来持续推进我的本地长期任务。
```

## 核心设计

一个 auto-worker 通常有三层。

### 1. 工作区

也就是实际产出所在的目录，例如：

```text
book/
docs/
notes/
work/
```

### 2. worker 状态目录

这是 worker 的“记忆”和“规则书”：

```text
.claude/auto-worker/<worker-name>/
  TASKS.md
  STATE.md
  HANDOFF.md
  FAILURES.md
  worker-prompt.md
  RUNS.jsonl
  logs/
```

含义：

| 文件 | 作用 |
| --- | --- |
| `TASKS.md` | 长期任务队列、目标、权限和禁止动作 |
| `STATE.md` | 当前进度、连续失败次数、下一步建议 |
| `HANDOFF.md` | 最近一轮做了什么、改了什么、下一轮做什么 |
| `FAILURES.md` | 失败详情和排查线索 |
| `worker-prompt.md` | 每一轮新 Claude worker 读取的固定提示词 |
| `RUNS.jsonl` | 每轮 wrapper 的机器可读运行记录 |
| `logs/` | 每轮 Claude 输出日志 |

### 3. 执行脚本

wrapper 脚本负责启动 Claude、写日志、防并发和记录运行结果：

```text
.claude/auto-worker/run-<worker-name>-worker.ps1
.claude/auto-worker/run-<worker-name>-worker.sh
```

Windows Task Scheduler 等外部调度器可以定时运行这些 wrapper。

## 为什么这种模式有效？

每一轮 Claude 都是新的、短命的，但项目状态不是。

每个 worker 都会从文件中恢复上下文：

```text
读取 TASKS.md
读取 STATE.md
读取 HANDOFF.md
读取 FAILURES.md
选择一个小任务
修改授权范围内的文件
运行验证
更新 STATE.md 和 HANDOFF.md
退出
```

所以整个流程具备：

- 可恢复；
- 可审计；
- 更安全；
- 可暂停；
- 可检查；
- 不依赖超长聊天上下文。

## 默认安全边界

生成的 worker 默认应该是保守的：

- 不访问网络；
- 不调用外部 API；
- 不下载依赖；
- 不 push、发布、部署；
- 不删除未知文件；
- 不修改系统或用户级配置；
- 不处理 secrets、密码、token、cookie、私钥；
- 不在 worker 内部再启动新的 Claude 进程；
- 不进入无限循环；
- 每轮只做一个小任务；
- 每轮都验证和交接；
- 连续失败后停止修改。

如果某个任务确实需要更高权限，应该由用户明确授权，并把授权写入 `TASKS.md`。

## 仓库内容

```text
SKILL.md
README.md
README.zh-CN.md

templates/
  worker/
    TASKS.md.template
    STATE.md.template
    HANDOFF.md.template
    FAILURES.md.template
    worker-prompt.md.template
  scripts/
    run-worker.ps1.template
    run-worker.sh.template

references/
  worker-patterns.md
  windows-task-scheduler.md
  safety-rules.md
  troubleshooting.md
  glossary.md

scripts/
  inspect_worker.py

evals/
  evals.json
  trigger-evals.json
```

## 当前成熟度

这是一个 MVP 级 skill，来自一次真实 Claude Code auto-worker 实验。

它已经适合低风险、本地文件型、长期任务自动化，但不应该被理解成完全自治的生产运维系统。

当前优势：

- 来自真实写作自动化实践；
- 有保守安全模型；
- 使用文件状态恢复和交接；
- 包含 Windows Task Scheduler 经验；
- 包含 PowerShell / Git Bash wrapper 模板；
- 提供状态检查脚本；
- 提供 eval prompt，方便后续测试。

当前不足：

- 还没有确定性 `create_worker.py` 生成器；
- Windows 支持最完整，macOS / Linux 调度文档还未补齐；
- 还没有跑完整 benchmark / eval viewer；
- 还没有图形化状态面板；
- 最终质量仍依赖清晰的 `TASKS.md` 和阶段性人工 review。

## 路线图

计划增强：

- `create_worker.py`：根据模板确定性生成 worker；
- `schedule_windows.py`：管理 Task Scheduler 的创建、查询、暂停、恢复和调频；
- Markdown 状态报告，让非技术用户更容易查看；
- 阶段性质量门，例如“每个阶段结束后暂停”；
- macOS / Linux 调度支持；
- 正式 skill eval 和触发描述优化；
- 打包成 `.skill` 发布。

## 设计理念

目标不是让 AI 失控地自动运行。

目标是让长期 AI 工作变得：

```text
足够小，可以验证；
足够安全，可以调度；
足够清晰，可以检查；
足够结构化，可以恢复。
```

当你想要的是“有记忆、有边界、有日志、有停止按钮”的自动化，而不是失控的自动执行时，就适合使用 `auto-worker`。
