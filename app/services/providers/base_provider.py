from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseLLMProvider(ABC):
    """Abstract Base Class for LLM Script Generators."""

    @abstractmethod
    def generate_script(
        self,
        video_subject: str,
        language: str = "en-US",
        paragraph_number: int = 1,
        prompt: Optional[str] = None,
    ) -> str:
        """Generate a video script from a subject or prompt."""
        pass

    @abstractmethod
    def generate_terms(self, script: str, amount: int = 5) -> List[str]:
        """Extract search keywords/terms from a script."""
        pass


class BaseTTSProvider(ABC):
    """Abstract Base Class for Text-To-Speech Generators."""

    @abstractmethod
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice_name: str,
        rate: float = 1.0,
        volume: float = 1.0,
    ) -> Dict[str, Any]:
        """Synthesize text to an audio file."""
        pass


class BaseMaterialProvider(ABC):
    """Abstract Base Class for Video/Image Material Fetchers."""

    @abstractmethod
    def search_materials(
        self,
        keyword: str,
        amount: int = 10,
        aspect_ratio: str = "9:16",
    ) -> List[Dict[str, Any]]:
        """Search and return candidate media items."""
        pass
