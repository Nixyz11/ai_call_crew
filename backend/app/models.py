"""Data models for the AI Call Center application"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class IssueType(str, Enum):
    """Types of issues patients may have"""
    CONSULTATION = "consultation"
    APPOINTMENT = "appointment"
    SERVICE_INFO = "service_info"
    FOLLOW_UP = "follow_up"
    BILLING = "billing"
    OTHER = "other"


class PatientInfo(BaseModel):
    """Patient information model"""
    name: str = Field(..., min_length=1, max_length=100)
    phone_number: str = Field(..., regex=r'^[+]?[0-9\-\s()]+$')
    email: Optional[str] = None
    date_of_birth: Optional[str] = None
    medical_id: Optional[str] = None


class CallRequest(BaseModel):
    """Incoming call request model"""
    patient_info: PatientInfo
    issue_type: IssueType
    description: Optional[str] = None
    preferred_date: Optional[str] = None
    preferred_time: Optional[str] = None
    duration_requested: Optional[int] = None  # in minutes
    special_notes: Optional[str] = None


class CallResponse(BaseModel):
    """Call response model"""
    call_id: str
    status: str
    assistant_response: str
    next_steps: Optional[List[str]] = None
    scheduled_callback_time: Optional[str] = None
    appointment_id: Optional[str] = None


class ConsultationRequest(BaseModel):
    """Consultation request model"""
    patient_info: PatientInfo
    specialty: str
    symptoms: Optional[str] = None
    urgency_level: Optional[str] = "normal"
    preferred_doctor: Optional[str] = None


class AppointmentBooking(BaseModel):
    """Appointment booking model"""
    patient_info: PatientInfo
    service_type: str
    preferred_date: str
    preferred_time: Optional[str] = None
    duration: Optional[int] = 30  # in minutes
    doctor_id: Optional[str] = None
    notes: Optional[str] = None


class Service(BaseModel):
    """Medical service model"""
    id: str
    name: str
    description: Optional[str] = None
    duration: int  # in minutes
    cost: Optional[float] = None
    availability: Optional[List[str]] = None


class Appointment(BaseModel):
    """Appointment model"""
    id: str
    patient_info: PatientInfo
    service: Service
    date: str
    time: str
    duration: int
    status: str  # scheduled, completed, cancelled
    confirmation_number: str
    notes: Optional[str] = None


class AgentTask(BaseModel):
    """Task for CrewAI agents"""
    task_id: str
    task_type: str
    data: dict
    priority: Optional[str] = "normal"
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
