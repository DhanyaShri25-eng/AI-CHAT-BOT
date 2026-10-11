# BuildWise AI 🏗️📐

### AI-Powered Building Design, Architecture, Construction Cost Estimation & Project Planning Platform

BuildWise AI is an enterprise-grade full-stack conversational AI platform designed specifically for building construction, architectural space planning, deterministic IS 456 material quantity calculation, itemized construction budgeting, and Critical Path Method (CPM) project scheduling.

---

## 🌟 Key Capabilities

1. **Interactive 2D Architecture Studio:**
   - Parametric geometric setback calculation (Front, Rear, Side setbacks according to TNCDBR 2019 / NBC 2016).
   - Usable building footprint determination.
   - Vastu Shastra zone alignment (Kitchen in South-East Agni corner, Master Bedroom in South-West Nairuthi corner, Pooja/Entrance in North-East).
   - Scaled blueprint SVG generation with doors, windows, dimensions, and room inspection.
   - Architectural front elevation concept SVG with plinth, floor levels, glazing, and parapet details.

2. **Deterministic Construction Material Takeoff (BOQ):**
   - Grounded in **IS 456:2000** (Plain and Reinforced Concrete), **IS 1200** (Methods of Measurement), and **IS 383** (Fine & Coarse Aggregate).
   - Accurate quantities for:
     - Cement (OPC 53 structural grade & PPC for masonry/plastering)
     - Fe 500D / 550D TMT Steel Rebar (kg and metric tons with footing/column/beam/slab distribution)
     - Manufactured Fine Aggregate (M-Sand Zone II)
     - Coarse Aggregate (20mm & 12mm Blue Metal)
     - AAC Lightweight Blocks / Red Clay Wire-Cut Bricks
     - Vitrified flooring and ceramic wall dado tiles
     - Wall putty, primer, and washable acrylic emulsions
     - Integral and membrane waterproofing
     - Electrical modular conduits, wiring runs & DBs
     - Plumbing CPVC/PVC lines and sanitary ware
   - Factored engineering wastage allowances (3–10%).

3. **Itemized Construction Cost Engine:**
   - Regional South India & Indian metro price benchmarks (Q3 2026 verified rates).
   - Itemized breakdown: Civil Materials, Labour Wages, Machinery & Transport, Architectural/Structural Fees, Municipal Approvals & EB deposits, GST, and Contingency Reserve (6%).
   - Multi-tier estimates: **Low**, **Expected**, and **High** ranges.
   - Economy vs. Standard vs. Standard Premium vs. Luxury tier comparison.

4. **Critical Path Method (CPM) Construction Scheduling:**
   - 15 execution gates across 9 construction phases.
   - Task predecessor dependencies, early start, early finish, and critical path highlighting.
   - Interactive Gantt chart timeline with task status tracking.
   - Weather and monsoon buffer risk assessments.

5. **Voice-Enabled Multilingual AI Chat:**
   - Microphone voice input with animated audio visualizer waves.
   - Full support for **English**, **Tamil (தமிழ்)**, and **Tanglish** (e.g., *"30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs"*).
   - Editable parameter confirmation before executing calculations.
   - Browser Text-To-Speech (TTS) audio playback.
   - Multi-turn conversation history with collapsible sidebar.

6. **Verified Building By-Law Knowledge Retrieval (RAG):**
   - Grounded citations from **NBC 2016**, **TNCDBR 2019**, and **IS 456**.
   - Setbacks, Floor Space Index (FSI), rainwater harvesting mandates, and minimum room dimensions.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 16)                    │
