export interface FloorPlanRoom {
  id?: string;
  floor_level: number;
  name: string;
  room_type: string;
  x: number;
  y: number;
  width: number;
  length: number;
  area_sqft: number;
  orientation?: string;
  doors?: Array<{ wall: string; offset: number; width: number }>;
  windows?: Array<{ wall: string; offset: number; width: number }>;
}

export interface DesignVersion {
  id: string;
  project_id?: string;
  version_number: number;
  title: string;
  description?: string;
  total_area_sqft: number;
  ground_floor_area: number;
  first_floor_area: number;
  style: string;
  plot_boundary: {
    plot_width: number;
    plot_length: number;
    setback_front: number;
    setback_rear: number;
    setback_sides: number;
    usable_width: number;
    usable_length: number;
  };
  rooms: FloorPlanRoom[];
  elevation_data?: {
    style: string;
    floors: number;
    svg: string;
  };
  svg_data?: string;
  created_at?: string;
}

export interface MaterialItem {
  name: string;
  category: string;
  estimated_quantity: number;
  wastage_percent: number;
  procurement_quantity: number;
  unit: string;
  unit_price: number;
  total_cost: number;
  calculation_method: string;
  assumptions: string;
  uncertainty: string;
  validation_status: string;
}

export interface CostEstimate {
  id?: string;
  project_id?: string;
  total_low: number;
  total_expected: number;
  total_high: number;
  currency: string;
  rate_per_sqft: number;
  material_cost: number;
  labor_cost: number;
  equipment_transport_cost: number;
  professional_fees: number;
  statutory_approvals_cost: number;
  contingency_cost: number;
  breakdown_by_phase: Record<string, number>;
  breakdown_by_material: MaterialItem[];
  assumptions: string[];
}

export interface ScheduleTask {
  id: string;
  phase_name: string;
  task_name: string;
  start_day: number;
  duration_days: number;
  end_day: number;
  dependencies: string[];
  is_critical: boolean;
  status: string;
  milestone: boolean;
  delay_risk_level: string;
  description?: string;
}

export interface ConstructionSchedule {
  id?: string;
  project_id?: string;
  total_duration_days: number;
  total_months: number;
  commencement_date: string;
  estimated_completion_date: string;
  contractor_speed: string;
  critical_path_tasks_count: number;
  milestones_count: number;
  weather_risk_assessment: string;
  tasks: ScheduleTask[];
}

export interface RecommendedPicture {
  id: string;
  title: string;
  category: string;
  style: string;
  tags: string[];
  image_url: string;
  thumbnail_url: string;
  description: string;
  specifications?: Record<string, string>;
}

export interface TrainingInsight {
  status: string;
  user_style_memory?: string;
  building_type_memory?: string;
  alignment_score?: number;
}

export interface ModelCheckpoint {
  id: string;
  name: string;
  version: string;
  type: string;
  parameters: string;
  is_active: boolean;
  training_status: string;
  trained_on: string;
  final_loss?: number;
  final_perplexity?: number;
  alignment_method: string;
  created_at: string;
}

export interface KaggleTrainingStatus {
  datasets: Record<string, {
    title: string;
    author: string;
    url: string;
    description: string;
    sample_count: number;
    features: string[];
    status: string;
    identifier?: string;
  }>;
  training_state: {
    is_training: boolean;
    job_id?: string;
    current_epoch: number;
    total_epochs: number;
    progress_percent: number;
    current_step: number;
    total_steps: number;
    training_loss: number;
    eval_loss: number;
    perplexity: number;
    learning_rate: number;
    loss_history: Array<{ step: number; epoch: number; loss: number; eval_loss: number }>;
    recent_logs: string[];
    last_completed_checkpoint?: ModelCheckpoint;
  };
  sample_blueprints: Array<{
    id: string;
    building_type: string;
    total_area_sqft: number;
    bedrooms: number;
    bathrooms: number;
    plot_size: string;
    orientation: string;
    roof_style?: string;
    roof_material?: string;
    roof_pitch?: string;
    image_url: string;
    description: string;
    rooms: Array<{ name: string; size: string; area_sqft: number; orientation?: string }>;
    bouygues_takeoff: {
      concrete_m3: number;
      steel_tons: number;
      formwork_m2: number;
      schedule_days: number;
      roof_area_sqft?: number;
    };
  }>;
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant' | 'system';
  content: string;
  model_used?: string;
  tool_calls?: any[];
  structured_data?: {
    floor_plan?: DesignVersion;
    materials?: { items: MaterialItem[] };
    cost_estimate?: CostEstimate;
    schedule?: ConstructionSchedule;
    regulations?: { results: Array<{ title: string; section_code: string; content: string }> };
    recommended_pictures?: RecommendedPicture[];
    training_insight?: TrainingInsight;
  };
  audio_url?: string;
  created_at?: string;
}

export interface Conversation {
  id: string;
  title: string;
  project_id?: string;
  pinned?: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  building_type: string;
  location: string;
  plot_length: number;
  plot_width: number;
  plot_area: number;
  plot_area_unit: string;
  built_up_area: number;
  floors: number;
  rooms: number;
  target_budget: number;
  current_stage: string;
  created_at: string;
  updated_at: string;
}

export interface MaterialCatalogItem {
  id: string;
  category: string;
  name: string;
  specification?: string;
  unit: string;
  default_price: number;
  currency: string;
  supplier: string;
  location: string;
  quotation_date: string;
  tax_inclusive: boolean;
}
