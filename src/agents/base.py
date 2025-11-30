"""
Base class for all AI agents.

Provides common functionality and interface for agents.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic
import structlog
from google import genai

from ..config.settings import Settings, get_settings

log = structlog.get_logger()

# Type variables for input and output
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')


class BaseAgent(ABC, Generic[InputType, OutputType]):
    """
    Abstract base class for all AI agents.

    Provides:
    - Gemini client initialization
    - Logging
    - Error handling
    - Common agent interface
    """

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7,
        settings: Optional[Settings] = None
    ):
        """
        Initialize the base agent.

        Args:
            model: Gemini model name (defaults to settings)
            temperature: Model temperature (0.0 to 1.0)
            settings: Application settings (auto-loaded if not provided)
        """
        self.settings = settings or get_settings()
        self.model = model or self.settings.gemini_model_digest
        self.temperature = temperature

        # Initialize Gemini client
        self.client = genai.Client(api_key=self.settings.gemini_api_key)

        # Logger with agent context
        self.log = log.bind(
            agent=self.__class__.__name__,
            model=self.model,
            temperature=temperature
        )

        self.log.info("Agent initialized")

    @abstractmethod
    def process(self, input_data: InputType) -> OutputType:
        """
        Process input and return output.

        Must be implemented by subclasses.

        Args:
            input_data: Input to process

        Returns:
            Processed output
        """
        pass

    def _generate_content(
        self,
        contents: str,
        response_schema: Any,
        temperature: Optional[float] = None
    ) -> Any:
        """
        Generate content using Gemini with structured output.

        Args:
            contents: Prompt content
            response_schema: Pydantic model for response validation
            temperature: Override default temperature

        Returns:
            Validated Pydantic model instance
        """
        temp = temperature if temperature is not None else self.temperature

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config={
                    "temperature": temp,
                    "response_mime_type": "application/json",
                    "response_schema": response_schema
                }
            )

            return response_schema.model_validate_json(response.text)

        except Exception as e:
            self.log.error("Content generation failed", error=str(e))
            raise

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(model={self.model}, temperature={self.temperature})"
