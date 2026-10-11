import math
from typing import Dict, List, Any, Optional
import uuid

def generate_floor_plan(
    plot_width: float = 30.0,
    plot_length: float = 40.0,
    building_type: str = "2BHK",
    orientation: str = "North",
    floors: int = 1,
    architectural_style: str = "Modern",
    setback_front: float = 5.0,
    setback_rear: float = 3.0,
    setback_sides: float = 3.0
) -> Dict[str, Any]:
    """
    Deterministic architectural floor plan and footprint generator.
    Calculates setbacks, usable building envelope, room dimensions, circulation,
    Vastu alignment, door swings, and generates a blueprint-grade SVG.
    """
    # 1. Calculate usable building envelope
    usable_width = max(15.0, plot_width - (setback_sides * 2))
    usable_length = max(18.0, plot_length - (setback_front + setback_rear))
    ground_footprint_sqft = round(usable_width * usable_length, 2)
    
    rooms: List[Dict[str, Any]] = []
    
    # 2. Room generation based on building type
    # Coordinate system: origin (0,0) at usable footprint top-left
    # Front is at y = usable_length (South) or y = 0 depending on orientation.
    # We standardize: Front entry is at bottom (y approaching usable_length if North facing front)
    
    uw = usable_width
    ul = usable_length
    
    if "NALUKETTU" in building_type.upper() or "NALUKETTU" in architectural_style.upper() or "COURTYARD" in building_type.upper():
        # Authentic Kerala Nalukettu: Central Sunken Nadumuttam Courtyard, Poomukham Verandah,
        # Padinjattini (West Living), Vadakkini (North Kitchen/Dining), Thekkini (South Master Bed), Kizhakkini (East Pooja)
        rooms = [
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Central Nadumuttam (Sunken Courtyard & Rainwater Well)",
                "room_type": "courtyard",
                "x": round(uw * 0.35, 2),
                "y": round(ul * 0.35, 2),
                "width": round(uw * 0.30, 2),
                "length": round(ul * 0.30, 2),
                "area_sqft": round((uw * 0.30) * (ul * 0.30), 1),
                "orientation": "Brahmasthana (Center)",
                "doors": [
                    {"wall": "north", "offset": 1.0, "width": 3.0},
                    {"wall": "south", "offset": 1.0, "width": 3.0},
                    {"wall": "east", "offset": 1.0, "width": 3.0},
                    {"wall": "west", "offset": 1.0, "width": 3.0}
                ],
                "windows": []
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Poomukham & Charupadi (Pillared Verandah)",
                "room_type": "verandah",
                "x": 0.0,
                "y": round(ul * 0.78, 2),
                "width": round(uw * 0.70, 2),
                "length": round(ul * 0.22, 2),
                "area_sqft": round((uw * 0.70) * (ul * 0.22), 1),
                "orientation": "North-East (Entrance)",
                "doors": [{"wall": "south", "offset": 2.5, "width": 4.0}],
                "windows": [{"wall": "north", "offset": 2.0, "width": 5.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Padinjattini (Western Block - Formal Living)",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.35, 2),
                "width": round(uw * 0.35, 2),
                "length": round(ul * 0.43, 2),
                "area_sqft": round((uw * 0.35) * (ul * 0.43), 1),
                "orientation": "West",
                "doors": [{"wall": "east", "offset": 2.0, "width": 3.2}],
                "windows": [{"wall": "west", "offset": 2.5, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Vadakkini (Northern Block - Modular Kitchen & Dining)",
                "room_type": "kitchen",
                "x": round(uw * 0.35, 2),
                "y": round(ul * 0.65, 2),
                "width": round(uw * 0.65, 2),
                "length": round(ul * 0.35, 2),
                "area_sqft": round((uw * 0.65) * (ul * 0.35), 1),
                "orientation": "North / South-East (Agni)",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 3.5}, {"wall": "north", "offset": 4.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Thekkini (Southern Block - Master Bedroom Suite)",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.35, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.35), 1),
                "orientation": "South-West (Nairuthi)",
                "doors": [{"wall": "north", "offset": 2.0, "width": 3.2}],
                "windows": [{"wall": "south", "offset": 2.0, "width": 4.5}, {"wall": "west", "offset": 2.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Kizhakkini (Eastern Block - Thevarappura Pooja & Lounge)",
                "room_type": "pooja",
                "x": round(uw * 0.65, 2),
                "y": round(ul * 0.25, 2),
                "width": round(uw * 0.35, 2),
                "length": round(ul * 0.40, 2),
                "area_sqft": round((uw * 0.35) * (ul * 0.40), 1),
                "orientation": "East",
                "doors": [{"wall": "west", "offset": 1.5, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 3.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Attached Bath & Utility",
                "room_type": "bath",
                "x": round(uw * 0.58, 2),
                "y": 0.0,
                "width": round(uw * 0.42, 2),
                "length": round(ul * 0.25, 2),
                "area_sqft": round((uw * 0.42) * (ul * 0.25), 1),
                "orientation": "South",
                "doors": [{"wall": "west", "offset": 1.0, "width": 2.5}],
                "windows": [{"wall": "south", "offset": 1.0, "width": 2.0}]
            }
        ]
    elif "1BHK" in building_type.upper():
        # 1 BHK Layout: Verandah/Entry, Living/Dining, Kitchen, 1 Bedroom, 1 Bath
        rooms = [
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Living & Dining Room",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.4, 2),
                "width": round(uw * 0.62, 2),
                "length": round(ul * 0.6, 2),
                "area_sqft": round((uw * 0.62) * (ul * 0.6), 1),
                "orientation": "North-East",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.5}],
                "windows": [{"wall": "south", "offset": 6.0, "width": 5.0}, {"wall": "east", "offset": 3.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Modular Kitchen",
                "room_type": "kitchen",
                "x": round(uw * 0.62, 2),
                "y": round(ul * 0.5, 2),
                "width": round(uw * 0.38, 2),
                "length": round(ul * 0.5, 2),
                "area_sqft": round((uw * 0.38) * (ul * 0.5), 1),
                "orientation": "South-East (Agni)",
                "doors": [{"wall": "west", "offset": 1.5, "width": 2.8}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 3.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Master Bedroom",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.65, 2),
                "length": round(ul * 0.4, 2),
                "area_sqft": round((uw * 0.65) * (ul * 0.4), 1),
                "orientation": "South-West (Nairuthi)",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.0}],
                "windows": [{"wall": "west", "offset": 2.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Attached Bathroom",
                "room_type": "bath",
                "x": round(uw * 0.65, 2),
                "y": 0.0,
                "width": round(uw * 0.35, 2),
                "length": round(ul * 0.4, 2),
                "area_sqft": round((uw * 0.35) * (ul * 0.4), 1),
                "orientation": "West",
                "doors": [{"wall": "west", "offset": 1.0, "width": 2.5}],
                "windows": [{"wall": "north", "offset": 1.0, "width": 2.0}]
            }
        ]
    elif "3BHK" in building_type.upper():
        # 3BHK: Living, Dining, Kitchen, Pooja, Master Bed + Bath, Bed 2 + Bath, Bed 3, Common Bath, Foyer/Staircase
        rooms = [
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Formal Living Room",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.55, 2),
                "width": round(uw * 0.55, 2),
                "length": round(ul * 0.45, 2),
                "area_sqft": round((uw * 0.55) * (ul * 0.45), 1),
                "orientation": "North-East",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.8}],
                "windows": [{"wall": "east", "offset": 2.5, "width": 5.0}, {"wall": "south", "offset": 6.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Dining & Family Space",
                "room_type": "dining",
                "x": round(uw * 0.55, 2),
                "y": round(ul * 0.55, 2),
                "width": round(uw * 0.45, 2),
                "length": round(ul * 0.45, 2),
                "area_sqft": round((uw * 0.45) * (ul * 0.45), 1),
                "orientation": "East",
                "doors": [{"wall": "west", "offset": 1.5, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Modular Kitchen & Utility",
                "room_type": "kitchen",
                "x": round(uw * 0.6, 2),
                "y": round(ul * 0.25, 2),
                "width": round(uw * 0.4, 2),
                "length": round(ul * 0.3, 2),
                "area_sqft": round((uw * 0.4) * (ul * 0.3), 1),
                "orientation": "South-East (Agni Corner)",
                "doors": [{"wall": "south", "offset": 1.0, "width": 2.8}],
                "windows": [{"wall": "east", "offset": 1.5, "width": 3.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Master Bedroom (Suite)",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.35, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.35), 1),
                "orientation": "South-West (Master Nairuthi)",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.2}],
                "windows": [{"wall": "west", "offset": 2.0, "width": 5.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Master Ensuite Bath",
                "room_type": "bath",
                "x": 0.0,
                "y": round(ul * 0.35, 2),
                "width": round(uw * 0.28, 2),
                "length": round(ul * 0.2, 2),
                "area_sqft": round((uw * 0.28) * (ul * 0.2), 1),
                "orientation": "West",
                "doors": [{"wall": "north", "offset": 1.0, "width": 2.5}],
                "windows": [{"wall": "west", "offset": 1.0, "width": 2.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Bedroom 2 (Guest / Parents)",
                "room_type": "bed",
                "x": round(uw * 0.28, 2),
                "y": round(ul * 0.35, 2),
                "width": round(uw * 0.32, 2),
                "length": round(ul * 0.2, 2),
                "area_sqft": round((uw * 0.32) * (ul * 0.2), 1),
                "orientation": "North-West",
                "doors": [{"wall": "south", "offset": 1.0, "width": 3.0}],
                "windows": [{"wall": "north", "offset": 1.0, "width": 3.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Bedroom 3 (Kids Room)",
                "room_type": "bed",
                "x": round(uw * 0.6, 2),
                "y": 0.0,
                "width": round(uw * 0.4, 2),
                "length": round(ul * 0.25, 2),
                "area_sqft": round((uw * 0.4) * (ul * 0.25), 1),
                "orientation": "North-East",
                "doors": [{"wall": "south", "offset": 1.0, "width": 3.0}],
                "windows": [{"wall": "north", "offset": 1.5, "width": 4.0}]
            }
        ]
    elif "DUPLEX" in building_type.upper() or floors > 1:
        # Duplex: Ground Floor (Grand Living, Kitchen, Dining, Master Bed, Staircase, Foyer) + First Floor (2 Beds, Family Lounge, Balcony, Terrace)
        rooms = [
            # Ground Floor
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Grand Living Foyer",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.5, 2),
                "width": round(uw * 0.55, 2),
                "length": round(ul * 0.5, 2),
                "area_sqft": round((uw * 0.55) * (ul * 0.5), 1),
                "orientation": "North-East",
                "doors": [{"wall": "south", "offset": 2.5, "width": 4.0}],
                "windows": [{"wall": "south", "offset": 7.0, "width": 5.0}, {"wall": "east", "offset": 3.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Open Modular Kitchen & Dining",
                "room_type": "kitchen",
                "x": round(uw * 0.55, 2),
                "y": round(ul * 0.5, 2),
                "width": round(uw * 0.45, 2),
                "length": round(ul * 0.5, 2),
                "area_sqft": round((uw * 0.45) * (ul * 0.5), 1),
                "orientation": "South-East (Agni)",
                "doors": [{"wall": "west", "offset": 2.0, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Ground Master Suite",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.35, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.35), 1),
                "orientation": "South-West (Nairuthi)",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.2}],
                "windows": [{"wall": "west", "offset": 2.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Dog-Legged Staircase & Foyer",
                "room_type": "stairs",
                "x": round(uw * 0.58, 2),
                "y": 0.0,
                "width": round(uw * 0.42, 2),
                "length": round(ul * 0.5, 2),
                "area_sqft": round((uw * 0.42) * (ul * 0.5), 1),
                "orientation": "North-West",
                "doors": [{"wall": "south", "offset": 1.0, "width": 3.0}],
                "windows": [{"wall": "north", "offset": 1.5, "width": 3.0}]
            },
            # First Floor
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 1,
                "name": "First Floor Family Lounge",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.45, 2),
                "width": round(uw * 0.55, 2),
                "length": round(ul * 0.55, 2),
                "area_sqft": round((uw * 0.55) * (ul * 0.55), 1),
                "orientation": "Center-East",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.2}],
                "windows": [{"wall": "east", "offset": 3.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 1,
                "name": "Upper Master Bedroom",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.45, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.45), 1),
                "orientation": "South-West",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.0}],
                "windows": [{"wall": "west", "offset": 2.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 1,
                "name": "Covered Balcony & Sit-out",
                "room_type": "balcony",
                "x": round(uw * 0.55, 2),
                "y": round(ul * 0.65, 2),
                "width": round(uw * 0.45, 2),
                "length": round(ul * 0.35, 2),
                "area_sqft": round((uw * 0.45) * (ul * 0.35), 1),
                "orientation": "North-East Road Facing",
                "doors": [{"wall": "north", "offset": 1.5, "width": 3.0}],
                "windows": []
            }
        ]
    else:
        # Default 2BHK: Living, Dining, Kitchen, Master Bed + Bath, Bed 2, Common Bath
        rooms = [
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Living & Drawing Hall",
                "room_type": "living",
                "x": 0.0,
                "y": round(ul * 0.48, 2),
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.52, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.52), 1),
                "orientation": "North-East",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.8}],
                "windows": [{"wall": "south", "offset": 7.0, "width": 4.5}, {"wall": "east", "offset": 2.0, "width": 4.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Kitchen & Dining Area",
                "room_type": "kitchen",
                "x": round(uw * 0.58, 2),
                "y": round(ul * 0.48, 2),
                "width": round(uw * 0.42, 2),
                "length": round(ul * 0.52, 2),
                "area_sqft": round((uw * 0.42) * (ul * 0.52), 1),
                "orientation": "South-East (Agni Corner)",
                "doors": [{"wall": "west", "offset": 1.5, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 2.0, "width": 3.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Master Bedroom",
                "room_type": "bed",
                "x": 0.0,
                "y": 0.0,
                "width": round(uw * 0.58, 2),
                "length": round(ul * 0.48, 2),
                "area_sqft": round((uw * 0.58) * (ul * 0.48), 1),
                "orientation": "South-West (Nairuthi Corner)",
                "doors": [{"wall": "south", "offset": 2.0, "width": 3.0}],
                "windows": [{"wall": "west", "offset": 2.0, "width": 4.5}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Attached Bathroom",
                "room_type": "bath",
                "x": round(uw * 0.58, 2),
                "y": 0.0,
                "width": round(uw * 0.22, 2),
                "length": round(ul * 0.24, 2),
                "area_sqft": round((uw * 0.22) * (ul * 0.24), 1),
                "orientation": "West",
                "doors": [{"wall": "west", "offset": 0.8, "width": 2.5}],
                "windows": [{"wall": "north", "offset": 0.8, "width": 2.0}]
            },
            {
                "id": str(uuid.uuid4())[:8],
                "floor_level": 0,
                "name": "Children / Guest Bedroom",
                "room_type": "bed",
                "x": round(uw * 0.58, 2),
                "y": round(ul * 0.24, 2),
                "width": round(uw * 0.42, 2),
                "length": round(ul * 0.24, 2),
                "area_sqft": round((uw * 0.42) * (ul * 0.24), 1),
                "orientation": "North-West (Vayu)",
                "doors": [{"wall": "south", "offset": 1.0, "width": 3.0}],
                "windows": [{"wall": "east", "offset": 1.2, "width": 3.5}]
            }
        ]

    # Calculate total area
    ground_rooms = [r for r in rooms if r.get("floor_level", 0) == 0]
    first_rooms = [r for r in rooms if r.get("floor_level", 0) == 1]
    ground_area = sum(r["area_sqft"] for r in ground_rooms)
    first_area = sum(r["area_sqft"] for r in first_rooms)
    total_built_up = ground_area + first_area
    
    # 3. Generate Blueprint SVG
    svg_markup = render_blueprint_svg(
        plot_w=plot_width,
        plot_l=plot_length,
        setback_f=setback_front,
        setback_r=setback_rear,
        setback_s=setback_sides,
        rooms=rooms,
        orientation=orientation
    )
    
    # 4. Generate Architectural Front Elevation SVG
    elevation_markup = render_elevation_svg(
        building_type=building_type,
        floors=2 if ("DUPLEX" in building_type.upper() or floors > 1) else 1,
        style=architectural_style,
        width_ft=usable_width
    )
    
    return {
        "id": str(uuid.uuid4()),
        "version_number": 1,
        "title": f"Architectural Blueprint - {building_type} ({architectural_style})",
        "description": f"Vastu-compliant conceptual layout generated for {plot_width}x{plot_length} ft plot with {orientation} orientation.",
        "total_area_sqft": round(total_built_up, 1),
        "ground_floor_area": round(ground_area, 1),
        "first_floor_area": round(first_area, 1),
        "style": architectural_style,
        "plot_boundary": {
            "plot_width": plot_width,
            "plot_length": plot_length,
            "setback_front": setback_front,
            "setback_rear": setback_rear,
            "setback_sides": setback_sides,
            "usable_width": usable_width,
            "usable_length": usable_length
        },
        "rooms": rooms,
        "elevation_data": {
            "style": architectural_style,
            "floors": 2 if ("DUPLEX" in building_type.upper() or floors > 1) else 1,
            "svg": elevation_markup
        },
        "svg_data": svg_markup
    }

def render_blueprint_svg(
    plot_w: float,
    plot_l: float,
    setback_f: float,
    setback_r: float,
    setback_s: float,
    rooms: List[Dict[str, Any]],
    orientation: str
) -> str:
    """Generate high-precision SVG blueprint with dimensional labels, doors, and room colors."""
    # Scale factor: 1 ft = 18 px
    scale = 18.0
    pad = 40.0
    
    view_w = int(plot_w * scale + pad * 2)
    view_h = int(plot_l * scale + pad * 2)
    
    # Room colors by type
    palette = {
        "living": "#1e3a5f",    # Blueprint deep cyan
        "dining": "#1b3350",
        "kitchen": "#2c3b28",   # Sage green accent
        "bed": "#24324c",       # Slate
        "bath": "#1d2e38",      # Teal
        "stairs": "#282a36",    # Dark slate
        "balcony": "#1e3745"
    }
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="100%" height="100%" style="background-color: #0b1329; font-family: monospace;">',
        '<!-- Grid Background -->',
        '<defs>',
        '  <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse">',
        '    <path d="M 18 0 L 0 0 0 18" fill="none" stroke="#16274a" stroke-width="0.8"/>',
        '  </pattern>',
        '  <pattern id="grid-major" width="90" height="90" patternUnits="userSpaceOnUse">',
        '    <path d="M 90 0 L 0 0 0 90" fill="none" stroke="#1e3663" stroke-width="1.2"/>',
        '  </pattern>',
        '</defs>',
        f'<rect width="{view_w}" height="{view_h}" fill="url(#grid)" />',
        f'<rect width="{view_w}" height="{view_h}" fill="url(#grid-major)" />',
        
        '<!-- Plot Boundary (Dotted Gold) -->',
        f'<rect x="{pad}" y="{pad}" width="{plot_w * scale}" height="{plot_l * scale}" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="6,4"/>',
        f'<text x="{pad + 10}" y="{pad - 12}" fill="#f59e0b" font-size="12" font-weight="bold">PLOT BOUNDARY: {plot_w:.0f}\' x {plot_l:.0f}\' ({(plot_w*plot_l):.0f} sq.ft)</text>',
        
        '<!-- Setback Zone (Translucent hatching) -->',
        f'<text x="{pad + 10}" y="{pad + 20}" fill="#64748b" font-size="10">REAR SETBACK {setback_r:.1f}\'</text>',
        f'<text x="{pad + 10}" y="{view_h - pad - 10}" fill="#64748b" font-size="10">FRONT SETBACK {setback_f:.1f}\' (ROAD ACCESS)</text>',
        
        '<!-- North Arrow -->',
        f'<g transform="translate({view_w - pad - 35}, {pad + 40})">',
        '  <circle cx="0" cy="0" r="18" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>',
        '  <path d="M 0 -14 L 6 0 L -6 0 Z" fill="#38bdf8"/>',
        '  <path d="M 0 14 L 6 0 L -6 0 Z" fill="#64748b"/>',
        f'  <text x="-4" y="-18" fill="#38bdf8" font-size="11" font-weight="bold">N</text>',
        f'  <text x="-12" y="32" fill="#94a3b8" font-size="9">{orientation}</text>',
        '</g>'
    ]
    
    # Origin of building footprint (taking setbacks into account)
    footprint_x = pad + (setback_s * scale)
    footprint_y = pad + (setback_r * scale)
    
    # Render Rooms
    for r in rooms:
        if r.get("floor_level", 0) != 0:
            continue # Render ground floor in main blueprint
        rx = footprint_x + (r["x"] * scale)
        ry = footprint_y + (r["y"] * scale)
        rw = r["width"] * scale
        rh = r["length"] * scale
        color = palette.get(r["room_type"], "#1e293b")
        
        # Room Box
        svg.append(f'<!-- Room: {r["name"]} -->')
        svg.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="{color}" stroke="#38bdf8" stroke-width="2.5" fill-opacity="0.85" rx="2"/>')
        
        # Room text label
        cx = rx + rw / 2
        cy = ry + rh / 2
        svg.append(f'<text x="{cx}" y="{cy - 8}" fill="#f8fafc" font-size="11" font-weight="bold" text-anchor="middle">{r["name"]}</text>')
        svg.append(f'<text x="{cx}" y="{cy + 8}" fill="#38bdf8" font-size="10" text-anchor="middle">{r["width"]:.1f}\' x {r["length"]:.1f}\'</text>')
        svg.append(f'<text x="{cx}" y="{cy + 22}" fill="#94a3b8" font-size="9" text-anchor="middle">({r["area_sqft"]:.0f} sq.ft)</text>')
        
        # Door Indicators
        for d in r.get("doors", []):
            wall = d.get("wall", "south")
            offset = d.get("offset", 2.0) * scale
            dw = d.get("width", 3.0) * scale
            if wall == "south":
                dx = rx + offset
                dy = ry + rh
                svg.append(f'<line x1="{dx}" y1="{dy}" x2="{dx + dw}" y2="{dy}" stroke="#facc15" stroke-width="3.5"/>')
                svg.append(f'<path d="M {dx} {dy} A {dw} {dw} 0 0 1 {dx + dw} {dy - dw}" fill="none" stroke="#facc15" stroke-dasharray="2,2"/>')
            elif wall == "north":
                dx = rx + offset
                dy = ry
                svg.append(f'<line x1="{dx}" y1="{dy}" x2="{dx + dw}" y2="{dy}" stroke="#facc15" stroke-width="3.5"/>')
            elif wall == "east":
                dx = rx + rw
                dy = ry + offset
                svg.append(f'<line x1="{dx}" y1="{dy}" x2="{dx}" y2="{dy + dw}" stroke="#facc15" stroke-width="3.5"/>')
            elif wall == "west":
                dx = rx
                dy = ry + offset
                svg.append(f'<line x1="{dx}" y1="{dy}" x2="{dx}" y2="{dy + dw}" stroke="#facc15" stroke-width="3.5"/>')
                
        # Window Indicators
        for w in r.get("windows", []):
            wall = w.get("wall", "east")
            offset = w.get("offset", 2.0) * scale
            ww = w.get("width", 3.5) * scale
            if wall == "east":
                wx = rx + rw
                wy = ry + offset
                svg.append(f'<rect x="{wx - 2}" y="{wy}" width="4" height="{ww}" fill="#0ea5e9" stroke="#ffffff" stroke-width="0.8"/>')
            elif wall == "west":
                wx = rx
                wy = ry + offset
                svg.append(f'<rect x="{wx - 2}" y="{wy}" width="4" height="{ww}" fill="#0ea5e9" stroke="#ffffff" stroke-width="0.8"/>')
            elif wall == "north":
                wx = rx + offset
                wy = ry
                svg.append(f'<rect x="{wx}" y="{wy - 2}" width="{ww}" height="4" fill="#0ea5e9" stroke="#ffffff" stroke-width="0.8"/>')
            elif wall == "south":
                wx = rx + offset
                wy = ry + rh
                svg.append(f'<rect x="{wx}" y="{wy - 2}" width="{ww}" height="4" fill="#0ea5e9" stroke="#ffffff" stroke-width="0.8"/>')

    # Legend at bottom right
    svg.append(f'<g transform="translate({view_w - 220}, {view_h - 75})">')
    svg.append('  <rect width="200" height="65" fill="#0f172a" stroke="#334155" rx="4"/>')
    svg.append('  <line x1="12" y1="18" x2="35" y2="18" stroke="#38bdf8" stroke-width="2.5"/>')
    svg.append('  <text x="42" y="22" fill="#cbd5e1" font-size="10">RCC Wall / Partition</text>')
    svg.append('  <line x1="12" y1="36" x2="35" y2="36" stroke="#facc15" stroke-width="2.5"/>')
    svg.append('  <text x="42" y="40" fill="#cbd5e1" font-size="10">Door Openings (Swing)</text>')
    svg.append('  <rect x="12" y="48" width="22" height="6" fill="#0ea5e9"/>')
    svg.append('  <text x="42" y="54" fill="#cbd5e1" font-size="10">Glazed Windows</text>')
    svg.append('</g>')
    
    svg.append('</svg>')
    return "\n".join(svg)

def render_elevation_svg(
    building_type: str,
    floors: int = 2,
    style: str = "Modern",
    width_ft: float = 24.0
) -> str:
    """Generate architectural front elevation concept SVG with parapet, glazing, and textures."""
    w = 640
    h = 420
    floor_h = 130
    ground_y = 350
    b_w = 420
    b_x = (w - b_w) // 2
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%" style="background: linear-gradient(180deg, #090d16 0%, #111d33 100%); font-family: sans-serif;">',
        '<!-- Sky backdrop & ground line -->',
        f'<line x1="20" y1="{ground_y}" x2="{w - 20}" y2="{ground_y}" stroke="#64748b" stroke-width="3"/>',
        f'<rect x="20" y="{ground_y}" width="{w - 40}" height="50" fill="#1e293b"/>',
        f'<text x="40" y="{ground_y + 25}" fill="#94a3b8" font-size="11">GROUND LEVEL ±0.00\'</text>',
        
        '<!-- Plinth Beam Level -->',
        f'<rect x="{b_x - 10}" y="{ground_y - 20}" width="{b_w + 20}" height="20" fill="#334155" stroke="#475569" stroke-width="1.5"/>',
        f'<text x="{b_x + b_w + 18}" y="{ground_y - 8}" fill="#38bdf8" font-size="10">+2.5\' PLINTH</text>'
    ]
    
    # Ground Floor Facade
    g_top = ground_y - 20 - floor_h
    svg.append(f'<!-- Ground Floor Facade -->')
    svg.append(f'<rect x="{b_x}" y="{g_top}" width="{b_w}" height="{floor_h}" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>')
    # Main Entrance Teak Door
    svg.append(f'<rect x="{b_x + 50}" y="{g_top + 30}" width="55" height="100" fill="#78350f" stroke="#b45309" stroke-width="2"/>')
    svg.append(f'<circle cx="{b_x + 95}" cy="{g_top + 80}" r="3" fill="#facc15"/>') # Door handle
    # Large French Window
    svg.append(f'<rect x="{b_x + 160}" y="{g_top + 35}" width="110" height="75" fill="#0284c7" stroke="#38bdf8" stroke-width="2" fill-opacity="0.3"/>')
    svg.append(f'<line x1="{b_x + 215}" y1="{g_top + 35}" x2="{b_x + 215}" y2="{g_top + 110}" stroke="#38bdf8" stroke-width="1.5"/>')
    # Louvered accent panel / stone cladding
    svg.append(f'<rect x="{b_x + 300}" y="{g_top + 10}" width="95" height="110" fill="#334155" stroke="#64748b" stroke-width="1.5"/>')
    for y_offset in range(15, 110, 10):
        svg.append(f'<line x1="{b_x + 300}" y1="{g_top + y_offset}" x2="{b_x + 395}" y2="{g_top + y_offset}" stroke="#475569" stroke-width="1.2"/>')
    svg.append(f'<text x="{b_x + b_w + 18}" y="{g_top + floor_h // 2}" fill="#94a3b8" font-size="10">+10.5\' CEILING</text>')

    if floors >= 2:
        # First Floor
        f1_top = g_top - floor_h
        svg.append(f'<!-- Intermediate Slab Beam -->')
        svg.append(f'<rect x="{b_x - 15}" y="{g_top - 12}" width="{b_w + 30}" height="12" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>')
        
        svg.append(f'<!-- First Floor Facade -->')
        svg.append(f'<rect x="{b_x}" y="{f1_top}" width="{b_w}" height="{floor_h}" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>')
        
        # Cantilevered Balcony with Glass Railing
        svg.append(f'<rect x="{b_x + 30}" y="{f1_top + 60}" width="160" height="60" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5" fill-opacity="0.25"/>')
        svg.append(f'<line x1="{b_x + 30}" y1="{f1_top + 60}" x2="{b_x + 190}" y2="{f1_top + 60}" stroke="#f8fafc" stroke-width="2"/>')
        svg.append(f'<text x="{b_x + 65}" y="{f1_top + 95}" fill="#e2e8f0" font-size="10">GLASS BALCONY</text>')
        
        # Master Bedroom Corner Window
        svg.append(f'<rect x="{b_x + 230}" y="{f1_top + 25}" width="140" height="80" fill="#0284c7" stroke="#38bdf8" stroke-width="2" fill-opacity="0.3"/>')
        svg.append(f'<line x1="{b_x + 300}" y1="{f1_top + 25}" x2="{b_x + 300}" y2="{f1_top + 105}" stroke="#38bdf8" stroke-width="1.5"/>')
        
        # Parapet Wall & Pergola
        parapet_top = f1_top - 35
        svg.append(f'<!-- Parapet & Terrace -->')
        svg.append(f'<rect x="{b_x - 10}" y="{parapet_top}" width="{b_w + 20}" height="35" fill="#334155" stroke="#475569" stroke-width="1.5"/>')
        # Modern Pergola Beams
        for px in range(b_x + 40, b_x + 180, 25):
            svg.append(f'<rect x="{px}" y="{parapet_top - 18}" width="12" height="18" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>')
        svg.append(f'<text x="{b_x + b_w + 18}" y="{parapet_top + 18}" fill="#f59e0b" font-size="10">+23.5\' TERRACE</text>')
    else:
        parapet_top = g_top - 30
        svg.append(f'<rect x="{b_x - 5}" y="{parapet_top}" width="{b_w + 10}" height="30" fill="#334155" stroke="#475569" stroke-width="1.5"/>')
        svg.append(f'<text x="{b_x + b_w + 18}" y="{parapet_top + 18}" fill="#f59e0b" font-size="10">+13.0\' PARAPET</text>')

    # Title header inside SVG
    svg.append(f'<text x="30" y="35" fill="#38bdf8" font-size="14" font-weight="bold">CONCEPTUAL FRONT ELEVATION - {style.upper()} STYLE</text>')
    svg.append(f'<text x="30" y="52" fill="#94a3b8" font-size="11">{building_type} | {floors} Floor(s) | Architectural Elevation Concept</text>')
    
    svg.append('</svg>')
    return "\n".join(svg)
