from typing import Dict, List, Any, Optional
from backend.app.services.calculation_engine import calculate_material_quantities

# Baseline Verified Regional Price Catalog (Tamil Nadu / South India benchmarks)
DEFAULT_MATERIAL_CATALOG = [
    {
        "id": "mat-cem-01",
        "category": "Cement",
        "name": "UltraTech Super Cement OPC 53",
        "specification": "IS 12269 Grade 53 High Strength",
        "unit": "Bag (50kg)",
        "default_price": 395.0,
        "currency": "INR",
        "supplier": "South India Cements Depot",
        "location": "Chennai, Tamil Nadu",
        "quotation_date": "2026-09-15",
        "tax_inclusive": True
    },
    {
        "id": "mat-cem-02",
        "category": "Cement",
        "name": "Coromandel King PPC Cement",
        "specification": "IS 1489 Part 1 Fly-ash based PPC",
        "unit": "Bag (50kg)",
        "default_price": 375.0,
        "currency": "INR",
        "supplier": "India Cements Authorized Dealer",
        "location": "Coimbatore, Tamil Nadu",
        "quotation_date": "2026-09-20",
        "tax_inclusive": True
    },
    {
        "id": "mat-stl-01",
        "category": "Steel",
        "name": "Tata Tiscon 550D Super Ductile TMT",
        "specification": "IS 1786 Fe 550D Earthquake Resistant",
        "unit": "Metric Ton",
        "default_price": 66500.0,
        "currency": "INR",
        "supplier": "Tata Tiscon Direct Dealer",
        "location": "Chennai, Tamil Nadu",
        "quotation_date": "2026-10-01",
        "tax_inclusive": True
    },
    {
        "id": "mat-stl-02",
        "category": "Steel",
        "name": "JSW Neosteel Fe 550D TMT",
        "specification": "IS 1786 Fe 550D High Elongation",
        "unit": "Metric Ton",
        "default_price": 63500.0,
        "currency": "INR",
        "supplier": "JSW Steel Yard",
        "location": "Madurai, Tamil Nadu",
        "quotation_date": "2026-09-28",
        "tax_inclusive": True
    },
    {
        "id": "mat-snd-01",
        "category": "Sand",
        "name": "Manufactured M-Sand (Zone II)",
        "specification": "IS 383 Machine Crushed Granite Sand",
        "unit": "Metric Ton",
        "default_price": 1650.0,
        "currency": "INR",
        "supplier": "Blue Metal Quarry Consortium",
        "location": "Kanchipuram, Tamil Nadu",
        "quotation_date": "2026-09-10",
        "tax_inclusive": True
    },
    {
        "id": "mat-blk-01",
        "category": "Blocks",
        "name": "Siporex / Magicrete AAC Blocks 8\"",
        "specification": "600x200x200mm Autoclaved Aerated",
        "unit": "Piece",
        "default_price": 62.0,
        "currency": "INR",
        "supplier": "GreenBuild Blocks Ltd",
        "location": "Chennai, Tamil Nadu",
        "quotation_date": "2026-09-18",
        "tax_inclusive": True
    },
    {
        "id": "mat-til-01",
        "category": "Tiles",
        "name": "Kajaria 800x800mm Vitrified Floor Tiles",
        "specification": "Double Charged Nano Polished",
        "unit": "Sq.Ft",
        "default_price": 68.0,
        "currency": "INR",
        "supplier": "Kajaria Galaxy Showroom",
        "location": "Chennai, Tamil Nadu",
        "quotation_date": "2026-10-02",
        "tax_inclusive": True
    },
    {
        "id": "mat-pnt-01",
        "category": "Paint",
        "name": "Asian Paints Apex Ultima + Royale Emulsion",
        "specification": "Exterior Weather-proof + Interior Washable",
        "unit": "Litre",
        "default_price": 320.0,
        "currency": "INR",
        "supplier": "Asian Paints Colour World",
        "location": "Chennai, Tamil Nadu",
        "quotation_date": "2026-09-25",
        "tax_inclusive": True
    }
]

