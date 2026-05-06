import requests
from config import Config

class EmbeddingEngine:
    def __init__(self, config: Config):
        self.provider = config.embedding.provider
        self.model_name = config.embedding.model_name
        self.api_key = config.embedding.api_key
        self.base_url = config.embedding.base_url

        if not self.api_key:
            raise ValueError(
                f"请设置 {self.provider.upper()}_API_KEY 环境变量。\n"
                f"获取方式：\n"
                f"  - OpenAI: https://platform.openai.com/api-keys\n"
                f"  - Jina AI: https://jina.ai/embeddings/ (注册后获取)"
            )

    def encode(self, texts):
        if self.provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            resp = client.embeddings.create(input=texts, model=self.model_name)
            return [d.embedding for d in resp.data]

        elif self.provider == "jina":
            url = "https://api.jina.ai/v1/embeddings"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            payload = {"model": self.model_name, "input": texts}
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return [item["embedding"] for item in data["data"]]

        else:
            raise ValueError(f"不支持的嵌入提供者: {self.provider}")