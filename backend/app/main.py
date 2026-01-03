"""FastAPI application for AI Call Center Assistant"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Call Crew - Medical Call Center Assistant",
    description="CrewAI-powered call center assistant for medical institutions",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class CallRequest(BaseModel):
    """Model for incoming call requests"""
    patient_name: str
    phone_number: str
    issue_type: str  # consultation, appointment, service_info, other
    description: Optional[str] = None
    preferred_date: Optional[str] = None

class CallResponse(BaseModel):
    """Model for call response"""
    call_id: str
    status: str
    assistant_response: str
    next_steps: Optional[List[str]] = None

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Call Crew - Medical Call Center Assistant",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/call/process")
async def process_call(call_request: CallRequest) -> CallResponse:
    """
    Process an incoming call from a patient
    
    Args:
        call_request: Call request with patient info and issue type
    
    Returns:
        CallResponse with assistant's response and next steps
    """
    try:
        logger.info(f"Processing call from {call_request.patient_name}")
        
        # TODO: Integrate with CrewAI agents
        # Process call based on issue type
        
        response = CallResponse(
            call_id=f"CALL-{hash(call_request.patient_name)}" ,
            status="processed",
            assistant_response=f"Thank you {call_request.patient_name}. I will assist you with your {call_request.issue_type}.",
            next_steps=["Wait for agent response", "Provide additional info if needed"]
        )
        
        return response
    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing call")

@app.post("/api/consultation")
async def handle_consultation(call_request: CallRequest) -> CallResponse:
    """Handle patient consultation requests"""
    try:
        # TODO: Route to consultation agent
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
    """Handle appointment booking requests"""
    try:
        # TODO: Route to appointment booking agent
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
    """Get available medical services"""
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
