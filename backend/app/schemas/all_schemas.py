from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

# --- AUTH SCHEMAS ---
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = "BuildWise User"
    role: Optional[str] = "homeowner"
    phone: Optional[str] = None
    location: Optional[str] = "Tamil Nadu, India"

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserProfileOut(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    role: str
    phone: Optional[str]
    location: Optional[str]
    company_name: Optional[str]
    created_at: datetime

# --- PROJECT SCHEMAS ---
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    building_type: Optional[str] = "2BHK Residential"
    location: Optional[str] = "Chennai, Tamil Nadu"
    plot_length: float = 40.0
    plot_width: float = 30.0
    plot_area: Optional[float] = None
    plot_area_unit: Optional[str] = "sqft"
    built_up_area: Optional[float] = None
    floors: int = 2
    target_budget: Optional[float] = 4500000.0

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    building_type: Optional[str] = None
    plot_length: Optional[float] = None
    plot_width: Optional[float] = None
    built_up_area: Optional[float] = None
    floors: Optional[int] = None
    target_budget: Optional[float] = None
    current_stage: Optional[str] = None

class ProjectOut(BaseModel):
    id: str
    name: str
    description: Optional[str]
    building_type: str
    location: str
    plot_length: float
    plot_width: float
    plot_area: float
    plot_area_unit: str
    built_up_area: float
    floors: int
    rooms: int
    target_budget: float
    current_stage: str
    created_at: datetime
    updated_at: datetime

# --- ARCHITECTURE & FLOOR PLAN SCHEMAS ---
class FloorPlanGenerateRequest(BaseModel):
    project_id: Optional[str] = None
    building_type: str = "2BHK" # 1BHK, 2BHK, 3BHK, 4BHK, Duplex
    plot_length: float = 40.0
    plot_width: float = 30.0
    orientation: str = "North" # North, East, South, West
    floors: int = 1
    architectural_style: str = "Modern" # Modern, Minimalist, Traditional Chettinad, Kerala Vernacular
    setback_front: Optional[float] = 5.0
    setback_rear: Optional[float] = 3.0
    setback_sides: Optional[float] = 3.0
    custom_rooms: Optional[List[Dict[str, Any]]] = None

class FloorPlanRoomOut(BaseModel):
    id: Optional[str] = None
    floor_level: int = 0
    name: str
    room_type: str
    x: float
    y: float
    width: float
    length: float
    area_sqft: float
    orientation: Optional[str] = None
    doors: List[Dict[str, Any]] = []
    windows: List[Dict[str, Any]] = []

class DesignVersionOut(BaseModel):
    id: str
    project_id: Optional[str] = None
    version_number: int
    title: str
    description: Optional[str]
    total_area_sqft: float
    ground_floor_area: float
    first_floor_area: float
    style: str
    plot_boundary: Dict[str, Any]
    rooms: List[FloorPlanRoomOut]
    elevation_data: Optional[Dict[str, Any]] = None
    svg_data: Optional[str] = None
    created_at: Optional[datetime] = None

# --- MATERIAL CALCULATION SCHEMAS ---
class MaterialCalculateRequest(BaseModel):
    project_id: Optional[str] = None
    built_up_area: float = 1800.0 # sq ft
    floors: int = 2
    foundation_type: str = "Isolated Column Footing" # Isolated, Pile, Raft
    structure_type: str = "RCC Framed Structure" # RCC Framed, Load Bearing
    wall_type: str = "AAC Lightweight Blocks" # Red Clay Bricks, AAC Lightweight Blocks, Solid Fly Ash Bricks
    plaster_type: str = "Cement Sand Mortar 1:6"
    flooring_type: str = "Vitrified Tiles (800x800mm)"
    construction_quality: str = "Standard Premium" # Economy, Standard, Premium, Luxury

class MaterialItemOut(BaseModel):
    name: str
    category: str
    estimated_quantity: float
    wastage_percent: float
    procurement_quantity: float
    unit: str
    unit_price: float
    total_cost: float
    calculation_method: str
    assumptions: str
    uncertainty: str
    validation_status: str

# --- COST ESTIMATION SCHEMAS ---
class CostEstimateOut(BaseModel):
    id: Optional[str] = None
    project_id: Optional[str] = None
    total_low: float
    total_expected: float
    total_high: float
    currency: str = "INR"
    rate_per_sqft: float
    material_cost: float
    labor_cost: float
    equipment_transport_cost: float
    professional_fees: float
    statutory_approvals_cost: float
    contingency_cost: float
    breakdown_by_phase: Dict[str, float]
    breakdown_by_material: List[MaterialItemOut]
    assumptions: List[str]

# --- SCHEDULING SCHEMAS ---
class ScheduleGenerateRequest(BaseModel):
    project_id: Optional[str] = None
    built_up_area: float = 1800.0
    floors: int = 2
    start_date: Optional[str] = None
    contractor_speed: str = "Normal" # Fast-track, Normal, Phased
    monsoon_factor: bool = True

class ScheduleTaskOut(BaseModel):
    id: str
    phase_name: str
    task_name: str
    start_day: int
    duration_days: int
    end_day: int
    dependencies: List[str]
    is_critical: bool
    status: str
    milestone: bool
    delay_risk_level: str
    description: Optional[str] = None

# --- CHAT & VOICE SCHEMAS ---
class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    project_id: Optional[str] = None
    message: str
    model: Optional[str] = "buildwise-llama3-construction-8b"
    language: Optional[str] = "en" # en, ta, tanglish

class VoiceTranscribeResponse(BaseModel):
    transcription: str
    detected_language: str
    confidence: float
    is_tanglish: bool
    tamil_translation: Optional[str] = None
    extracted_parameters: Optional[Dict[str, Any]] = None

class VoiceSpeakRequest(BaseModel):
    text: str
    language: Optional[str] = "en"
    voice_speed: Optional[float] = 1.0

# --- DOCUMENTS / RAG ---
class DocumentSearchRequest(BaseModel):
    query: str
    jurisdiction: Optional[str] = "Tamil Nadu / National"
    top_k: int = 4

class DocumentSearchResult(BaseModel):
    title: str
    section_code: Optional[str]
    publisher: str
    jurisdiction: str
    content: str
    relevance_score: float
