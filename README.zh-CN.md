<div align="center">

# 抖音智能体工作流包

*不是又一个上传脚本，而是抖音发布的 workflow 工程套件。*

[![License: MIT](https://img.shields.io/badge/License-MIT-3fb950?style=flat-square&labelColor=black)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Finn763/douyin-agent-workflow-kit?style=flat-square&logo=github&labelColor=black)](https://github.com/Finn763/douyin-agent-workflow-kit/stargazers)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&labelColor=black)](#安装)
[![Douyin](https://img.shields.io/badge/Platform-Douyin-161823?style=flat-square&labelColor=black)](#怎么跑)

中文 | [English](README.md)

</div>

> GitHub 上大多数抖音自动化仓库是单一用途的上传脚本，页面一改版就失效。这套包把问题反过来解：每个阶段都是提示词、契约或数据模式——模型、智能体、图片生成器、发布器都可以独立替换。

一套**不绑定特定智能体与模型**的抖音图文自动发布工作流：5 个专职智能体覆盖 8 个流水线阶段——热点 → 图文 → 图片 → 发布 → 日志，全程由一份行业画像 JSON 驱动，换个赛道只需换画像。可运行在 [OpenClaw](https://github.com/openclaw/openclaw)、[Hermes](https://github.com/NousResearch/hermes-agent)、Codex 或任何能浏览抖音创作者中心、调用本地脚本的智能体系统中。

---

## 怎么跑

![抖音流水线](docs/architecture.zh-CN.svg)

左边进画像，右边出一篇发布 + 一条 CSV 日志。[▶ 交互版](https://finn763.github.io/douyin-agent-workflow-kit/architecture.zh-CN.html)

1. **画像** — 行业 JSON 定受众、定位、关键词、视觉规则（`industry-skill/examples/` 自带 AI 科普和餐饮两个 starter）。
2. **热点 ①②** — 按关键词搜抖音关联热点，挑真实可用的（`prompts/01_hotspot_picker.md`）。
3. **图文 ③** — 每篇换角度写文案；同一热点不等于同一版式（`02_content_writer.md`）。
4. **图片 ④⑤** — AI 直出带中文标题的主封面 + Pillow 确定性渲染两张支撑卡片，统一 3:4 竖版 1080×1440（`03_image_prompt_builder.md` + `render_support_cards.py`）。
5. **校验 ⑥** — 合规检查先行，资产不过关碰不到发布页（`04_compliance_checker.md`）。
6. **发布 ⑦** — 发布器在真实发布页重搜热点；搜不到就停发，绝不硬发（`05_publisher_agent.md` + 发布器契约）。
7. **记录 ⑧** — 逐条 CSV 日志 + 失败截图。日志落文件，不打在聊天里。

---

## 为什么做这套包

| 常见的上传脚本 | 这套工作流包 |
|---|---|
| 为一个账号硬编码流程 | 行业画像 JSON 泛化到任意赛道 |
| 绑定某一种智能体/模型 | 每阶段一个提示词+契约，OpenClaw / Hermes / Codex 通用 |
| 给什么发什么 | 发布前校验资产；**热点选不上就中止，不强发** |
| 配置里存 cookie/token | **凭证零落盘**——人工登录，会话由发布器自己管理 |
| 不检查图片质量 | 强制 3:4 竖版，禁止模糊边/拉伸底图 |
| 日志打在聊天里 | 结构化 CSV 逐条日志 + 失败截图留档 |

写死在流程里的可靠性规则，不是写在注释里的建议：

- **热点二次校验**——每次发布前在真实发布页重搜，搜不到就停。
- **BGM 验证**——音乐必须在页面上同时显示歌名**和**时长才算选中。
- **封面 + 上传门禁**——图片没传完、封面没确认，一条都不发。
- **凭证安全**——密码、cookie、扫码信息、浏览器配置一律不进包。

---

## 安装

### 方式 A——脚手架一个新项目（workflow-kit）

```bash
# Windows
python workflow-kit/tools/init_project.py --target C:\douyin-ai-project --account-alias my-alias --display-name "我的抖音昵称"

# macOS / Linux
python3 workflow-kit/tools/init_project.py --target ~/douyin-ai-project --account-alias my-alias --display-name "我的抖音昵称"
```

校验草稿、发布一条排期：

```bash
python workflow-kit/tools/check_note_ready.py --project . --id demo
python workflow-kit/tools/publish_with_sau.py --project . --id demo --social-root /path/to/social-auto-upload
```

完整流程见 `workflow-kit/INSTALL.md`。

### 方式 B——把 Skill 装进你的智能体（industry-skill）

1. 把 `industry-skill/` 复制进你的智能体 skills 目录。
2. 准备一份行业画像 JSON（可从 `industry-skill/examples/` 直接改）。
3. 让智能体按画像执行抖音发布工作流。

完整规范见 `industry-skill/SKILL.md`。

---

## 包里有什么

| | |
|---|---|
| 智能体 | 5 个专职提示词（热点挑选、文案撰写、图片提示词构建、合规检查、发布执行） |
| 阶段 | 8 个，定义在 `workflow-kit/workflow/stages.md`，输入输出契约在 `io_contract.md` |
| 发布器 | 通过小契约委托（`adapters/social-auto-upload/`）；参考实现对接 [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) CLI |
| 行业包 | 2 个现成画像：AI 科普、本地生活餐饮 |
| 运行时 | 无自有运行时——Python 3.9+ 脚本 + 你自己的智能体和发布器 |

---

## 仓库结构

```
workflow-kit/               # 通用工作流包（中文文档）
├── prompts/                # 5 个分阶段智能体提示词
├── workflow/               # 阶段定义与输入输出契约
├── adapters/               # 发布器适配契约
├── configs/                # 账号 / 发布器 / 工作流配置示例
├── templates/project/      # 脚手架项目布局
├── tools/                  # 初始化 / 校验 / 演示图 / 发布脚本
└── agent_specs/            # OpenClaw / Hermes / 通用智能体任务说明
industry-skill/             # 行业可配置 Skill（英文文档）
├── SKILL.md                # 安全规则、工作流、内容/图片/发布规则
├── references/             # 内容 / 图片 / 发布 / 行业配置规则
├── examples/               # 2 个行业画像
└── scripts/                # 批量排期、卡片渲染、发布封装
docs/architecture.*         # 上面的流程图（svg + 源 spec json + 交互版 html）
```

## 相关工作

| 项目 | 关系 |
|---|---|
| [dreammis/social-auto-upload](https://github.com/dreammis/social-auto-upload) | 上传器本体——本包是它之上的工作流层 |
| [withwz/douyin_upload](https://github.com/withwz/douyin_upload) | PyAutoGUI 上传脚本，无工作流抽象 |

## 免责声明

⚠️ 本项目**仅供学习与技术研究用途**。自动化发布可能违反抖音平台用户协议（《抖音用户服务协议》5.1 条禁止使用自动化程序接入平台）。使用本软件即表示你同意：遵守平台规则与适用法律，使用风险自担；账号被限流、封禁或处罚等一切后果由使用者自行承担；控制发布频率——本包在条件不满足时会主动中止发布，而非强行发布。作者不对使用本软件产生的任何后果负责。

## 许可证

[MIT](LICENSE) © 2026 Finn763
