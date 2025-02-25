import os
from typing import Optional, Dict, Any
import requests
import openai
from ..config import LLM_MODELS, OPENAI_MODEL, OPENAI_TEMPERATURE

class LLMHandler:
    def __init__(self):
        self.current_model = None
        self.assistant = None
        self.model_config = None
        self.travel_context = "You are a helpful travel assistant. Help users plan their trips, suggest destinations, activities, and provide travel tips."

    def initialize_model(self, model_type: str, api_key: Optional[str] = None) -> Any:
        """Initialize the selected LLM model."""
        if model_type not in LLM_MODELS:
            raise ValueError(f"Unsupported model type: {model_type}")

        self.model_config = LLM_MODELS[model_type]
        self.current_model = model_type

        if model_type == "ollama":
            return self._initialize_ollama()
        elif model_type == "openai":
            return self._initialize_openai(api_key)

    def _initialize_ollama(self) -> Any:
        """Initialize Ollama model."""
        try:
            # Check if Ollama is running
            response = requests.get('http://localhost:11434/api/version')
            if response.status_code != 200:
                raise ConnectionError("Ollama service is not running")

            # Import here to avoid dependency issues if not using Ollama
            from langchain_community.llms import Ollama
            
            self.assistant = Ollama(
                model=self.model_config["model"],
                system=self.travel_context
            )
            return self.assistant

        except Exception as e:
            raise ConnectionError(f"Failed to initialize Ollama: {str(e)}")

    def _initialize_openai(self, api_key: str) -> Any:
        """Initialize OpenAI model."""
        if not api_key:
            raise ValueError("OpenAI API key is required")

        try:
            openai.api_key = api_key
            
            # Import here to avoid dependency issues if not using OpenAI
            from langchain_openai import ChatOpenAI
            
            self.assistant = ChatOpenAI(
                model=OPENAI_MODEL,
                temperature=OPENAI_TEMPERATURE,
                api_key=api_key
            )
            return self.assistant

        except Exception as e:
            raise ConnectionError(f"Failed to initialize OpenAI: {str(e)}")

    def chat(self, prompt: str, context: Optional[Dict[str, str]] = None) -> str:
        """Send a chat message to the current model with travel context."""
        if not self.assistant:
            raise RuntimeError("No model initialized. Call initialize_model first.")

        try:
            # Enhance prompt with travel context if provided
            enhanced_prompt = self._build_travel_prompt(prompt, context)
            response = self.assistant.invoke(enhanced_prompt)
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            raise RuntimeError(f"Error during chat: {str(e)}")

    def _build_travel_prompt(self, prompt: str, context: Optional[Dict[str, str]] = None) -> str:
        """Build a travel-specific prompt with context."""
        if not context:
            return prompt

        context_str = []
        if context.get('destination'):
            context_str.append(f"Destination: {context['destination']}")
        if context.get('dates'):
            context_str.append(f"Travel Dates: {context['dates']}")
        if context.get('budget'):
            context_str.append(f"Budget: {context['budget']}")
        if context.get('interests'):
            context_str.append(f"Interests: {', '.join(context['interests'])}")

        if context_str:
            return f"Context: {'. '.join(context_str)}\n\nQuery: {prompt}"
        return prompt

    def get_current_model(self) -> Dict[str, Any]:
        """Get information about the current model."""
        if not self.model_config:
            raise RuntimeError("No model initialized")
        return self.model_config 