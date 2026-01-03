# 🚀 AI Call Crew - Local Models Setup (Ollama + Hugging Face)

## Using Ollama & Hugging Face Instead of OpenAI

This guide shows how to run AI Call Crew with **local Ollama models** and **Hugging Face models** - no OpenAI API needed!

---

## Prerequisites

### Install Ollama

1. **Download Ollama** from https://ollama.ai/
2. **Install** for your OS (Windows, macOS, Linux)
3. **Verify installation:**
   ```bash
   ollama --version
   ```

### Pull a Model

Pull a local model from Ollama:

```bash
# Pull Llama 2 (powerful, 7B parameters)
ollama pull llama2

# Or pull Mistral (faster, 7B parameters)
ollama pull mistral

# Or pull Neural Chat (optimized, 7B parameters)
ollama pull neural-chat

# Or pull Dolphin (creative, 7B parameters)
ollama pull dolphin-mixtral
```

**List all pulled models:**
```bash
ollama list
```

---

## Step 1: Start Ollama Server

Before running your app, start the Ollama server:

### On macOS/Linux:
```bash
ollama serve
```

### On Windows:
Ollama runs as a background service automatically. Verify it's running by:
```bash
curl http://localhost:11434
```

**Expected output:** Ollama is now running on `http://localhost:11434`

---

## Step 2: Install AI Call Crew

```bash
git clone https://github.com/Nixyz11/ai_call_crew.git
cd ai_call_crew

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install additional local model support
pip install ollama langchain-ollama transformers
```

---

## Step 3: Create .env File

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

Add to `.env`:
```
# Ollama Configuration
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
LLM_TYPE=ollama

# Alternative: Use HuggingFace models
# LLM_TYPE=huggingface
# HF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
# HF_API_KEY=your_huggingface_token_here (optional)

DEBUG=True
LOG_LEVEL=INFO
```

---

## Step 4: Update Configuration (config.py)

Navigate to `backend/app/config.py` and update:

**Replace this:**
```python
LLM_MODEL: str = "gpt-4"
OPENAI_API_KEY: Optional[str] = None
```

**With this for Ollama:**
```python
LLM_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_TYPE: str = os.getenv("LLM_TYPE", "ollama")
OPENAI_API_KEY: Optional[str] = None  # Not needed for Ollama
```

---

## Step 5: Update Agents to Use Local Models

Create/Update `backend/app/agents/call_center_crew.py` to use Ollama:

**Replace the imports section with:**
```python
from crewai import Agent, Task, Crew
from crewai_tools import tool
from langchain_ollama import OllamaLLM
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

# Initialize Ollama LLM
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

llm = OllamaLLM(
    model=ollama_model,
    base_url=ollama_base_url,
    temperature=0.7
)
```

**Then update agent definitions:**
```python
consultation_agent = Agent(
    role="Medical Consultation Coordinator",
    goal="Guide patients through medical consultations and help schedule appropriate doctor appointments",
    backstory="""You are an experienced medical consultation coordinator with deep knowledge of patient care 
    processes and medical services. You listen carefully to patient symptoms and concerns, ask clarifying questions, 
    and recommend appropriate medical services and doctor specialties.""",
    tools=[check_doctor_availability, schedule_callback],
    llm=llm,  # Add this line
    verbose=True,
    allow_delegation=False
)

# Do the same for appointment_agent and service_info_agent
```

---

## Step 6: Run the Application

**Make sure Ollama server is running first!**

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Application startup complete
```

---

## Testing with Local Models

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

### Test 2: Process a Call (with Ollama)
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
    "description": "I have a headache"
  }'
```

### Test 3: Interactive Docs
```
http://localhost:8000/docs
```

---

## Alternative: Using Hugging Face Models

If you prefer Hugging Face models instead of Ollama:

### Install HuggingFace Support
```bash
pip install transformers torch huggingface-hub
```

### Update .env
```
LLM_TYPE=huggingface
HF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.1
HF_API_KEY=hf_your_token_here  # Get from https://huggingface.co/settings/tokens
```

