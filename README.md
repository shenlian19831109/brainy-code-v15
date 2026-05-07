BrainyCode v1.5 —— 类脑可验证代码生成助手
用大脑的双系统记忆与程序真相层（IR）消除 AI 编程幻觉。
不训练模型，将“编造函数”类幻觉降低 80% 以上。

核心原理
大模型写代码时经常编造不存在的 API、忘记你的偏好，根本原因是生成过程缺乏事实锚点。
本项目模拟人脑的 互补学习系统，并引入 极简程序真相（IR） 实现半约束生成：

海马体 MemoryStore 快速存储情景记忆（用户偏好、禁止模式），通过内容寻址检索。

皮层语义 MinimalIR 从项目源码提取函数名，构成精确的符号表。

前额叶 ConstraintExecutor 在 LLM 生成后立即检查调用的函数是否真实存在。

预测编码回路：生成 → 校验 → 检测到不存在函数（误差信号）→ 自动生成修正提示并让模型重写 → 最后经 LSP 语法检查兜底。

效果：在不重新训练模型的前提下，消除绝大多数“调用不存在函数”的幻觉，整体可用性大幅提升。

安装与配置
1. 克隆仓库并安装依赖
bash
git clone https://github.com/你的用户名/BrainyCode-v15.git
cd BrainyCode-v15
pip install -r requirements.txt
# 如果使用 OpenAI 的嵌入或 LLM，额外执行：
pip install openai
2. 选择嵌入服务（二选一）
OpenAI 嵌入（推荐，成本极低）
前往 platform.openai.com 创建 API Key，然后设置环境变量：

bash
export EMBED_PROVIDER=openai
export EMBED_MODEL=text-embedding-3-small
export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
Jina AI 嵌入（带免费额度）
注册 jina.ai 获取 Key，然后设置：

bash
export EMBED_PROVIDER=jina
export EMBED_MODEL=jina-embeddings-v3
export JINA_API_KEY=jina_xxxxxxxxxxxxxxxxxxxxxxxx
3. 选择语言模型（LLM）
本地免费 Ollama（推荐）
安装并拉取模型，例如 ollama pull codestral，然后设置：

bash
export LLM_PROVIDER=ollama
export LLM_MODEL=codestral
或使用 OpenAI

bash
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o-mini
💡 可以将以上环境变量写入 .env 文件（已在 .gitignore 忽略）。

使用方法
在你的项目目录下执行所有命令。

构建 IR（程序真相）

bash
python /path/to/cli.py build-ir --project-root .
输出：✅ IR 构建完成，共 X 个函数。

半约束生成代码

bash
python /path/to/cli.py generate --project-root . "你的需求描述"
系统会自动：

将项目内可用函数列表注入 prompt

拦截编造的不存在函数并强制 LLM 重写

使用 LSP 语法检查兜底

记录用户偏好（可选）
在 Python 交互环境或脚本中：

python
from config import Config
from ai_assistant import AIAssistantV15
assistant = AIAssistantV15(Config(project_root="."))
assistant.user_feedback("不要使用 eval", accepted=False)
此规则将被存入记忆，后续生成自动避免。

项目结构说明
text
ai_hippocampus_v15/
├── ai_assistant.py            # 主程序，整合所有模块
├── cli.py                     # 命令行入口
├── config.py                  # 配置管理，读取环境变量
├── constraint_executor.py     # 硬约束执行器（前额叶）
├── embedding_adapter.py       # 嵌入适配（OpenAI/Jina）
├── ir_extractor.py            # 极简 IR 提取（函数名、参数、文件）
├── llm_adapter.py             # LLM 适配（Ollama/OpenAI/HuggingFace）
├── lsp_validator.py           # LSP 语法兜底检查
├── memory_store.py            # 向量记忆库（海马体）
├── requirements.txt           # 依赖清单
└── .gitignore                 # 忽略 .env、记忆文件、缓存


类脑机制对照表
脑结构	工程模块	功能
海马体	MemoryStore	情景记忆、内容寻址
新皮层	MinimalIR	语义记忆（精确符号表）
前额叶	ConstraintExecutor	监控输出、产生错误信号
预测编码	校验-重试回路	误差驱动修正
双系统	快记忆写入 + IR 慢更新	解决稳定性-可塑性困境
路线图
v1.5 极简 IR + 硬约束 + 半约束生成 （当前版本）

v2.0 alpha 完整 IR（类型、调用图）+ 约束解码

v2.0 beta 多语言、搜索式合成、私有化部署

许可证 MIT License • 欢迎提交 Issue/PR 一起推进。
