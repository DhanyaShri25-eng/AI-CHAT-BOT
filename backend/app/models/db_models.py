import datetime
import uuid
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def gen_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="homeowner")  # homeowner, architect, contractor, engineer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, unique=True)
    phone = Column(String(30), nullable=True)
    location = Column(String(255), default="Tamil Nadu, India")
    company_name = Column(String(255), nullable=True)
    experience_years = Column(Integer, default=0)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, unique=True)
    preferred_language = Column(String(20), default="en")  # en, ta, tanglish
    theme = Column(String(20), default="blueprint")  # light, dark, blueprint
    ai_model = Column(String(100), default="buildwise-llama3-construction-8b")
    voice_enabled = Column(Boolean, default=True)
    voice_speed = Column(Float, default=1.0)
    auto_tts = Column(Boolean, default=False)
    privacy_analytics = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="settings")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    building_type = Column(String(50), default="Residential")  # 1BHK, 2BHK, 3BHK, 4BHK, Duplex, Villa, Commercial
    location = Column(String(255), default="Chennai, Tamil Nadu")
    plot_length = Column(Float, default=40.0)  # feet
    plot_width = Column(Float, default=30.0)   # feet
    plot_area = Column(Float, default=1200.0)  # sq ft
    plot_area_unit = Column(String(20), default="sqft")
    built_up_area = Column(Float, default=1800.0) # sq ft
    floors = Column(Integer, default=2)
    rooms = Column(Integer, default=6)
    target_budget = Column(Float, default=4500000.0) # INR
    current_stage = Column(String(50), default="Planning") # Planning, Architecture, Approvals, Foundation, Structure, Masonry, Finishing, Completed
    start_date = Column(DateTime, nullable=True)
    estimated_completion_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="projects")
    requirements = relationship("ProjectRequirement", back_populates="project", uselist=False, cascade="all, delete-orphan")
    design_versions = relationship("DesignVersion", back_populates="project", cascade="all, delete-orphan")
    material_estimates = relationship("MaterialEstimate", back_populates="project", cascade="all, delete-orphan")
    cost_estimates = relationship("CostEstimate", back_populates="project", cascade="all, delete-orphan")
    schedules = relationship("ScheduleTask", back_populates="project", cascade="all, delete-orphan")


class ProjectRequirement(Base):
    __tablename__ = "project_requirements"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, unique=True)
    road_access_width = Column(Float, default=30.0) # feet
    plot_orientation = Column(String(20), default="North") # North, East, South, West
    bedrooms = Column(Integer, default=3)
    bathrooms = Column(Integer, default=3)
    kitchen_type = Column(String(50), default="Modular / Vastu Compliant (South-East)")
    dining_required = Column(Boolean, default=True)
    living_area_sqft = Column(Float, default=240.0)
    staircase_type = Column(String(50), default="Internal Dog-legged") # Internal, External
    parking_slots = Column(Integer, default=1) # 1 Car + 2 Bikes
    balconies = Column(Integer, default=2)
    terrace_garden = Column(Boolean, default=True)
    architectural_style = Column(String(50), default="Modern Contemporary") # Modern, Minimalist, Traditional Chettinad, Kerala Vernacular
    construction_quality = Column(String(50), default="Standard Premium") # Economy, Standard, Premium, Luxury
    material_preferences = Column(JSON, default=dict) # e.g. {"cement": "UltraTech 53", "steel": "Tata Tiscon Fe550D"}
    known_restrictions = Column(Text, nullable=True)
    setback_front = Column(Float, default=5.0) # feet
    setback_rear = Column(Float, default=3.0)
    setback_sides = Column(Float, default=3.0)
    extracted_from_chat = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="requirements")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    title = Column(String(255), default="New Project Consultation")
    pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False) # user, assistant, system
    content = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=True)
    tokens_used = Column(Integer, default=0)
    structured_data = Column(JSON, nullable=True) # for rendering floor plans, calculation tables, gantt charts directly
    tool_calls = Column(JSON, nullable=True)
    audio_url = Column(String(500), nullable=True)
    feedback_rating = Column(Integer, nullable=True) # 1 for thumbs up, -1 for thumbs down
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class DesignVersion(Base):
    __tablename__ = "design_versions"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    version_number = Column(Integer, default=1)
    title = Column(String(255), default="Concept Plan V1")
    description = Column(Text, nullable=True)
    total_area_sqft = Column(Float, default=1800.0)
    ground_floor_area = Column(Float, default=1000.0)
    first_floor_area = Column(Float, default=800.0)
    style = Column(String(50), default="Modern")
    plot_boundary = Column(JSON, nullable=False) # {width, length, setbacks: {front, rear, left, right}}
    elevation_data = Column(JSON, nullable=True) # Front elevation design concept parameters & SVG
    svg_data = Column(Text, nullable=True) # Rendered SVG markup
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="design_versions")
    rooms = relationship("FloorPlanRoom", back_populates="design_version", cascade="all, delete-orphan")


