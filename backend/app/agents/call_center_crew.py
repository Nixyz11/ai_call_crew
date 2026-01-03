"""CrewAI Agents for medical call center"""

from crewai import Agent, Task, Crew
from crewai_tools import tool
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# Tools for agents
@tool
def check_doctor_availability(date: str, time: str, doctor_id: Optional[str] = None) -> str:
    """Check doctor availability for a specific date and time"""
    return f"Doctor availability checked for {date} at {time}. Status: Available"


@tool
def book_appointment(patient_name: str, doctor_id: str, date: str, time: str) -> str:
    """Book an appointment with a doctor"""
    return f"Appointment booked for {patient_name} with doctor {doctor_id} on {date} at {time}"


@tool
def get_service_info(service_type: str) -> str:
    """Get information about medical services"""
    services = {
        "consultation": "General consultation - 30 mins - $50",
        "dental": "Dental checkup - 45 mins - $75",
        "lab_tests": "Lab tests - 15 mins - $100",
        "follow_up": "Follow-up visit - 20 mins - $30"
    }
    return services.get(service_type, "Service not found")


@tool
def schedule_callback(patient_name: str, phone: str, callback_time: str) -> str:
    """Schedule a callback for the patient"""
    return f"Callback scheduled for {patient_name} ({phone}) at {callback_time}"


# Define Agents
consultation_agent = Agent(
    role="Medical Consultation Coordinator",
    goal="Guide patients through medical consultations and help schedule appropriate doctor appointments",
    backstory="""You are an experienced medical consultation coordinator with deep knowledge of patient care 
    processes and medical services. You listen carefully to patient symptoms and concerns, ask clarifying questions, 
    and recommend appropriate medical services and doctor specialties.""",
    tools=[check_doctor_availability, schedule_callback],
    verbose=True,
    allow_delegation=False
)


appointment_agent = Agent(
    role="Appointment Booking Specialist",
    goal="Efficiently book and manage patient appointments with doctors and medical services",
    backstory="""You are a professional appointment scheduler with expertise in calendar management and 
    patient scheduling. You confirm patient availability, check doctor schedules, and book appointments 
    with attention to detail. You always provide confirmation numbers and send reminders.""",
    tools=[check_doctor_availability, book_appointment],
    verbose=True,
    allow_delegation=False
)


service_info_agent = Agent(
    role="Medical Services Information Specialist",
    goal="Provide comprehensive, accurate information about available medical services, procedures, and costs",
    backstory="""You are knowledgeable about all medical services offered, procedures, duration, costs, 
    and availability. You explain services clearly to patients, answer questions about benefits and 
    contraindications, and help patients choose the right services for their needs.""",
    tools=[get_service_info],
    verbose=True,
    allow_delegation=False
)


def create_call_center_crew(call_data: dict) -> Crew:
    """
    Create a dynamic crew based on the type of call
    
    Args:
        call_data: Dictionary containing call information including issue_type
        
    Returns:
        Crew object configured for the call type
    """
    issue_type = call_data.get("issue_type", "other")
    
    if issue_type == "consultation":
        tasks = [
            Task(
                description=f"Handle consultation request for patient: {call_data.get('patient_name', 'Unknown')}",
                agent=consultation_agent,
                expected_output="Consultation guidance and recommended next steps"
            )
        ]
        agents = [consultation_agent]
    elif issue_type == "appointment":
        tasks = [
            Task(
                description=f"Book appointment for patient: {call_data.get('patient_name', 'Unknown')} on {call_data.get('preferred_date', 'available date')}",
                agent=appointment_agent,
                expected_output="Appointment confirmation with details"
            )
        ]
        agents = [appointment_agent]
    elif issue_type == "service_info":
        tasks = [
            Task(
                description=f"Provide service information for patient inquiry: {call_data.get('description', 'general inquiry')}",
                agent=service_info_agent,
                expected_output="Detailed service information and recommendations"
            )
        ]
        agents = [service_info_agent]
    else:
        # Default: use consultation agent
        tasks = [
            Task(
                description=f"Handle general inquiry for patient: {call_data.get('patient_name', 'Unknown')}",
                agent=consultation_agent,
                expected_output="Guidance and recommended actions"
            )
        ]
        agents = [consultation_agent]
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
        memory=True,
        cache=True
    )
    
    return crew
