# src/orchnex/providers/llama_provider.py
from typing import Optional
from openai import OpenAI
from .base import LLMProvider

class LlamaProvider(LLMProvider):
    def __init__(self):
        super().__init__()
        self.client = None
        self.model_name = "meta/llama-3.1-8b-instruct"
        self.default_params = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 10240
        }

    def initialize(self, api_key: str, **kwargs):
        """Initialize the Llama provider"""
        try:
            self.client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )
            self.model_name = kwargs.get('model_name', self.model_name)
            self._is_initialized = True
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama provider: {str(e)}")

    def generate_response(self, prompt: str, temperature: Optional[float] = None) -> str:
        """Generate response using Llama"""
        if not self.client:
            raise RuntimeError("Provider not initialized")
            
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature or self.default_params["temperature"],
                top_p=self.default_params["top_p"],
                max_tokens=self.default_params["max_tokens"]
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")