class FloorPlanRoom(Base):
    __tablename__ = "floor_plan_rooms"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    design_version_id = Column(String(36), ForeignKey("design_versions.id"), nullable=False)
    floor_level = Column(Integer, default=0) # 0 = Ground, 1 = First, etc.
    name = Column(String(100), nullable=False) # Living Room, Master Bedroom, Kitchen
    room_type = Column(String(50), nullable=False) # living, bed, bath, kitchen, dining, balcony, parking, stairs
    x = Column(Float, nullable=False) # Coordinates in feet from top-left origin
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False) # Width in feet
    length = Column(Float, nullable=False) # Length in feet
    area_sqft = Column(Float, nullable=False)
    orientation = Column(String(20), nullable=True) # SE, SW, NE, NW
    doors = Column(JSON, default=list) # [{wall: 'north', offset: 3, width: 3}]
    windows = Column(JSON, default=list) # [{wall: 'east', offset: 2, width: 4}]
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    design_version = relationship("DesignVersion", back_populates="rooms")


class MaterialCatalogItem(Base):
    __tablename__ = "material_catalog"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    category = Column(String(100), nullable=False) # Cement, Steel, Sand, Coarse Aggregate, Bricks/Blocks, Tiles, Paint, Plumbing, Electrical
    name = Column(String(255), nullable=False)
    specification = Column(String(255), nullable=True) # OPC 53 Grade, Fe 550D TMT, M-Sand Zone II
    unit = Column(String(50), nullable=False) # Bag (50kg), Metric Ton, Ton, Cu.Ft, Sq.Ft, Litre, Piece
    default_price = Column(Float, nullable=False) # Base price in INR
    currency = Column(String(10), default="INR")
    standard_code = Column(String(50), nullable=True) # IS 12269, IS 1786, IS 383
    wastage_percent = Column(Float, default=5.0) # Default standard wastage
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    quotations = relationship("SupplierQuotation", back_populates="material")


class SupplierQuotation(Base):
    __tablename__ = "supplier_quotations"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    material_id = Column(String(36), ForeignKey("material_catalog.id"), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=True) # UltraTech, Tata Tiscon, Coromandel, Asian Paints
    location = Column(String(100), default="Chennai")
    unit_price = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    delivery_charge = Column(Float, default=0.0)
    tax_inclusive = Column(Boolean, default=True) # 18% or 28% GST included
    quotation_date = Column(DateTime, default=datetime.datetime.utcnow)
    verified_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_verified = Column(Boolean, default=True)
    contact_phone = Column(String(50), nullable=True)

    material = relationship("MaterialCatalogItem", back_populates="quotations")


class MaterialEstimate(Base):
    __tablename__ = "material_estimates"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    total_built_up_sqft = Column(Float, nullable=False)
    items = Column(JSON, nullable=False) # list of calculated materials with quantity, wastage, units, formulas
    calculation_basis = Column(String(255), default="Deterministic Engineering Thumb-Rule & IS 456 Structural Mix")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="material_estimates")


class CostEstimate(Base):
    __tablename__ = "cost_estimates"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    total_low = Column(Float, nullable=False)
    total_expected = Column(Float, nullable=False)
    total_high = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    rate_per_sqft = Column(Float, nullable=False) # e.g. 2,100 INR/sq ft
    breakdown = Column(JSON, nullable=False) # breakdown by civil, structural, finishing, electrical, plumbing, labor, contingency
    assumptions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="cost_estimates")


class ScheduleTask(Base):
    __tablename__ = "schedule_tasks"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    phase_name = Column(String(100), nullable=False) # Substructure, Superstructure, Finishing
    task_name = Column(String(255), nullable=False)
    start_day = Column(Integer, default=0) # Relative day from project commencement
    duration_days = Column(Integer, default=14)
    dependencies = Column(JSON, default=list) # List of preceding task IDs
    is_critical = Column(Boolean, default=False) # Critical Path Method flag
    status = Column(String(50), default="Pending") # Pending, In Progress, Completed, Delayed
    milestone = Column(Boolean, default=False)
    delay_risk_level = Column(String(20), default="Low") # Low, Medium, High
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="schedules")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    title = Column(String(255), nullable=False)
    category = Column(String(100), default="Building Regulations") # NBC 2016, TNCDBR 2019, IS 456, Material Specs
    publisher = Column(String(255), default="Bureau of Indian Standards")
    jurisdiction = Column(String(100), default="National / Tamil Nadu")
    version = Column(String(50), default="2016/2019")
    content = Column(Text, nullable=False)
    embeddings = Column(JSON, nullable=True) # Vector representations
    section_code = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UploadedFileMetadata(Base):
    __tablename__ = "uploaded_files"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False)
    parsed_content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=True)
    rating = Column(Integer, nullable=False) # 1-5 or 1/-1
    category = Column(String(50), default="accuracy") # accuracy, floor_plan, cost, speed
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class UsageMetric(Base):
    __tablename__ = "usage_metrics"

    id = Column(String(36), primary_key=True, default=gen_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    endpoint = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=True)
    tokens_in = Column(Integer, default=0)
    tokens_out = Column(Integer, default=0)
    response_time_ms = Column(Float, default=0.0)
    status_code = Column(Integer, default=200)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
