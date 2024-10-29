# src/orchnex/config.py
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration class for LLM settings"""
    gemini_api_key: str
    nvidia_api_key: str
    gemini_model: str = "gemini-1.5-pro-exp-0827"
    llama_model: str = "meta/llama-3.1-8b-instruct"
    max_iterations: int = 2
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 1024