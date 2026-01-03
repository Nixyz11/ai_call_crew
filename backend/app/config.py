"""Configuration module for AI Call Crew - Ollama Version"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings for Ollama-based AI Call Crew"""
    
    # API Settings
    API_TITLE: str = "AI Call Crew"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "CrewAI-powered medical call center assistant with Ollama"
    DEBUG: bool = True
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Ollama Settings (LOCAL LLM)
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 512
    
    # CrewAI Settings
    CREW_VERBOSE: bool = True
    CREW_MEMORY: bool = True
    CREW_CACHE: bool = True
    
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
        "backstory": "You are an experienced medical consultation coordinator with deep knowledge of patient care processes and medical services. Listen carefully to patient symptoms and concerns, ask clarifying questions, and recommend appropriate medical services."
    },
    "appointment_agent": {
        "name": "Appointment Booking Specialist",
        "role": "Appointment Scheduler",
        "goal": "Efficiently book and manage patient appointments with doctors and medical services",
        "backstory": "You are a professional appointment scheduler with expertise in calendar management and patient scheduling. Confirm patient availability, check doctor schedules, and book appointments with attention to detail."
    },
    "service_info_agent": {
        "name": "Service Information Specialist",
        "role": "Medical Services Expert",
        "goal": "Provide comprehensive information about available medical services, procedures, and costs",
        "backstory": "You are knowledgeable about all medical services offered, procedures, duration, costs, and availability. Explain services clearly to patients and help them choose appropriate services for their needs."
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


# Ollama Model Information
AVAILABLE_MODELS = {
    "mistral": {
        "name": "Mistral 7B",
        "size": "4.4 GB",
        "speed": "Fast",
        "quality": "Excellent",
        "recommended": True
    },
    "llama2": {
        "name": "Llama 2 7B",
        "size": "3.8 GB",
        "speed": "Moderate",
        "quality": "Good",
        "recommended": False
    },
    "gemma:2b": {
        "name": "Gemma 2B",
        "size": "1.7 GB",
        "speed": "Very Fast",
        "quality": "Fair",
        "recommended": False
    }
}
