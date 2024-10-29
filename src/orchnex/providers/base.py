# src/orchnex/providers/base.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class ProviderConfig:
    """Configuration settings for LLM providers"""
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 1024
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    stop_sequences: Optional[list] = None
    timeout: int = 30

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    All LLM providers must implement these methods.
    """
    
    def __init__(self):
        self._is_initialized: bool = False
        self._config: ProviderConfig = ProviderConfig()
        self._model_name: str = ""
        self._supported_models: list = []
        self._metadata: Dict[str, Any] = {}

    @abstractmethod
    def initialize(self, api_key: str, **kwargs) -> None:
        """
        Initialize the provider with necessary credentials and settings.

        Args:
            api_key (str): API key for the provider
            **kwargs: Additional provider-specific initialization parameters
        
        Raises:
            ValueError: If initialization parameters are invalid
            RuntimeError: If initialization fails
        """
        pass

    @abstractmethod
    def generate_response(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Generate a response from the LLM based on the input prompt.

        Args:
            prompt (str): Input prompt for the LLM
            temperature (Optional[float]): Override default temperature if provided

        Returns:
            str: Generated response from the LLM

        Raises:
            RuntimeError: If provider is not initialized or generation fails
        """
        pass

    def update_config(self, **kwargs) -> None:
        """
        Update provider configuration settings.

        Args:
            **kwargs: Configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
            else:
                raise ValueError(f"Invalid configuration parameter: {key}")

    def get_config(self) -> ProviderConfig:
        """
        Get current provider configuration.

        Returns:
            ProviderConfig: Current configuration settings
        """
        return self._config

    def set_model(self, model_name: str) -> None:
        """
        Set the model to use for this provider.

        Args:
            model_name (str): Name of the model to use

        Raises:
            ValueError: If model is not supported by this provider
        """
        if model_name not in self._supported_models:
            raise ValueError(f"Model {model_name} not supported by this provider")
        self._model_name = model_name

    def get_model(self) -> str:
        """
        Get current model name.

        Returns:
            str: Current model name
        """
        return self._model_name

    def get_supported_models(self) -> list:
        """
        Get list of supported models.

        Returns:
            list: List of supported model names
        """
        return self._supported_models

    def is_initialized(self) -> bool:
        """
        Check if provider is initialized.

        Returns:
            bool: True if provider is initialized, False otherwise
        """
        return self._is_initialized

    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set provider-specific metadata.

        Args:
            key (str): Metadata key
            value (Any): Metadata value
        """
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Any:
        """
        Get provider-specific metadata.

        Args:
            key (str): Metadata key

        Returns:
            Any: Metadata value

        Raises:
            KeyError: If metadata key doesn't exist
        """
        if key not in self._metadata:
            raise KeyError(f"Metadata key not found: {key}")
        return self._metadata[key]

    def validate_response(self, response: str) -> bool:
        """
        Validate provider response.

        Args:
            response (str): Response to validate

        Returns:
            bool: True if response is valid, False otherwise
        """
        return bool(response and response.strip())

    def cleanup(self) -> None:
        """
        Cleanup provider resources.
        Override this method if provider needs cleanup.
        """
        self._is_initialized = False

    def __enter__(self):
        """Context manager entry"""
        if not self._is_initialized:
            raise RuntimeError("Provider must be initialized before using as context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()

    def __str__(self) -> str:
        """String representation of provider"""
        return f"{self.__class__.__name__}(model={self._model_name}, initialized={self._is_initialized})"

    def __repr__(self) -> str:
        """Detailed string representation of provider"""
        return (f"{self.__class__.__name__}("
                f"model={self._model_name}, "
                f"initialized={self._is_initialized}, "
                f"config={self._config})")