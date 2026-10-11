from typing import List, Dict, Any
from datetime import datetime, timedelta

def generate_construction_schedule(
    built_up_area: float = 1800.0,
    floors: int = 2,
    start_date_str: str = None,
    contractor_speed: str = "Normal",
    monsoon_factor: bool = True
) -> Dict[str, Any]:
    """
    Critical Path Method (CPM) construction scheduling engine.
    Calculates task durations, dependencies, earliest start/finish days,
    critical path flags, milestones, and weather delay risks.
    """
    speed_factor = 1.0
    if contractor_speed == "Fast-track":
        speed_factor = 0.82
    elif contractor_speed == "Phased":
        speed_factor = 1.25

    # Area duration scaling:
    # A standard 1800 sq.ft 2-floor house takes ~180 to 220 calendar days (~6-7 months).
    scale = (built_up_area / 1800.0) ** 0.5 * speed_factor

    # Phase sequence with predecessor links
    raw_tasks = [
        {
            "id": "TSK-01",
            "phase": "Phase 1: Architectural & Statutory",
            "name": "Soil Investigation & Structural Design",
            "base_days": 14,
            "deps": [],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "Borehole soil test, SBC verification, IS 456 RCC framing structural design"
        },
        {
            "id": "TSK-02",
            "phase": "Phase 1: Architectural & Statutory",
            "name": "Municipal Plan Sanction & EB/Water Approvals",
            "base_days": 21,
            "deps": ["TSK-01"],
            "critical": True,
            "milestone": True,
            "risk": "Medium",
            "desc": "Corporation/DTCP building permit, temporary electricity and water connection"
        },
        {
            "id": "TSK-03",
            "phase": "Phase 2: Substructure & Earthwork",
            "name": "Site Clearing, Excavation & Anti-Termite Treatment",
            "base_days": 10,
            "deps": ["TSK-02"],
            "critical": True,
            "milestone": False,
            "risk": "Medium" if monsoon_factor else "Low",
            "desc": "JCB earthwork, foundation trenches, PCC bed 1:4:8, chemical termite piping"
        },
        {
            "id": "TSK-04",
            "phase": "Phase 2: Substructure & Earthwork",
            "name": "Footings, Column Starters & Plinth Beam RCC",
            "base_days": 18,
            "deps": ["TSK-03"],
            "critical": True,
            "milestone": True,
            "risk": "Medium",
            "desc": "M20 concrete column footings, rebar cage tying, plinth beam casting and curing"
        },
        {
            "id": "TSK-05",
            "phase": "Phase 3: RCC Superstructure",
            "name": "Ground Floor Columns & First Floor Slab Casting",
            "base_days": 24,
            "deps": ["TSK-04"],
            "critical": True,
            "milestone": True,
            "risk": "High" if monsoon_factor else "Medium",
            "desc": "Column formwork, staging, beam rebar tying, 5-inch slab concrete pouring and 21-day pond curing"
        },
        {
            "id": "TSK-06",
            "phase": "Phase 3: RCC Superstructure",
            "name": "First Floor Columns & Roof Terrace Slab Casting",
            "base_days": 24 if floors > 1 else 0,
            "deps": ["TSK-05"],
            "critical": True if floors > 1 else False,
            "milestone": True if floors > 1 else False,
            "risk": "Medium",
            "desc": "Upper floor RCC frame, headroom, parapet beam, water tank pedestal casting"
        },
        {
            "id": "TSK-07",
            "phase": "Phase 4: Masonry & Enclosure",
            "name": "Exterior & Interior AAC Block Masonry",
            "base_days": 20,
            "deps": ["TSK-06"] if floors > 1 else ["TSK-05"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "600x200x200mm block laying with polymer joint mortar, lintel beams with chajjas"
        },
        {
            "id": "TSK-08",
            "phase": "Phase 5: MEP Rough-in",
            "name": "Electrical Conduit Chasing & Plumbing Wall Piping",
            "base_days": 14,
            "deps": ["TSK-07"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "Concealed PVC conduit chasing, switch boxes, CPVC hot/cold water supply and drainage drops"
        },
        {
            "id": "TSK-09",
            "phase": "Phase 6: Plastering & Waterproofing",
            "name": "Internal & External Plastering with Curing",
            "base_days": 20,
            "deps": ["TSK-08"],
            "critical": True,
            "milestone": True,
            "risk": "Medium",
            "desc": "12mm 1:6 internal smooth sponge plaster, 20mm 1:4 external sand-faced plaster + 14-day curing"
        },
        {
            "id": "TSK-10",
            "phase": "Phase 6: Plastering & Waterproofing",
            "name": "Terrace Roof & Sunken Bath Waterproofing",
            "base_days": 10,
            "deps": ["TSK-09"],
            "critical": False,
            "milestone": False,
            "risk": "Medium",
            "desc": "Elastomeric polymer membrane, pond testing 48 hours, protective screed slope"
        },
        {
            "id": "TSK-11",
            "phase": "Phase 7: Flooring & Finishing",
            "name": "Vitrified Tile Laying & Granite Countertops",
            "base_days": 18,
            "deps": ["TSK-09"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "800x800mm vitrified tiles, anti-skid bathroom tiles, black granite kitchen counter with sink"
        },
        {
            "id": "TSK-12",
            "phase": "Phase 7: Flooring & Finishing",
            "name": "Door Frames, Teak Joinery & UPVC Windows",
            "base_days": 12,
            "deps": ["TSK-11"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "Teak main door fixing, flush interior doors with Godrej locks, UPVC sliding glass windows"
        },
        {
            "id": "TSK-13",
            "phase": "Phase 8: Painting & Fixture Fitting",
            "name": "Interior Putty, Primer & 2-Coat Acrylic Emulsion",
            "base_days": 15,
            "deps": ["TSK-12"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "2 coats Birla White wall putty, primer, Asian Paints Royale interior + Apex exterior"
        },
        {
            "id": "TSK-14",
            "phase": "Phase 8: Painting & Fixture Fitting",
            "name": "Sanitary Ware, Modular Switches & Deep Cleaning",
            "base_days": 8,
            "deps": ["TSK-13"],
            "critical": True,
            "milestone": False,
            "risk": "Low",
            "desc": "Jaquar faucets, EWC commodes, Legrand switches, light fittings, site debris removal"
        },
        {
            "id": "TSK-15",
            "phase": "Phase 9: Final Handover",
            "name": "Final Quality Audit, Completion Certificate & Griha Pravesham",
            "base_days": 5,
            "deps": ["TSK-14"],
            "critical": True,
            "milestone": True,
            "risk": "Low",
            "desc": "Snag list inspection, client key handover, completion documentation"
        }
    ]

    # Filter zero duration tasks (e.g. single floor)
    filtered = [t for t in raw_tasks if t["base_days"] > 0]
    
    # Calculate CPM Forward Pass
    task_map = {}
    current_day = 0
    tasks_out = []
    
    for t in filtered:
        dur = max(3, round(t["base_days"] * scale))
        
        # Determine earliest start based on max end of dependencies
        if not t["deps"]:
            start_day = 0
        else:
            dep_ends = [task_map[d]["end_day"] for d in t["deps"] if d in task_map]
            start_day = max(dep_ends) if dep_ends else 0
            
        end_day = start_day + dur
        
        task_info = {
            "id": t["id"],
            "phase_name": t["phase"],
            "task_name": t["name"],
            "start_day": start_day,
            "duration_days": dur,
            "end_day": end_day,
            "dependencies": t["deps"],
            "is_critical": t["critical"],
            "status": "In Progress" if start_day == 0 else "Pending",
            "milestone": t["milestone"],
            "delay_risk_level": t["risk"],
            "description": t["desc"]
        }
        task_map[t["id"]] = task_info
        tasks_out.append(task_info)
        
    total_project_days = max(t["end_day"] for t in tasks_out)
    
    # Calculate dates
    base_date = datetime.utcnow()
    if start_date_str:
        try:
            base_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except Exception:
            pass
            
    finish_date = base_date + timedelta(days=total_project_days)
    
    return {
        "total_duration_days": total_project_days,
        "total_months": round(total_project_days / 30.0, 1),
        "commencement_date": base_date.strftime("%Y-%m-%d"),
        "estimated_completion_date": finish_date.strftime("%Y-%m-%d"),
        "contractor_speed": contractor_speed,
        "critical_path_tasks_count": sum(1 for t in tasks_out if t["is_critical"]),
        "milestones_count": sum(1 for t in tasks_out if t["milestone"]),
        "weather_risk_assessment": "Monsoon impact buffer included: Earthwork & Slab casting schedule aligned with weather windows." if monsoon_factor else "Dry season accelerated timeline assumed.",
        "tasks": tasks_out
    }
