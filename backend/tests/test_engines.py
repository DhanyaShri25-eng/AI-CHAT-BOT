import pytest
from backend.app.services.floorplan_engine import generate_floor_plan
from backend.app.services.calculation_engine import calculate_material_quantities
from backend.app.services.pricing_engine import calculate_full_cost_estimate
from backend.app.services.schedule_engine import generate_construction_schedule
from backend.app.services.voice_service import extract_parameters_from_text
from backend.app.services.rag_service import search_building_codes

def test_floorplan_engine():
    res = generate_floor_plan(plot_width=30.0, plot_length=40.0, building_type="2BHK")
    assert res["total_area_sqft"] > 0
    assert len(res["rooms"]) >= 4
    assert "<svg" in res["svg_data"]
    assert "elevation_data" in res
    assert "<svg" in res["elevation_data"]["svg"]
    assert res["plot_boundary"]["usable_width"] == 24.0 # 30 - 3*2

def test_calculation_engine():
    items = calculate_material_quantities(built_up_area=1800.0, floors=2)
    names = [i["name"] for i in items]
    assert any("Cement" in n for n in names)
    assert any("Steel" in n for n in names)
    assert any("M-Sand" in n for n in names)
    assert any("Aggregate" in n for n in names)
    assert any("Tiles" in n for n in names)
    # Check steel quantity is reasonable: ~7-8 tons for 1800 sq ft
    steel = next(i for i in items if "Steel" in i["name"])
    assert 6.0 <= steel["procurement_quantity"] <= 9.0

def test_pricing_engine():
    est = calculate_full_cost_estimate(built_up_area=1800.0, floors=2)
    assert est["total_low"] < est["total_expected"] < est["total_high"]
    assert est["rate_per_sqft"] > 1800.0
    assert est["material_cost"] > 0
    assert est["labor_cost"] > 0
    assert len(est["breakdown_by_phase"]) == 10

def test_schedule_engine():
    sch = generate_construction_schedule(built_up_area=1800.0, floors=2)
    assert sch["total_duration_days"] > 120
    assert len(sch["tasks"]) >= 10
    assert sch["critical_path_tasks_count"] > 0

def test_voice_parameter_extraction():
    sample_text = "30x40 plot la 3BHK duplex veedu kattanum, budget 45 lakhs, vadakku paatha vaasal venum"
    params = extract_parameters_from_text(sample_text)
    assert params["plot_width"] == 30.0
    assert params["plot_length"] == 40.0
    assert params["budget_inr"] == 4500000.0
    assert params["orientation"] == "North"
    assert "3BHK" in params["building_type"]

def test_rag_service():
    res = search_building_codes("setback requirements for residential building")
    assert len(res) > 0
    assert "TNCDBR" in res[0]["title"] or "TNCDBR" in res[0]["section_code"]
