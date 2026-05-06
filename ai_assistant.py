from config import Config
from embedding_adapter import EmbeddingEngine
from llm_adapter import LLMEngine
from ir_extractor import MinimalIR
from constraint_executor import ConstraintExecutor
from lsp_validator import LSPValidator
from memory_store import MemoryStore

class AIAssistantV15:
    def __init__(self, config: Config):
        self.config = config
        self.embedding_engine = EmbeddingEngine(config)
        self.llm = LLMEngine(config)
        self.ir = MinimalIR(config.project_root)
        self.ir.build()
        self.constraint = ConstraintExecutor(self.ir)
        self.lsp = LSPValidator()
        self.memory = MemoryStore(self.embedding_engine)
        self.project_id = config.project_root

    def generate_code(self, user_intent: str, language: str = "python") -> str:
        # 1. 从记忆检索禁止模式
        facts = self.memory.search(user_intent, k=5)
        forbidden = []
        for f in facts:
            if f["metadata"].get("type") == "forbidden":
                forbidden.append(f["metadata"].get("pattern", ""))

        # 2. IR 可用函数列表
        available_funcs = self.ir.get_function_names()[:30]

        # 3. 构建半约束 Prompt
        constraints = f"可用函数列表（只能使用这些，不准编造）：\n{', '.join(available_funcs)}\n"
        if forbidden:
            constraints += f"\n禁止使用：{', '.join(forbidden)}\n"

        prompt = f"""{constraints}
需求：{user_intent}
语言：{language}
请严格使用上面列出的函数，如果不确定是否存在某个函数，请用注释代替。生成代码："""

        # 4. 初次生成
        code = self.llm.generate(prompt)

        # 5. 硬约束重试循环
        retries = 0
        while retries < self.constraint.max_retries:
            ok, viols = self.constraint.validate(code)
            if ok:
                break
            retries += 1
            correction = f"你的代码调用了不存在的函数：{viols}。请用已知函数重写。"
            prompt = f"{constraints}\n之前生成被拒绝：{code[:300]}...\n错误：{correction}\n请重新生成。"
            code = self.llm.generate(prompt)

        # 6. LSP 兜底
        ext = 'py' if language == 'python' else 'ts'
        if not self.lsp.validate(code, f"generated.{ext}"):
            prompt = f"{constraints}\n代码编译失败，请修复语法错误。\n代码：\n{code}\n请修正。"
            code = self.llm.generate(prompt)

        return code

    def user_feedback(self, feedback: str, accepted: bool):
        if not accepted:
            self.memory.add(
                text=f"禁止使用: {feedback}",
                metadata={"type": "forbidden", "pattern": feedback}
            )