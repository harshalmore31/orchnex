# src/orchnex/providers/mistral_provider.py
from typing import Optional, Generator
from mistralai import Mistral
from mistralai.models.chat_completion import ChatMessage
from .base import LLMProvider

class MistralProvider(LLMProvider):
    """Mistral AI provider implementation"""
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.model_name = "mistral-large-latest"
        self.default_params = {
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 1024,
            "stream": False  # Default to non-streaming
        }
        self.system_instruction = None
        self.message_history = []

    def initialize(self, api_key: str, **kwargs):
        """Initialize the Mistral provider"""
        try:
            self.client = Mistral(api_key=api_key)
            self.model_name = kwargs.get('model_name', self.model_name)
            self.system_instruction = kwargs.get('system_instruction')
            
            # Update default parameters if provided
            if 'generation_config' in kwargs:
                self.default_params.update(kwargs['generation_config'])
            
            # Initialize message history with system instruction if provided
            if self.system_instruction:
                self.message_history = [{
                    "role": "system",
                    "content": self.system_instruction
                }]
            else:
                self.message_history = []
                
            self._is_initialized = True
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Mistral provider: {str(e)}")

    def generate_response(self, prompt: str, temperature: Optional[float] = None, stream: bool = False) -> str:
        """
        Generate response using Mistral AI
        
        Args:
            prompt (str): Input prompt
            temperature (Optional[float]): Override default temperature if provided
            stream (bool): Whether to stream the response
            
        Returns:
            str: Generated response
        """
        if not self.client:
            raise RuntimeError("Provider not initialized")
            
        try:
            # Add user message to history
            self.message_history.append({
                "role": "user",
                "content": prompt
            })
            
            # Prepare parameters
            params = self.default_params.copy()
            if temperature is not None:
                params["temperature"] = temperature
            params["stream"] = stream
            
            # Generate response
            if stream:
                return self._stream_response(params)
            else:
                return self._generate_single_response(params)
                
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")

    def _generate_single_response(self, params: dict) -> str:
        """Generate a single response"""
        response = self.client.chat(
            model=self.model_name,
            messages=self.message_history,
            **params
        )
        
        content = response.choices[0].message.content
        
        # Add assistant response to history
        self.message_history.append({
            "role": "assistant",
            "content": content
        })
        
        return content

    def _stream_response(self, params: dict) -> Generator[str, None, None]:
        """Stream the response"""
        stream_response = self.client.chat.stream(
            model=self.model_name,
            messages=self.message_history,
            **params
        )
        
        full_content = ""
        for chunk in stream_response:
            content = chunk.data.choices[0].delta.content
            if content:
                full_content += content
                yield content
        
        # Add complete response to history
        self.message_history.append({
            "role": "assistant",
            "content": full_content
        })

    def get_message_history(self) -> list:
        """Get the current message history"""
        return self.message_history

    def clear_history(self) -> None:
        """Clear the message history"""
        if self.system_instruction:
            self.message_history = [{
                "role": "system",
                "content": self.system_instruction
            }]
        else:
            self.message_history = []

    def cleanup(self) -> None:
        """Cleanup resources"""
        self.clear_history()
        self.client = None
        super().cleanup()

    def set_system_instruction(self, instruction: str) -> None:
        """Set or update the system instruction"""
        self.system_instruction = instruction
        self.clear_history()  # Reset history with new instruction