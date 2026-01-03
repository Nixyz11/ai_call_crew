# 🚀 AI Call Crew - Complete Setup Guide

## Step-by-Step Installation & Running Guide

This guide will walk you through everything needed to set up and run AI Call Crew on your local machine.

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **pip** (usually comes with Python)
- **A code editor** (VS Code, PyCharm, etc.)

### Verify your Python installation:
```bash
python --version
# Should show Python 3.8 or higher
```

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/Nixyz11/ai_call_crew.git
cd ai_call_crew
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn
- CrewAI & CrewAI-tools
- OpenAI
- And all other required dependencies

### Step 4: Create Environment File

Create a `.env` file in the project root:

#### On Windows (Command Prompt):
```bash
type nul > .env
```

#### On macOS/Linux (Terminal):
```bash
touch .env
```

### Step 5: Add OpenAI API Key

Open the `.env` file with a text editor and add:

```
OPENAI_API_KEY=your_actual_api_key_here
DEBUG=True
LOG_LEVEL=INFO
```

**Replace `your_actual_api_key_here` with your real OpenAI API key**

---

## Running the Application

### Start the Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

The application is now running!

---

## Testing the API

### Method 1: Interactive API Docs (Recommended)

1. Open your browser
2. Go to: `http://localhost:8000/docs`
3. You'll see the Swagger UI with all endpoints
4. Try the endpoints directly from the browser!

### Method 2: Using cURL

#### Health Check:
```bash
curl http://localhost:8000/health
```

#### Get Available Services:
```bash
curl http://localhost:8000/api/services
```

#### Process a Call:
```bash
curl -X POST http://localhost:8000/api/call/process \
  -H "Content-Type: application/json" \
  -d '{
    "patient_info": {
      "name": "John Doe",
      "phone_number": "+1-555-0100",
      "email": "john@example.com"
    },
    "issue_type": "consultation",
    "description": "I have been experiencing headaches for 3 days"
  }'
```

#### Book an Appointment:
```bash
curl -X POST http://localhost:8000/api/appointment \
  -H "Content-Type: application/json" \
  -d '{
    "patient_info": {
      "name": "Jane Smith",
      "phone_number": "+1-555-0101"
    },
    "service_type": "consultation",
    "preferred_date": "2024-01-15",
    "preferred_time": "14:00"
  }'
```

### Method 3: Using Python

Create a file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Test health check
print("Testing health check...")
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Test process call
print("\nTesting call processing...")
call_data = {
    "patient_info": {
        "name": "John Doe",
        "phone_number": "+1-555-0100"
    },
    "issue_type": "consultation",
    "description": "I have a headache"
}
response = requests.post(f"{BASE_URL}/api/call/process", json=call_data)
print(json.dumps(response.json(), indent=2))

# Get services
print("\nGetting available services...")
response = requests.get(f"{BASE_URL}/api/services")
print(json.dumps(response.json(), indent=2))
```

Run it:
```bash
python test_api.py
```

---

## Project Structure Explanation

```
ai_call_crew/
├── backend/
│   └── app/
│       ├── __init__.py                    # Package init
│       ├── main.py                        # FastAPI application
│       ├── models.py                      # Data models (Pydantic)
│       ├── config.py                      # Configuration
│       └── agents/
│           ├── __init__.py
│           └── call_center_crew.py        # CrewAI agents
├── requirements.txt                       # Dependencies
├── .gitignore
├── README.md                              # Project overview
├── SETUP.md                               # This file
└── .env                                   # Your API keys (create this)
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Virtual environment not activated or dependencies not installed

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not found"

**Solution:** Add API key to `.env` file

```bash
# Create .env file with your API key
echo OPENAI_API_KEY=your_key_here > .env
```

### Issue: "Address already in use: ('127.0.0.1', 8000)"

**Solution:** Another service is using port 8000

```bash
# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

### Issue: "Connection refused" when testing API

**Solution:** Make sure the server is running

1. Check that you ran: `python -m uvicorn app.main:app --reload`
2. Check that the URL is correct: `http://localhost:8000`
3. Server should show "Uvicorn running on..."

---

## Useful Commands

### Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Deactivate virtual environment
```bash
deactivate
```

### Install new package
```bash
pip install package-name
```

### Update requirements.txt
```bash
pip freeze > requirements.txt
```

### Run server in production mode
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Run with custom workers
```bash
python -m uvicorn app.main:app --workers 4 --port 8000
```

---

## Next Steps

After setup:

1. **Explore the API** - Visit `http://localhost:8000/docs`
2. **Test the Agents** - Use the endpoints to test CrewAI agents
3. **Customize** - Edit `backend/app/config.py` to customize settings
4. **Add More Agents** - Extend `backend/app/agents/call_center_crew.py`
5. **Integrate** - Connect with your medical system

---

## Getting Help

- Check the [README.md](README.md) for project overview
- Review the [CrewAI documentation](https://docs.crewai.com/)
- Check [FastAPI documentation](https://fastapi.tiangolo.com/)
- Open an issue on GitHub for bugs

---

## Quick Reference

| Task | Command |
|------|----------|
| Clone repo | `git clone https://github.com/Nixyz11/ai_call_crew.git` |
| Create venv | `python -m venv venv` |
| Activate venv | `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows) |
| Install deps | `pip install -r requirements.txt` |
| Run server | `cd backend && python -m uvicorn app.main:app --reload` |
| API Docs | `http://localhost:8000/docs` |
| Health check | `curl http://localhost:8000/health` |

---

<div align="center">
  <p><strong>You're all set! Happy developing! 🚀</strong></p>
</div>
