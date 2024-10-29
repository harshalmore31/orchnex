# src/orchnex/providers/base.py
from abc import ABC, abstractmethod
from typing import Optional

class LLMProvider(ABC):
    @abstractmethod
    def initialize(self, api_key: str, **kwargs):
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, temperature: Optional[float] = None) -> str:
        pass