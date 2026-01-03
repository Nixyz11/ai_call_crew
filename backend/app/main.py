"""FastAPI application for AI Call Center Assistant with conversation memory"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
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

conversation_history: Dict[str, List[Dict[str, str]]] = {}

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

def extract_specialty(description: str) -> str:
    description_lower = description.lower() if description else ""
    
    specialties = {
        "cardiology": ["heart", "cardiac", "cardiologist", "chest pain", "heart disease"],
        "gastroenterology": ["stomach", "digestive", "abdominal", "gut", "gastro"],
        "neurology": ["headache", "migraine", "brain", "neurologist", "headaches"],
        "orthopedics": ["bone", "joint", "fracture", "arthritis", "knee", "back pain"],
        "general": ["appointment", "consultation", "checkup", "visit"]
    }
    
    for specialty, keywords in specialties.items():
        if any(keyword in description_lower for keyword in keywords):
            return specialty
    return "general"

def get_conversation_context(session_id: str) -> str:
    history = conversation_history.get(session_id, [])
    if len(history) <= 1:
        return "(first message in conversation)"
    context = "Previous messages in this conversation:\n"
    for msg in history[-4:-1]:  # Last 3 messages
        context += f"- Patient: {msg.get('user', '')}\n- Agent: {msg.get('agent', '')}\n"
    return context

def generate_smart_response(patient_name: str, description: str, specialty: str, session_id: str) -> str:
    context = get_conversation_context(session_id)
    history = conversation_history.get(session_id, [])
    
    patient_name = patient_name.strip() if patient_name else "there"
    
    if specialty == "cardiology":
        if "appointment" in description.lower() or "book" in description.lower():
            return f"Thank you {patient_name}. I understand you want to book a cardiology appointment. We have experienced cardiologists available. Would you prefer a morning, afternoon, or evening appointment? Also, do you have any specific dates in mind?"
        else:
            return f"Thank you {patient_name}. I understand you're experiencing heart-related issues. This requires a cardiologist's evaluation. I can help you schedule an appointment with our cardiology specialist. When would be the best time for you to visit?"
    
    elif specialty == "gastroenterology":
        if "appointment" in description.lower() or "book" in description.lower():
            return f"Thank you {patient_name}. I'll help you book an appointment with our gastroenterologist. We have available slots next week. Would you prefer morning or afternoon? Any particular days that work best for you?"
        else:
            return f"Thank you {patient_name}. Digestive issues require proper evaluation by a specialist. I recommend scheduling a consultation with our gastroenterologist. They can provide a comprehensive assessment and treatment plan. Would you like to book an appointment?"
    
    elif specialty == "neurology":
        if "appointment" in description.lower() or "book" in description.lower():
            return f"Thank you {patient_name}. Our neurologists have several availability slots. Would you prefer this week or next week? What time of day works best for you?"
        else:
            return f"Thank you {patient_name}. Neurological concerns should be evaluated by a specialist. I can connect you with our experienced neurologist. They can help diagnose and treat your condition. Shall we schedule an appointment?"
    
    elif specialty == "orthopedics":
        if "appointment" in description.lower() or "book" in description.lower():
            return f"Thank you {patient_name}. Our orthopedic specialists are available for appointments. We have slots available Tuesday through Saturday. Which day suits you best?"
        else:
            return f"Thank you {patient_name}. Bone and joint issues require professional orthopedic care. I can help you schedule an evaluation with our orthopedic specialist. They'll assess your condition and recommend treatment. Would you like to proceed with booking?"
    
    else:
        if len(history) > 1:
            return f"Thank you {patient_name}. Based on what you've shared, I recommend booking a general consultation. Our doctors can assess your condition and refer you to a specialist if needed. Are you interested in scheduling an appointment this week?"
        else:
            return f"Hello {patient_name}! Thank you for contacting us. I'm here to help you with your medical needs. Could you tell me more about what brings you in today?"

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
        session_id = call_request.phone_number
        logger.info(f"Processing call from {call_request.patient_name}")
        
        specialty = extract_specialty(call_request.description or "")
        response_text = generate_smart_response(
            patient_name=call_request.patient_name,
            description=call_request.description or "",
            specialty=specialty,
            session_id=session_id
        )
        
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        conversation_history[session_id].append({
            "user": call_request.description,
            "agent": response_text
        })
        
        next_steps = []
        if "appointment" in response_text.lower():
            next_steps = ["Choose preferred appointment time", "Confirm specialist preference", "Receive appointment confirmation"]
        else:
            next_steps = ["Provide more details if needed", "Proceed to book appointment", "Receive appointment confirmation"]
        
        response = CallResponse(
            call_id=f"CALL-{hash(session_id)}",
            status="processed",
            assistant_response=response_text,
            next_steps=next_steps
        )
        return response
    except Exception as e:
        logger.error(f"Error processing call: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing call")

@app.get("/api/services")
async def get_services():
    services = [
        {"id": "1", "name": "Cardiology", "duration": "45 mins"},
        {"id": "2", "name": "Gastroenterology", "duration": "45 mins"},
        {"id": "3", "name": "Neurology", "duration": "45 mins"},
        {"id": "4", "name": "Orthopedics", "duration": "45 mins"},
        {"id": "5", "name": "General Consultation", "duration": "30 mins"},
    ]
    return {"services": services}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
