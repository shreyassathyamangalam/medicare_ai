"""
Configuration management for Medicare AI
Loads environment variables and LangChain Models
"""

# Import libraries
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from langchain_google_genai import ChatGoogleGenerativeAI
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    google_api_key: str = Field(..., description="Google Gemini API Key")
    tavily_api_key: str = Field(..., description="Tavily Search API Key")
    
    # Server Settings
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    cors_origins: str = Field(default="http://localhost:3000")
    
    # AI Model Settings
    gemini_model: str = Field(default="gemini-2.0-flash-exp")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=100, le=8192)
    
    # File Upload Settings
    max_file_size: int = Field(default=10 * 1024 * 1024) # 10MB
    
    class Config():
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origin_list(self):
        """Convert Comma-separated CORS origins to List"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    

# Global Settings Instance
settings = Settings()

@lru_cache()
def load_google_llm():
    """
    Load Google Gemini LLM with LangChain
    Cached to avoid recreating on every request
    """
    return ChatGoogleGenerativeAI(
        model = settings.gemini_model,
        google_api_key = settings.google_api_key,
        temperature = settings.temperature,
        max_output_tokens = settings.max_tokens,
        convert_system_message_to_human = True # Gemini compatibility
    )
    
@lru_cache()
def load_google_vision_llm():
    """
    Load Google Gemini with vision capabilities
    """
    return ChatGoogleGenerativeAI(
        model = settings.gemini_model,
        google_api_key = settings.google_api_key,
        temperature = 0.3, # Lower temp for consistent extraction
        max_output_tokens = settings.max_tokens,
        convert_system_message_to_human = True # Gemini compatibility
    )
