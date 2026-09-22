# 5S Audit & Scoring App — Python Logic

这个仓库收集了从「5S Audit & Scoring App」低代码模板（`template.json`，疑似 Builder.ai 类平台导出的应用）中提取出来的 **Python 代码节点**（workflow 中的 `Code/Python` 组件）。

原始文件是一个完整的低代码应用模板（页面布局、表单、工单等 JSON 配置），本仓库只保留其中真正的 Python 逻辑部分，方便版本管理和代码审查。

## ⚠️ 重要说明

这些脚本运行在低代码工作流引擎的 "Code/Python" 节点里，**不是独立可执行的 Python 脚本**。它们依赖平台注入的运行时变量：

- `parameter` — 一个 list，`parameter[1]`、`parameter[2]`… 对应节点输入端口的值
- `output` — 一个 dict/list，`output[1] = ...` 用来写节点输出端口
- `internal_memory` — 部分节点用它做跨执行的状态持久化（去重逻辑用到）

如果要在本地/GitHub Actions 里独立运行或做单元测试，需要自己 mock 这些变量。例如运行 `tests/test_dedup_verification.py` 前，需要先在同一作用域里定义一个 `output = {}`（脚本本身只模拟了业务逻辑和断言，`output[1] = ...` 这一行沿用了平台的写法）。

## 目录结构

```
.
├── finding_capa_escalation/
│   └── capa_escalation.py       # 5S 发现项（Finding）严重度达标后自动升级为 CAPA，
│                                 # 创建 CAPA 工单 + 发送通知邮件，并做防重复触发
├── ai_photo_analysis/
│   ├── resolve_photo_urls.py    # 从 Finding 工单的 evidence_photo 字段解析出可访问的图片 URL，
│   │                             # 供后续 LLM Vision 节点分析
│   └── process_vision_response.py # 解析 LLM Vision 的返回结果，写回 AI 检测结论/置信度/框选坐标
└── tests/
    └── test_dedup_verification.py # 对 CAPA 去重逻辑的模拟测试（3 次连续状态更新只应产生 1 个 CAPA + 1 封邮件）
```

## 各脚本说明

### `finding_capa_escalation/capa_escalation.py`
在 Finding 工单被创建/确认为 High/Critical 严重度时触发：
- 用 `internal_memory` + `capa_reference_id` 双重防重复检查，避免同一 Finding 被重复升级
- 生成 `CAPA-{audit_id}-{finding_id前8位}` 格式的 CAPA 单号
- 输出 CAPA 工单创建 payload、通知邮件收件人/主题/正文、以及回写 Finding 工单的更新 payload

### `ai_photo_analysis/resolve_photo_urls.py`
接收 Ticket 创建事件里的 `evidence_photo` 字段（可能是 dict/list/字符串等多种格式），统一解析成完整可访问的图片 URL 列表，交给下一个节点传给视觉大模型。

### `ai_photo_analysis/process_vision_response.py`
解析视觉大模型返回的 JSON（是否违规、置信度、边界框），标准化置信度到 0–100 范围，并组装成回写 Finding 工单的 payload。

### `tests/test_dedup_verification.py`
模拟同一张 Finding 工单连续 3 次状态更新事件，验证 CAPA 升级与邮件发送逻辑只会执行一次（防重复触发的回归测试）。

## 免责声明

这些代码是从业务模板中原样提取的，包含硬编码的示例值（如日期、内部邮箱地址等），推送到公开仓库前请自行检查并替换成环境变量或占位符，避免泄露内部信息。