│   • Blueprint Design System & Tailwind CSS                  │
│   • Interactive 2D Floor Plan SVG Canvas                    │
│   • Architectural Front Elevation Concept Viewer            │
│   • Cost Breakdown & BOQ Data Visualizer                    │
│   • CPM Gantt Timeline Visualizer                           │
│   • Real-Time Microphone Recorder & Tanglish Preview        │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / REST / SSE Stream
┌──────────────────────────────▼──────────────────────────────┐
│                  Backend (Python FastAPI)                   │
│   • Pydantic Request & Response Validation                  │
│   • SQLAlchemy Async ORM (SQLite / PostgreSQL)              │
│   • JWT Authentication & Session Management                 │
├─────────────────────────────────────────────────────────────┤
│                    Core Engine Modules                      │
│   ├── Architecture & Floor-Plan Geometry Engine             │
│   ├── IS 456 Deterministic Material Takeoff Engine          │
│   ├── Price & Regional Benchmark Cost Engine                │
│   ├── Critical Path Method (CPM) Scheduling Engine          │
│   ├── Verified Regulatory RAG (NBC / TNCDBR / IS Codes)     │
│   └── Whisper Voice Transcription & Speech Engine           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ (Tested on Node v24)
- npm 9+

### 1. Backend Setup & Startup

```bash
cd backend

# Create environment file
copy .env.example .env

# Run FastAPI server
python run.py
```
*The backend API will be available at `http://localhost:8000`. You can inspect the interactive OpenAPI documentation at `http://localhost:8000/docs`.*

### 2. Frontend Setup & Startup

```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Start Next.js development server
npm run dev
```
*The frontend application will be running at `http://localhost:3000`.*

---

## 🧪 Running Automated Tests

Run the unit and calculation test suite to verify IS 456 engineering quantity thumb-rules, setback geometry, and Tanglish NLP parameter extraction:

```bash
python -m pytest backend/tests/test_engines.py -v
```

Output:
```
backend/tests/test_engines.py::test_floorplan_engine PASSED
backend/tests/test_engines.py::test_calculation_engine PASSED
backend/tests/test_engines.py::test_pricing_engine PASSED
backend/tests/test_engines.py::test_schedule_engine PASSED
backend/tests/test_engines.py::test_voice_parameter_extraction PASSED
backend/tests/test_engines.py::test_rag_service PASSED
======================== 6 passed in 0.05s =========================
```

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health and engine operational status |
| `POST` | `/api/auth/register` | User registration |
| `POST` | `/api/auth/login` | User login & JWT issuance |
| `GET` | `/api/conversations` | List conversation history |
| `POST` | `/api/chat` | Multi-turn conversational engineering assistant |
| `POST` | `/api/chat/stream` | Server-Sent Events (SSE) token stream |
| `POST` | `/api/voice/transcribe` | Whisper audio transcription with Tanglish parsing |
| `POST` | `/api/voice/speak` | Text-to-speech synthesis endpoint |
| `POST` | `/api/designs/generate` | Generates 2D floor plan geometry and SVG blueprint |
| `POST` | `/api/designs/{id}/revise` | Parametric revision of floor plan layout |
| `POST` | `/api/estimates/calculate` | Computes itemized construction cost & BOQ quantities |
| `POST` | `/api/estimates/compare` | Multi-tier cost comparisons (Economy, Standard, Luxury) |
| `GET` | `/api/materials` | Verified building material catalog |
| `POST` | `/api/prices/quotations` | Submits verified supplier price quotation |
| `POST` | `/api/schedules/generate` | Generates CPM Gantt construction schedule |
| `POST` | `/api/documents/search` | RAG search over NBC 2016 and TNCDBR 2019 regulations |

---

## 🛠️ Customizing the AI Model

BuildWise AI supports plug-and-play LLM engines configured via `.env`:
- **`built-in`**: Autonomous expert civil engineering reasoning agent with deterministic tool execution (default).
- **`ollama`**: Connect to a local Ollama instance (e.g. `llama3:8b`, `qwen2.5:7b`).
- **`openai-compatible` / `vLLM`**: Connect to any OpenAI-compatible remote inference server.
- **`gemini` / `groq`**: Fast cloud inference models.

---

## 📜 Disclaimer
*BuildWise AI provides conceptual architectural layouts, mathematical quantity takeoff estimates, and baseline planning schedules. Actual site construction drawings and structural reinforcement details must be reviewed and certified by a registered Architect and licensed Structural Engineer in accordance with local municipal regulations.*