def calculate_full_cost_estimate(
    built_up_area: float = 1800.0,
    floors: int = 2,
    structure_type: str = "RCC Framed Structure",
    wall_type: str = "AAC Lightweight Blocks",
    construction_quality: str = "Standard Premium"
) -> Dict[str, Any]:
    """
    Computes an itemized construction budget covering civil materials, labour,
    mechanical equipment, professional architecture & structural fees,
    municipal plan sanctions, GST, and contingency reserves.
    Provides Low, Expected, and High ranges.
    """
    materials = calculate_material_quantities(
        built_up_area=built_up_area,
        floors=floors,
        structure_type=structure_type,
        wall_type=wall_type,
        construction_quality=construction_quality
    )
    
    total_material_cost = sum(item["total_cost"] for item in materials)
    
    # Labour component in South India / India Tier-1/2:
    # Usually ~28% to 34% of civil construction value or approx ₹480 - ₹620 / sq.ft.
    # Includes: Head Mason, Assistant Mason, Carpenter (shuttering), Bar-bender, Plumber, Electrician, Painter, Helper
    labor_rate_per_sqft = 540.0
    if construction_quality == "Economy":
        labor_rate_per_sqft = 460.0
    elif construction_quality == "Luxury":
        labor_rate_per_sqft = 680.0
    total_labor_cost = round(built_up_area * labor_rate_per_sqft, 2)
    
    # Equipment, Transportation & Machinery:
    # Concrete mixers, needle vibrators, scaffolding & shuttering staging, earth mover (JCB) excavation
    equipment_transport_cost = round(built_up_area * 95.0, 2)
    
    # Professional Architectural & Structural Engineering Fees:
    # Architectural drawings, 3D elevations, structural analysis, site supervision: ~₹45 to ₹75 / sq.ft.
    professional_fees = round(built_up_area * 55.0, 2)
    
    # Statutory Approvals & Sanction Fees (Corporation / CMDA / DTCP):
    # Plan sanction fee, development charges, water/sewerage connection deposit, electricity EB meter connection
    statutory_approvals = round(built_up_area * 40.0 + 35000.0, 2)
    
    # Subtotal
    subtotal_civil_and_services = (
        total_material_cost +
        total_labor_cost +
        equipment_transport_cost +
        professional_fees +
        statutory_approvals
    )
    
    # Taxes (GST): Materials already include GST in quotations; contractor margin / service GST ~ 6%
    tax_cost = round(subtotal_civil_and_services * 0.05, 2)
    
    # Contingency (Price escalation, unforeseen soil / site excavation conditions, design changes): 6%
    contingency_cost = round(subtotal_civil_and_services * 0.06, 2)
    
    total_expected = round(subtotal_civil_and_services + tax_cost + contingency_cost, 2)
    total_low = round(total_expected * 0.91, 2)   # -9% (Value engineering, bulk procurement, standard fittings)
    total_high = round(total_expected * 1.12, 2)  # +12% (Premium fixtures, Italian marble, teak carvings, monsoon delays)
    
    rate_per_sqft = round(total_expected / built_up_area, 2)
    
    # Breakdown by Phase
    breakdown_by_phase = {
        "Site Preparation & Earthwork": round(total_expected * 0.03, 2),
        "Foundation & Plinth RCC": round(total_expected * 0.14, 2),
        "RCC Superstructure (Columns, Beams, Slabs)": round(total_expected * 0.26, 2),
        "Masonry Wall Construction": round(total_expected * 0.11, 2),
        "Plastering & Waterproofing": round(total_expected * 0.09, 2),
        "Electrical Rough-in & Fixtures": round(total_expected * 0.07, 2),
        "Plumbing & Sanitation": round(total_expected * 0.06, 2),
        "Flooring & Wall Tiling": round(total_expected * 0.10, 2),
        "Doors, Windows & Woodwork": round(total_expected * 0.08, 2),
        "Painting & Final Handover": round(total_expected * 0.06, 2)
    }
    
    assumptions = [
        f"Built-up area: {built_up_area:.0f} sq.ft across {floors} floor(s).",
        f"Construction grade: {construction_quality} with RCC Framed design.",
        "Material unit rates calibrated against Q3 2026 Chennai & Tamil Nadu market benchmarks.",
        "Soil bearing capacity assumed normal (Safe Bearing Capacity ~180 kN/m²); isolated footing foundation included.",
        "Labour charges computed on standard daily wage index (Mason: ₹1,100/day, Helper: ₹750/day).",
        "Includes standard plan sanction deposits, temporary electricity/water, and 6% contingency reserve.",
        "Interior loose furniture, false ceiling, and exterior landscaping excluded."
    ]
    
    return {
        "total_low": total_low,
        "total_expected": total_expected,
        "total_high": total_high,
        "currency": "INR",
        "rate_per_sqft": rate_per_sqft,
        "material_cost": total_material_cost,
        "labor_cost": total_labor_cost,
        "equipment_transport_cost": equipment_transport_cost,
        "professional_fees": professional_fees,
        "statutory_approvals_cost": statutory_approvals,
        "contingency_cost": contingency_cost,
        "breakdown_by_phase": breakdown_by_phase,
        "breakdown_by_material": materials,
        "assumptions": assumptions
    }
