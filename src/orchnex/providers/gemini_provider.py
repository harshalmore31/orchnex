# src/orchnex/providers/gemini_provider.py
from typing import Optional
import google.generativeai as genai
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self):
        super().__init__()
        self.model = None
        self.chat_session = None
        self.model_name = "gemini-1.5-pro-exp-0827"
        self.default_params = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 10240
        }

    def initialize(self, api_key: str, **kwargs):
        """Initialize the Gemini provider"""
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Update configuration
            generation_config = self.default_params.copy()
            generation_config.update(kwargs.get('generation_config', {}))
            
            # Initialize model with system instruction
            self.model = genai.GenerativeModel(
                model_name=kwargs.get('model_name', self.model_name),
                generation_config=generation_config,
                system_instruction=kwargs.get('system_instruction', '')
            )
            
            # Start chat session
            self.chat_session = self.model.start_chat()
            self._is_initialized = True
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini provider: {str(e)}")

    def generate_response(self, prompt: str, temperature: Optional[float] = None) -> str:
        """Generate response using Gemini"""
        if not self.chat_session:
            raise RuntimeError("Provider not initialized")
            
        try:
            response = self.chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")