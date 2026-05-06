from config import Config

class LLMEngine:
    def __init__(self, config: Config):
        self.provider = config.llm.provider
        self.model = config.llm.model_name
        self.api_key = config.llm.api_key
        self.base_url = config.llm.base_url

    def generate(self, prompt: str, max_tokens=1024) -> str:
        if self.provider == "ollama":
            import requests
            url = f"{self.base_url or 'http://localhost:11434'}/api/generate"
            resp = requests.post(url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            return resp.json()["response"]
        elif self.provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        elif self.provider == "huggingface_inference":
            import requests
            headers = {"Authorization": f"Bearer {self.api_key}"}
            api_url = f"https://api-inference.huggingface.co/models/{self.model}"
            resp = requests.post(api_url, headers=headers, json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": max_tokens}
            })
            return resp.json()[0]['generated_text']
        else:
            raise ValueError("未配置 LLM 提供者")