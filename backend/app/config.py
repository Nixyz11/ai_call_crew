"""Configuration module for AI Call Crew"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "AI Call Crew"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "CrewAI-powered medical call center assistant"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    
    # LLM Settings
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.7
    OPENAI_API_KEY: Optional[str] = None
    
    # CrewAI Settings
    CREW_VERBOSE: bool = True
    CREW_MEMORY: bool = True
    CREW_CACHE: bool = True
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    DB_ECHO: bool = False
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Call Center Settings
    CALL_TIMEOUT: int = 300  # seconds
    MAX_CONCURRENT_CALLS: int = 10
    ENABLE_CALL_RECORDING: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Load settings
settings = Settings()


# Agent Configurations
AGENT_CONFIGS = {
    "consultation_agent": {
        "name": "Consultation Coordinator",
        "role": "Medical Consultation Expert",
        "goal": "Guide patients through medical consultations and help schedule doctor appointments",
        "backstory": "You are an experienced medical consultation coordinator with deep knowledge of patient care processes."
    },
    "appointment_agent": {
        "name": "Appointment Booking Specialist",
        "role": "Appointment Scheduler",
        "goal": "Book and manage patient appointments with doctors and medical services",
        "backstory": "You are a professional appointment scheduler with expertise in calendar management and patient scheduling."
    },
    "service_info_agent": {
        "name": "Service Information Specialist",
        "role": "Medical Services Expert",
        "goal": "Provide comprehensive information about available medical services and procedures",
        "backstory": "You are knowledgeable about all medical services, procedures, costs, and availability."
    }
}


# Supported Issues for Routing
ISSUE_ROUTING = {
    "consultation": "consultation_agent",
    "appointment": "appointment_agent",
    "service_info": "service_info_agent",
    "follow_up": "consultation_agent",
    "billing": "service_info_agent",
    "other": "consultation_agent"
}