### Update agents/call_center_crew.py
```python
from transformers import pipeline
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

# Initialize HuggingFace LLM
hf_model = os.getenv("HF_MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")

llm = HuggingFacePipeline(
    model_id=hf_model,
    task="text-generation",
    device=0  # GPU device (0 for first GPU, -1 for CPU)
)
```

---

## Recommended Ollama Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama2** | 7B | Fast | Good | General purpose |
| **mistral** | 7B | Very Fast | Very Good | Balanced speed/quality |
| **neural-chat** | 7B | Fast | Good | Conversational |
| **dolphin-mixtral** | 46B | Slow | Excellent | Complex reasoning |
| **orca-mini** | 3B | Very Fast | OK | Low resource |

**Choose based on your hardware:**
- **8GB RAM:** Use orca-mini or mistral
- **16GB RAM:** Use llama2 or mistral (best choice)
- **32GB+ RAM:** Use dolphin-mixtral or larger models

---

## Recommended Hugging Face Models

```bash
# Fast & Efficient
mistralai/Mistral-7B-Instruct-v0.1

# Creative & Detailed
meta-llama/Llama-2-7b-chat-hf

# Small & Fast
PygmalionAI/pygmalion-2-7b

# Medical Focused
StanfordAIMI/stanford-crft-vec-base-v2
```

---

## Troubleshooting

### Issue: "Connection refused" on localhost:11434

**Solution:** Make sure Ollama server is running

```bash
# Windows: Should run automatically
# macOS/Linux:
ollama serve
```

### Issue: Model not found

**Solution:** Pull the model first

```bash
ollama pull llama2
ollama pull mistral  # or any other model
ollama list  # Check installed models
```

### Issue: "Out of memory" or "CUDA out of memory"

**Solution:** Use a smaller model

```bash
ollama pull orca-mini  # 3B - lightweight
# Then update .env:
# OLLAMA_MODEL=orca-mini
```

### Issue: Model is very slow

**Solution:** 
- Use a faster model (mistral instead of llama2)
- Run on GPU instead of CPU
- Use smaller model (7B instead of 13B)

### Issue: HuggingFace model won't load

**Solution:** Check your token and model name

```bash
# Set HF token
huggingface-cli login
# Enter your token from https://huggingface.co/settings/tokens
```

---

## Performance Tips

### For Faster Response:
1. Use **mistral** model (faster than llama2)
2. Reduce temperature: `temperature=0.3`
3. Set max tokens: `max_tokens=256`
4. Use GPU: Ensure CUDA/Metal is enabled

### For Better Responses:
1. Use **llama2** or **dolphin-mixtral**
2. Increase temperature: `temperature=0.8`
3. Allow more tokens: `max_tokens=512`
4. More detailed prompts

### Memory Optimization:
1. Enable quantization in Ollama
2. Use smaller models (7B)
3. Set context window smaller

---

## Complete Quick Reference

```bash
# 1. Start Ollama
ollama serve

# 2. (In another terminal) Pull model
ollama pull llama2

# 3. Clone and setup
git clone https://github.com/Nixyz11/ai_call_crew.git
cd ai_call_crew
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 4. Install dependencies
pip install -r requirements.txt
pip install ollama langchain-ollama

# 5. Create .env
echo OLLAMA_MODEL=llama2 > .env
echo OLLAMA_BASE_URL=http://localhost:11434 >> .env
echo LLM_TYPE=ollama >> .env

# 6. Run application
cd backend
python -m uvicorn app.main:app --reload

# 7. Test
curl http://localhost:8000/health

# 8. Open browser
# http://localhost:8000/docs
```

---

## Available Ollama Models

See all available models:
```bash
ollama list  # Local models
curl http://localhost:11434/api/tags  # API endpoint
```

Or visit: https://ollama.ai/library

---

<div align="center">
  <p><strong>Running AI Call Crew locally - no API keys needed! 🚀</strong></p>
</div>
