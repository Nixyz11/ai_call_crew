# AI Call Crew

<div align="center">
  <h3>CrewAI-Powered Call Center Assistant for Medical Institutions</h3>
  <p><strong>Intelligent Multi-Agent System for Patient Consultations, Appointments & Services</strong></p>
</div>

## 🎯 Overview

**AI Call Crew** is an advanced multi-agent AI system powered by CrewAI that handles incoming calls in medical institutions. It intelligently routes patient inquiries, provides medical information, schedules appointments, and guides patients through the consultation process.

The system uses specialized AI agents that work collaboratively to deliver a seamless patient experience while reducing call center workload and improving efficiency.

## ✨ Key Features

- **Multi-Agent Collaboration** - Specialized agents for consultations, appointments, and service information
- **Intelligent Call Routing** - Automatic routing based on patient inquiry type
- **Appointment Management** - Smart scheduling with doctor availability checking
- **Service Information** - Comprehensive details about medical services and procedures
- **Patient Consultation** - Guided consultations to understand patient needs
- **RESTful API** - Easy integration with existing systems
- **Scalable Architecture** - Built with FastAPI for high-performance async handling

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                     │
├─────────────────────────────────────────────────────┤
│  /api/call/process  /api/consultation  /api/appointment │
├─────────────────────────────────────────────────────┤
│           CrewAI Multi-Agent System                 │
├──────────────┬───────────────┬──────────────────────┤
│  Consultation│  Appointment  │  Service Information │
│   Agent      │   Agent       │      Agent           │
├──────────────┴───────────────┴──────────────────────┤
│    Tools: Doctor Availability, Booking, Services   │
└─────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
ai_call_crew/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic data models
│   │   ├── config.py            # Configuration settings
│   │   └── agents/
│   │       ├── __init__.py
│   │       └── call_center_crew.py  # CrewAI agents
│   └── requirements.txt         # Dependencies
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or poetry
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nixyz11/ai_call_crew.git
   cd ai_call_crew
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 🧠 Agents

### 1. Consultation Coordinator Agent
- **Role**: Medical Consultation Expert
- **Goal**: Guide patients through consultations and help schedule doctor appointments
- **Capabilities**:
  - Listen to patient symptoms and concerns
  - Ask clarifying questions
  - Recommend appropriate medical services
  - Schedule callbacks if needed

### 2. Appointment Booking Agent
- **Role**: Appointment Scheduler
- **Goal**: Efficiently book and manage patient appointments
- **Capabilities**:
  - Check doctor availability
  - Book appointments with selected doctors
  - Provide confirmation numbers
  - Send appointment reminders

### 3. Service Information Agent
- **Role**: Medical Services Expert
- **Goal**: Provide comprehensive information about medical services
- **Capabilities**:
  - Explain medical procedures
  - Discuss costs and duration
  - Answer service-related questions
  - Help patients choose appropriate services

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Process Call
```bash
POST /api/call/process
Content-Type: application/json

{
  "patient_info": {
    "name": "John Doe",
    "phone_number": "+1-555-0100",
    "email": "john@example.com"
  },
  "issue_type": "consultation",
  "description": "I have been experiencing headaches",
  "special_notes": "Prefer morning appointments"
}
```

### Book Appointment
```bash
POST /api/appointment
Content-Type: application/json

{
  "patient_info": {
    "name": "Jane Smith",
    "phone_number": "+1-555-0101"
  },
  "service_type": "consultation",
  "preferred_date": "2024-01-15",
  "preferred_time": "14:00"
}
```

### Get Services
```bash
GET /api/services
```

## ⚙️ Configuration

Edit `backend/app/config.py` to customize:
- LLM model (default: GPT-4)
- Temperature settings
- Max concurrent calls
- Call timeout duration
- Logging levels

## 🛠️ Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **CrewAI** - Multi-agent orchestration
- **OpenAI** - LLM provider
- **LangChain** - LLM utilities
- **SQLAlchemy** - Database ORM
- **Loguru** - Advanced logging

## 🔄 Workflow Example

1. Patient calls the medical institution
2. System receives call with patient info and issue type
3. Appropriate CrewAI agent is selected
4. Agent processes the call using specialized tools
5. Patient receives guidance, appointment booking, or service information
6. Confirmation and next steps are provided

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📝 API Models

### CallRequest
- `patient_info`: PatientInfo
- `issue_type`: Enum (consultation, appointment, service_info, follow_up, billing, other)
- `description`: Optional string
- `preferred_date`: Optional string
- `preferred_time`: Optional string

### CallResponse
- `call_id`: str
- `status`: str
- `assistant_response`: str
- `next_steps`: List[str]
- `scheduled_callback_time`: Optional string
- `appointment_id`: Optional string

## 🚀 Deployment

### Docker
```bash
docker build -t ai_call_crew .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai_call_crew
```

### Production
For production deployment, use:
- Gunicorn with multiple workers
- Nginx as reverse proxy
- PostgreSQL for data persistence
- Redis for caching

## 📚 Documentation

- [FastAPI Docs](http://localhost:8000/docs) - Interactive API documentation
- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Luka Cerovic**  
Full-Stack Developer & AI Enthusiast  
Serbia

## 🙏 Acknowledgments

- CrewAI for the amazing multi-agent framework
- OpenAI for powerful language models
- FastAPI community for the excellent web framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the code examples

---

<div align="center">
  <p><strong>Made with ❤️ for medical institutions</strong></p>
  <p>⭐ Star us on GitHub if you find this helpful!</p>
</div>
