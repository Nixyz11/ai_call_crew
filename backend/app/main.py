"""FastAPI application for AI Call Center Assistant"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Call Crew - Medical Call Center Assistant",
    description="CrewAI-powered call center assistant for medical institutions",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CallRequest(BaseModel):
    patient_name: str
    phone_number: str
    issue_type: str
    description: Optional[str] = None
    preferred_date: Optional[str] = None

class CallResponse(BaseModel):
    call_id: str
    status: str
    assistant_response: str
    next_steps: Optional[List[str]] = None

def generate_response(patient_name: str, description: str, issue_type: str) -> str:
    response = f"Thank you {patient_name or 'there'}. I understand you're experiencing issues with your {issue_type}. "
    description_lower = description.lower() if description else ""
    
    if "headache" in description_lower or "head pain" in description_lower:
        response += "Headaches can be quite uncomfortable. I can help you explore potential causes and solutions. Can you tell me if it's a throbbing pain, pressure, or sharp pain? Also, how long have you been experiencing this?"
    elif "stomach" in description_lower or "abdominal" in description_lower or "digestive" in description_lower:
        response += "Stomach and digestive issues can be concerning. I'm here to help. Can you describe the type of discomfort - is it cramping, nausea, bloating, or pain? When did it start?"
    elif "appointment" in description_lower or "available" in description_lower or "schedule" in description_lower:
        response += "I can help you check available appointment times. We have various services available at different times. What type of service are you interested in - a general consultation, specialist visit, or diagnostic procedure?"
    elif "service" in description_lower or "what do you offer" in description_lower:
        response += "We offer comprehensive medical services including consultations, diagnostic procedures, and specialist appointments. What specific service interests you? Would you like information about our cardiology, gastroenterology services, or ultrasound diagnostics?"
    elif "pain" in description_lower or "ache" in description_lower:
        response += "Pain and discomfort should be evaluated properly. Can you tell me where the pain is located and how long you've had it? This will help me guide you to the right service."
    elif "symptoms" in description_lower or "sick" in description_lower or "ill" in description_lower:
        response += "I'm sorry to hear you're not feeling well. Can you describe your main symptoms? This will help me better understand how to assist you."
    else:
        response += f"I'm here to help with your {issue_type} concerns. Can you provide more details about what you're experiencing so I can better assist you?"
    
    response += " How can I help you further?"
    return response

@app.get("/")
async def root():
    return {
        "message": "AI Call Crew - Medical Call Center Assistant",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/call/process")
async def process_call(call_request: CallRequest) -> CallResponse:
    try:
        logger.info(f"Processing call from {call_request.patient_name}")
        response_text = generate_response(
            patient_name=call_request.patient_name,
            description=call_request.description,
            issue_type=call_request.issue_type
        )
        response = CallResponse(
            call_id=f"CALL-{hash(call_request.patient_name)}",
            status="processed",
            assistant_response=response_text,
            next_steps=["Wait for additional guidance", "Feel free to ask more questions"]
        )
        return response
    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing call")

@app.post("/api/consultation")
async def handle_consultation(call_request: CallRequest) -> CallResponse:
    try:
        return CallResponse(
            call_id=f"CONSULT-{hash(call_request.patient_name)}",
            status="consultation_initiated",
            assistant_response="Doctor consultation has been scheduled.",
            next_steps=["Confirm appointment details", "Receive confirmation SMS"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error handling consultation")

@app.post("/api/appointment")
async def book_appointment(call_request: CallRequest) -> CallResponse:
    try:
        return CallResponse(
            call_id=f"APT-{hash(call_request.patient_name)}",
            status="appointment_booked",
            assistant_response=f"Your appointment has been scheduled for {call_request.preferred_date}.",
            next_steps=["Save confirmation number", "Receive appointment reminder"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error booking appointment")

@app.get("/api/services")
async def get_services():
    services = [
        {"id": "1", "name": "General Consultation", "duration": "30 mins"},
        {"id": "2", "name": "Dental Checkup", "duration": "45 mins"},
        {"id": "3", "name": "Lab Tests", "duration": "15 mins"},
        {"id": "4", "name": "Follow-up Visit", "duration": "20 mins"},
    ]
    return {"services": services}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
