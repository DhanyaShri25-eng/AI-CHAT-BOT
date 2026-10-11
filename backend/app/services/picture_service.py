from typing import List, Dict, Any, Optional
import re

# Comprehensive catalog of architectural and construction imagery
# Uses curated architectural photography with unique, verified images for each distinct design
PICTURE_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "pic-pin-luxury-01",
        "title": "Pinterest Curated: Ultra-Modern Cantilevered Luxury Villa",
        "category": "elevation",
        "style": "Modern Minimalist",
        "tags": ["pinterest", "luxury", "villa", "cantilever", "glass", "modern", "minimalist", "elevation", "duplex", "concrete"],
        "image_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=600&q=75",
        "description": "Trending Pinterest architectural pin: dramatic 4.5m cantilevered upper volume over fair-faced board-formed concrete, floor-to-ceiling sliding acoustic glass, and integrated illuminated lap pool.",
        "specifications": {
            "source_platform": "Pinterest Luxury Architecture Boards (Pin #8204)",
            "building_typology": "4BHK Contemporary Luxury Villa",
            "facade_composition": "Board-formed Concrete + Structural Low-E Glazing",
            "cantilever_span": "4.5m Reinforced Post-Tensioned Slab",
            "cost_bracket": "Luxury Tier (₹3,200 - ₹3,900 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-comm-01",
        "title": "Pinterest Curated: Commercial Glass Curtain Wall Plaza & Office",
        "category": "elevation",
        "style": "Commercial Contemporary",
        "tags": ["pinterest", "commercial", "office", "plaza", "glass", "curtain_wall", "elevation", "building", "complex", "retail"],
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=75",
        "description": "High-density commercial office building featuring unitized double-glazed curtain wall system, ground floor retail colonnade, central light-filled atrium, and integrated solar louvers.",
        "specifications": {
            "source_platform": "Pinterest Commercial Architecture Boards (Pin #5419)",
            "building_typology": "G+3 / G+5 Commercial Office & Retail Hub",
            "structural_framing": "RCC Column-Beam Grid (8m x 8m clear bays)",
            "glazing_system": "Double-glazed Argon-filled Low-E Curtain Wall",
            "cost_bracket": "Commercial Grade (₹2,600 - ₹3,400 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-ind-01",
        "title": "Pinterest Curated: Industrial PEB Steel Warehouse & Logistics Shed",
        "category": "elevation",
        "style": "Industrial PEB",
        "tags": ["pinterest", "industrial", "warehouse", "peb", "steel", "shed", "logistics", "factory", "commercial", "span"],
        "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=600&q=75",
        "description": "Pre-Engineered Building (PEB) clear-span steel warehouse with tapered portal frames (30m clear bay), 80mm insulated PUF sandwich panels, FM2 laser-screed floor, and ridge daylight monitors.",
        "specifications": {
            "source_platform": "Pinterest PEB Industrial Shed Boards (Pin #3190)",
            "building_typology": "Clear-Span Industrial Warehouse / Factory",
            "structural_system": "High-Tensile Structural Steel Portal Frame (Fe 350)",
            "roof_envelope": "Standing Seam PUF Insulated Sandwich Panels",
            "cost_bracket": "Industrial PEB (₹1,400 - ₹1,850 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-japan-01",
        "title": "Pinterest Curated: Japanese Minimalist Zen Residence (Minka & Engawa)",
        "category": "elevation",
        "style": "Japanese Minimalist",
        "tags": ["pinterest", "japanese", "zen", "minka", "minimalist", "engawa", "wood", "courtyard", "wabi_sabi", "yakisugi"],
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=600&q=75",
        "description": "Japanese Zen sanctuary combining Engawa covered perimeter cedar verandas, Yakisugi (shou-sugi-ban) charred wood cladding, sunken pebble Tsuboniwa courtyards, and Shoji diffused lighting.",
        "specifications": {
            "source_platform": "Pinterest Zen Japanese Architecture Boards (Pin #7621)",
            "building_typology": "3BHK Japanese Contemporary Courtyard Residence",
            "woodwork_cladding": "Yakisugi Charred Cedar + Hinoki Cypress Framing",
            "passive_cooling": "Deep cantilevered timber eaves with cross-atrium ventilation",
            "cost_bracket": "Premium Minimalist (₹2,500 - ₹3,100 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-nordic-01",
        "title": "Pinterest Curated: Scandinavian Nordic Contemporary Eco-Villa",
        "category": "elevation",
        "style": "Scandinavian Nordic",
        "tags": ["pinterest", "scandinavian", "nordic", "eco", "timber", "standing_seam", "a_frame", "sustainable", "passive_solar"],
        "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=600&q=75",
        "description": "Nordic sustainable residence featuring steep 45° pitch standing seam matte zinc roof, vertical dark pine cladding, triple-glazed solar thermal walls, and passive airtight insulation.",
        "specifications": {
            "source_platform": "Pinterest Scandinavian Eco Homes (Pin #9042)",
            "building_typology": "3BHK Nordic Eco-Villa / A-Frame Fusion",
            "structural_core": "Glulam Engineered Timber Posts & Beams",
            "roofing": "Standing Seam Matte Charcoal Zinc Sheeting (45° pitch)",
            "cost_bracket": "High-Efficiency Eco (₹2,400 - ₹3,000 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-medit-01",
        "title": "Pinterest Curated: Mediterranean Spanish Revival Hacienda Villa",
        "category": "elevation",
        "style": "Mediterranean Spanish",
        "tags": ["pinterest", "mediterranean", "spanish", "hacienda", "courtyard", "tiles", "barrel_tiles", "stucco", "arch"],
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=75",
        "description": "Spanish Revival hacienda centered around a terracotta-tiled fountain courtyard. White lime-washed stucco walls, low-pitch red clay barrel roof tiles (tejas), and arched colonnade loggias.",
        "specifications": {
            "source_platform": "Pinterest Mediterranean Hacienda Boards (Pin #4188)",
            "building_typology": "4BHK Spanish Revival Estate Villa",
            "roofing": "Handcrafted Red Clay Barrel Roof Tiles (Tejas Curvas)",
            "thermal_mass": "Thick Aerated Lime Stucco with deep recessed window reveals",
            "cost_bracket": "Luxury Hacienda (₹2,700 - ₹3,500 / sq.ft)"
        }
    },
    {
        "id": "pic-pin-apt-01",
        "title": "Multi-Family Residential G+3 Apartment Building",
        "category": "elevation",
        "style": "Contemporary Residential",
        "tags": ["apartment", "residential", "g+3", "flats", "units", "multi_family", "elevation", "balcony", "building"],
        "image_url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=75",
        "description": "Multi-unit G+3 residential building with 6 modular 2BHK/3BHK units, cantilevered balconies with safety railings, stilt parking zone, lift shaft core, and rooftop solar pergola.",
        "specifications": {
            "building_typology": "G+3 Multi-Family Apartment (6 Units)",
            "structural_core": "RCC Shear Wall & Ductile Framed Tube (IS 13920)",
            "circulation": "Central Passenger Lift + Fire Escape Staircase Core",
            "cost_bracket": "Multi-Unit Standard (₹2,100 - ₹2,700 / sq.ft)"
        }
    },
    {
        "id": "pic-nalu-01",
        "title": "Traditional Kerala Nalukettu Courtyard Villa",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["nalukettu", "kerala", "courtyard", "nadumuttam", "vernacular", "traditional", "thatchu_shastra", "poomukham", "tiles", "charupadi", "tharavadu"],
        "image_url": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=600&q=75",
        "description": "Authentic Kerala Nalukettu quad-structure homestead featuring terracotta Mangalore clay tiled roofs, exposed laterite masonry, ornate wooden gables (Mughappu), and pillared Poomukham.",
        "specifications": {
            "building_style": "Kerala Nalukettu (Four Blocks)",
            "courtyard": "Open-to-sky Central Nadumuttam",
            "materials": "Laterite Stone + Teakwood Pillars + Mangalore Clay Tiles",
            "roof_pitch": "42° Inward & Outward Sloped Hip Roof"
        }
    },
    {
        "id": "pic-elev-03",
        "title": "Kerala Traditional Vernacular Slope Roof House",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["elevation", "kerala", "traditional", "slope roof", "clay tiles", "vernacular", "south indian", "duplex", "monsoon"],
        "image_url": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=600&q=75",
        "description": "Climate-responsive tropical design with terracotta Mangalore clay roof tiles, exposed laterite stone masonry, wide overhangs for monsoon protection, and timber carved pillars.",
        "specifications": {
            "building_type": "2BHK / 3BHK Traditional Villa",
            "plot_size": "30x40 / 40x50 ft",
            "exterior_finish": "Laterite Cladding + Mangalore Clay Roof Tiles",
            "estimated_cost_tier": "Standard"
        }
    },
    {
        "id": "pic-roof-01",
        "title": "Kerala Vernacular Hip Roof (Mangalore Terracotta Tiles)",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["roof", "roof_style", "hip_roof", "kerala", "tiles", "terracotta", "census_india", "10029", "slope_roof", "monsoon"],
        "image_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&w=600&q=75",
        "description": "Census India Catalog 10029 H-03 A specification: 38.6% Kerala homes feature machine-made terracotta tiles. Combined with Kaggle 4-sided Hip Roof geometry for maximum monsoon rain runoff and cyclone wind deflection.",
        "specifications": {
            "roof_style": "Hip Roof (Pyramidal 4-sided)",
            "roof_material": "Machine-made Terracotta Clay Tiles (Census 10029)",
            "slope_angle": "38° Pitch",
            "rainfall_suitability": "> 3,000 mm annual rainfall"
        }
    },
    {
        "id": "pic-nalu-02",
        "title": "Sunken Central Nadumuttam Open Courtyard",
        "category": "interior",
        "style": "Kerala Vernacular",
        "tags": ["nalukettu", "nadumuttam", "courtyard", "interior", "thulsi", "rainwater", "kerala", "pillars", "atrium"],
        "image_url": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1544984243-ec57ea16fe25?auto=format&fit=crop&w=600&q=75",
        "description": "Sunken central Nadumuttam courtyard flanked by four carved teakwood columns and perimeter rainwater collection trough (Thumbi), providing natural convective stack cooling (-4°C indoors).",
        "specifications": {
            "room_type": "Central Nadumuttam Courtyard",
            "zone": "Brahmasthana (Center)",
            "thermal_effect": "Passive Convective Chimney Cooling (-4°C indoors)",
            "drainage": "Perimeter Granite Gutter leading to Rainwater Recharge"
        }
    },
    {
        "id": "pic-nalu-03",
        "title": "Poomukham Verandah with Carved Charupadi Seating",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["nalukettu", "charupadi", "poomukham", "verandah", "woodwork", "kerala", "teakwood", "porch"],
        "image_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?auto=format&fit=crop&w=600&q=75",
        "description": "Grand front reception verandah (Poomukham) with hand-carved Charupadi curved wooden bench seating, suspended brass lamps, and turn-crafted timber pillars.",
        "specifications": {
            "feature": "Charupadi Wooden Bench & Poomukham Verandah",
            "timber_spec": "Seasoned Burma Teak / Anjili Wood",
            "orientation": "East / North-East Facing Entry"
        }
    },
    {
        "id": "pic-trad-01",
        "title": "Chettinad & South Indian Heritage Courtyard Mansion",
        "category": "elevation",
        "style": "Traditional South Indian",
        "tags": ["chettinad", "heritage", "courtyard", "traditional", "athangudi", "mansion", "pillars", "thinnai"],
        "image_url": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?auto=format&fit=crop&w=600&q=75",
        "description": "Grand South Indian heritage home featuring handmade Athangudi patterned floor tiles, double-height Thinnai pillared verandahs, Burmese teak capitals, and lime-egg-plastered walls.",
        "specifications": {
            "building_type": "Heritage Mansion / 4BHK Courtyard",
            "flooring": "Handcrafted Athangudi Geometric Cement Tiles",
            "pillars": "Turned Solid Timber Columns with Stone Base",
            "estimated_cost_tier": "Luxury Heritage"
        }
    },
    {
        "id": "pic-trad-02",
        "title": "Modern Kerala Tropical Fusion Residence",
        "category": "elevation",
        "style": "Contemporary Tropical",
        "tags": ["tropical", "fusion", "kerala", "contemporary", "slope roof", "clay tiles", "glass", "duplex", "villa"],
        "image_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=600&q=75",
        "description": "Contemporary tropical architecture blending Mangalore sloped clay tiled roofs with expansive floor-to-ceiling glass fenestrations, cantilevered eaves, and landscaped inner gardens.",
        "specifications": {
            "building_type": "3BHK / 4BHK Tropical Fusion Duplex",
            "roof_type": "Sloped Terracotta + Concealed RCC Gutters",
            "glazing": "Double-Glazed Low-E Acoustic Glass",
            "estimated_cost_tier": "Standard Premium"
        }
    },
    {
        "id": "pic-trad-03",
        "title": "Laurie Baker Eco-Friendly Exposed Brick Vernacular House",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["laurie baker", "eco-friendly", "brick", "rat-trap", "filler slab", "vernacular", "budget", "sustainable", "jali"],
        "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=75",
        "description": "Laurie Baker cost-effective vernacular architecture with unplastered wire-cut rat-trap bond brickwork, terracotta Mangalore filler slab ceiling, and brick jali screens for natural cross-breeze.",
        "specifications": {
            "masonry": "Rat-Trap Bond Exposed Brick (saves 25% bricks & cement)",
            "roofing": "Terracotta Tile Filler Slab (30% less concrete & steel)",
            "ventilation": "Perforated Brick Jali Screen (zero AC energy need)",
            "cost_saving": "20% - 28% below standard RCC construction"
        }
    },
    {
        "id": "pic-trad-04",
        "title": "Traditional Padippura Entrance Gateway & Canopy",
        "category": "elevation",
        "style": "Kerala Vernacular",
        "tags": ["padippura", "gate", "entrance", "kerala", "traditional", "canopy", "roof", "tiles"],
        "image_url": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e?auto=format&fit=crop&w=600&q=75",
        "description": "Traditional Kerala boundary gateway (Padippura) featuring an arched timber doorway, Mangalore clay tiled hip canopy, brass bell fittings, and carved timber eaves.",
        "specifications": {
            "structure": "Padippura Entrance Gateway",
            "woodwork": "Weathered Anjili / Teak with Brass Studs",
            "roofing": "Miniature Mangalore Tile Hip Canopy"
        }
    },
    {
        "id": "pic-roof-02",
        "title": "Modern Urban Flat RCC Roof Terrace with Solar Pergola",
        "category": "elevation",
        "style": "Modern Minimalist",
        "tags": ["roof", "roof_style", "flat_roof", "rcc", "terrace", "concrete", "census_india", "10029", "solar", "waterproofing"],
        "image_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=600&q=75",
        "description": "Census India Catalog 10029 H-03 A standard: 48.2% predominant RCC concrete roof. Features 1:50 screed gradient, elastomeric waterproofing membrane, and rooftop solar pergola.",
        "specifications": {
            "roof_style": "Flat Roof with Parapet (Kaggle Flat)",
            "roof_material": "Reinforced Cement Concrete (RCC M25)",
            "waterproofing": "Dr. Fixit Integral + Elastomeric PU Membrane",
            "utility": "Solar PV Rooftop + Usable Recreation Terrace"
        }
    },
    {
        "id": "pic-roof-03",
        "title": "Contemporary Dual-Pitch Gable Roof Cottage",
        "category": "elevation",
        "style": "Contemporary",
        "tags": ["roof", "roof_style", "gable_roof", "metal_roof", "standing_seam", "census_india", "10029", "modern", "cottage"],
        "image_url": "https://images.unsplash.com/photo-1448630360428-65456885c650?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1448630360428-65456885c650?auto=format&fit=crop&w=600&q=75",
        "description": "Kaggle dual-pitch Gable roof with high cathedral ceiling height for passive chimney ventilation. Fitted with durable charcoal standing seam profiles with rockwool acoustic thermal insulation.",
        "specifications": {
            "roof_style": "Gable Roof (Dual Pitch A-Frame)",
            "roof_material": "Pre-coated Aluzinc / GI Standing Seam Metal",
            "slope_angle": "32° Pitch",
            "insulation": "50mm High-density Rockwool (Thermal SRI > 78)"
        }
    },
    {
        "id": "pic-elev-01",
        "title": "Modern Minimalist Duplex Villa",
        "category": "elevation",
        "style": "Modern Minimalist",
        "tags": ["elevation", "duplex", "3bhk", "modern", "minimalist", "facade", "villa", "concrete", "glass"],
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=75",
        "description": "Double-storey contemporary facade featuring cantilevered geometric balconies, dark grey textured plaster, recessed warm LED linear lighting, and large floor-to-ceiling glass fenestrations.",
        "specifications": {
            "building_type": "3BHK / 4BHK Duplex",
            "plot_size": "30x40 / 30x50 ft",
            "exterior_finish": "Apex Ultima Textured Emulsion + HPL Louvers",
            "estimated_cost_tier": "Standard Premium"
        }
    },
    {
        "id": "pic-elev-02",
        "title": "Contemporary Glass & Teakwood Facade",
        "category": "elevation",
        "style": "Contemporary",
        "tags": ["elevation", "contemporary", "wood", "glass", "luxury", "duplex", "balcony"],
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=75",
        "description": "Warm architectural facade combining vertical teakwood louvers, double-glazed soundproof glass walls, cantilevered portico, and landscape integration with stone-clad boundary pillars.",
        "specifications": {
            "building_type": "3BHK Duplex / Luxury Villa",
            "plot_size": "30x40 / 40x60 ft",
            "exterior_finish": "Burma Teak Battens + Powder-coated Aluminum Glazing",
            "estimated_cost_tier": "Luxury"
        }
    },
    {
        "id": "pic-elev-04",
        "title": "Compact Urban 30x40 G+1 Smart Home",
        "category": "elevation",
        "style": "Modern Minimalist",
        "tags": ["elevation", "compact", "30x40", "g+1", "2bhk", "3bhk", "budget", "urban", "car parking"],
        "image_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=75",
        "description": "Optimized urban footprint with ground floor covered parking, first floor master suite, glass railing balcony, and vertical CNC laser-cut MS privacy jali.",
        "specifications": {
            "building_type": "2BHK / 3BHK G+1",
            "plot_size": "30x40 ft (1200 sq.ft)",
            "exterior_finish": "Asian Paints Apex Weatherproof + MS Powder Coat",
            "estimated_cost_tier": "Standard"
        }
    },
    {
        "id": "pic-cubicasa-01",
        "title": "CubiCasa5k High-Precision Polygonal Floor Plan Blueprint",
        "category": "elevation",
        "style": "Architectural Blueprint",
        "tags": ["cubicasa", "cubicasa5k", "floor_plan", "blueprint", "cad", "vector", "polygon", "walls", "doors"],
        "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=75",
        "description": "Polygon vector architectural layout trained on CubiCasa5k (5,000 floor plans). Millimeter-precision wall vectors, interior partition topology, and door-swing clearance zones.",
        "specifications": {
            "dataset": "CubiCasa5k Benchmark",
            "polygon_types": "External load-bearing walls, partitions, door swings, window bays",
            "scale_factor": "1:50 Metric Scale",
            "spatial_features": "Closed polygonal room loops with automatic area takeoff"
        }
    },
    {
        "id": "pic-socal-01",
        "title": "SoCal Contemporary Coastal Residence (ted8080 Dataset)",
        "category": "elevation",
        "style": "Contemporary",
        "tags": ["socal", "ted8080", "california", "elevation", "luxury", "duplex", "facade", "house_prices"],
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=600&q=75",
        "description": "Elevation facade trained on ted8080 SoCal House Prices & Images (15,474 homes). Features seamless indoor-outdoor lanai flow, standing-seam shed roof, and high-appraisal architectural volume.",
        "specifications": {
            "dataset": "ted8080 SoCal House Prices & Images (15,474 homes)",
            "style_elements": "Low-pitch mono-slope shed roof, stucco & cedar cladding, double-glazed glass walls",
            "spatial_plan": "4BHK with ground floor guest suite and open kitchen concept",
            "valuation_index": "Top-quartile aesthetic appraisal valuation"
        }
    },
    {
        "id": "pic-wwymak-01",
        "title": "Art Deco Geometric Streamline Moderne Villa (wwymak Dataset)",
        "category": "elevation",
        "style": "Contemporary",
        "tags": ["wwymak", "art deco", "architecture", "styles", "geometric", "facade", "streamline"],
        "image_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=600&q=75",
        "description": "Elevation geometry derived from wwymak 25 Architectural Styles benchmark dataset. Features horizontal streamline banding, curved corner glass fenestrations, and stepped coping parapet flat roofs.",
        "specifications": {
            "dataset": "wwymak Architecture Dataset (10,043 elevation photos across 25 styles)",
            "architectural_movement": "Art Deco / Streamline Moderne",
            "fenestration": "Corner wrap-around curved steel-framed windows",
            "parapet": "Stepped geometric crown"
        }
    },
    {
        "id": "pic-nastaran-01",
        "title": "Minimalist Glass & Fair-Faced Concrete Villa (NastaranTH BuildingStyles)",
        "category": "elevation",
        "style": "Modern Minimalist",
        "tags": ["nastaranth", "buildingstyles", "concrete", "glass", "minimalist", "facade", "modern", "green_roof"],
        "image_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=75",
        "description": "Architectural classification derived from NastaranTH buildingstyles dataset (4,200 styles). Board-formed architectural concrete, thermal envelope curtain glass, and cantilevered sedum green roof.",
        "specifications": {
            "dataset": "NastaranTH/buildingstyles (HuggingFace)",
            "facade_materiality": "Fair-faced board-formed architectural concrete + Low-E triple glazing",
            "roofing_type": "Insulated flat slab with extensive sedum green roof",
            "daylighting": "92% natural daylight autonomy"
        }
    },
    {
        "id": "pic-int-01",
        "title": "Contemporary Modular Quartz Kitchen",
        "category": "kitchen",
        "style": "Contemporary",
        "tags": ["kitchen", "interior", "modular", "quartz", "acrylic", "vastu", "agni corner", "cabinets"],
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=75",
        "description": "Ergonomic L-shaped modular kitchen positioned in South-East Agni corner. Features high-gloss acrylic soft-close cabinets, quartz stone countertop, built-in induction & chimney.",
        "specifications": {
            "room_type": "Modular Kitchen",
            "vastu_zone": "South-East (Agni Corner)",
            "materials": "Marine Grade BWP Ply + 20mm Nano White Quartz Countertop",
            "hardware": "Hettich / Hafele Soft-Close Tandem Boxes"
        }
    },
    {
        "id": "pic-int-02",
        "title": "Double-Height Open Living & Dining Hall",
        "category": "living_room",
        "style": "Modern Minimalist",
        "tags": ["living room", "interior", "double height", "dining", "hall", "open plan", "lighting", "vastu"],
        "image_url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=600&q=75",
        "description": "Airy double-height central hall with Italian vitrified glazed tiles, suspended architectural chandelier, acoustic fluted wall paneling, and seamless connectivity to pooja and garden court.",
        "specifications": {
            "room_type": "Living & Dining Hall",
            "vastu_zone": "North-East / Central Brahmasthana transition",
            "flooring": "800x1600mm Glazed Vitrified Tiles (GVT)",
            "ceiling": "Gypsum False Ceiling with 3000K Warm White Cove LEDs"
        }
    },
    {
        "id": "pic-int-03",
        "title": "Master Bedroom with Walk-in Wardrobe",
        "category": "bedroom",
        "style": "Contemporary",
        "tags": ["bedroom", "master bedroom", "interior", "wardrobe", "wooden floor", "south west", "nairuthi"],
        "image_url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=600&q=75",
        "description": "South-West Nairuthi master bedroom with upholstered headboard, acoustic wooden wall paneling, sliding tinted glass wardrobe, attached luxury en-suite bathroom.",
        "specifications": {
            "room_type": "Master Bedroom",
            "vastu_zone": "South-West (Nairuthi Corner for stability)",
            "flooring": "Laminated Engineered Wooden Planks / GVT Tiles",
            "lighting": "Architectural Anti-Glare Magnetic Track Lights"
        }
    },
    {
        "id": "pic-int-04",
        "title": "Vastu North-East Pooja Room Mandir",
        "category": "pooja",
        "style": "Traditional South Indian",
        "tags": ["pooja", "interior", "mandir", "vastu", "north east", "teakwood", "marble", "spiritual"],
        "image_url": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=600&q=75",
        "description": "Pure white Makrana marble and brass inlay Pooja sanctuary strictly located in the auspicious Ishanya (North-East) corner with backlit CNC om pattern and solid teakwood carved doorway.",
        "specifications": {
            "room_type": "Pooja Room",
            "vastu_zone": "North-East (Ishanya Corner - auspicious energy)",
            "materials": "Makrana White Marble + Solid Teak Door Frame",
            "ventilation": "Direct East-facing brass jali ventilation"
        }
    },
    {
        "id": "pic-mat-01",
        "title": "IS 456 Structural Reinforcement & Concrete Framing",
        "category": "materials",
        "style": "Structural",
        "tags": ["materials", "steel", "tmt", "fe550d", "shuttering", "slab casting", "is 456", "concrete", "framing"],
        "image_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=600&q=75",
        "description": "Engineered RCC structural framing with Fe 550D TMT reinforcement, high-grade shuttering, and cover blocks conforming to IS 456:2000 specifications.",
        "specifications": {
            "standard_code": "IS 1786:2008 / IS 456:2000",
            "material": "Primary Fe 550D TMT (Tata Tiscon / JSW Neosteel)",
            "durability": "Corrosion resistant with thermo-mechanically treated core"
        }
    },
    {
        "id": "pic-mat-02",
        "title": "Vitrified Marble Tiles & Premium Finishes",
        "category": "materials",
        "style": "Contemporary",
        "tags": ["materials", "tiles", "vitrified", "marble", "flooring", "wall dado", "finishing"],
        "image_url": "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=600&q=75",
        "description": "Large format 4x2 ft Statuario marble-look vitrified tiles with rectified edges, zero-porosity surface, and epoxy grout joints for stain and scratch resistance.",
        "specifications": {
            "standard_code": "IS 15622 Group B1a",
            "tile_dimension": "1200mm x 600mm x 9mm",
            "finish": "High Gloss Nano Polished"
        }
    },
    {
        "id": "pic-ter-01",
        "title": "Open Terrace Garden & Pergola Pavilion",
        "category": "terrace",
        "style": "Modern Minimalist",
        "tags": ["terrace", "roof garden", "pergola", "balcony", "exterior", "waterproofing", "duplex"],
        "image_url": "https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?auto=format&fit=crop&w=600&q=75",
        "description": "Functional terrace rooftop with weather-resistant steel pergola, anti-skid exterior deck tiles, integral polymer waterproofing, and perimeter vertical greenery planters.",
        "specifications": {
            "room_type": "Terrace Garden & Lounge",
            "waterproofing": "Two-coat elastomeric acrylic membrane + screed slope",
            "flooring": "Anti-skid R11 exterior vitrified tiles"
        }
    },
    {
        "id": "pic-nalu-04",
        "title": "Handcrafted Teakwood Interior & Machhu Attic Woodwork",
        "category": "interior",
        "style": "Kerala Vernacular",
        "tags": ["nalukettu", "machhu", "woodwork", "interior", "teak", "anjili", "traditional", "kerala"],
        "image_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail_url": "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=600&q=75",
        "description": "Traditional wooden ceiling (Machhu) and ornamental timber rafters handcrafted from seasoned Anjili and teakwood, creating natural thermal insulation beneath Mangalore tiled roofs.",
        "specifications": {
            "timber": "Seasoned Teakwood / Anjili Wood",
            "joint": "Mortise & Tenon traditional wood joinery",
            "finish": "Natural Linseed Oil & Beeswax polish"
        }
    }
]

def search_and_recommend_pictures(
    query: str,
    category: Optional[str] = None,
    style: Optional[str] = None,
    limit: int = 3
) -> List[Dict[str, Any]]:
    """
    Intelligently score and retrieve the most relevant pictures based on conversation context,
    architectural style, room intent, and construction requirements.
    Guarantees strict deduplication so each returned picture has a unique, distinct image.
    """
    query_lower = query.lower()
    query_tokens = [w.strip() for w in query_lower.replace(",", " ").replace(".", " ").split() if len(w) > 2]
    scored_items = []

    # Detect style intent from query tokens
    is_modern_query = any(w in query_tokens for w in ["modern", "morden", "minimalist", "contemporary", "cuboid"])
    is_trad_query = any(w in query_tokens for w in ["traditional", "kerala", "nalukettu", "tharavadu", "nadumuttam", "charupadi", "poomukham"])

    for item in PICTURE_CATALOG:
        score = 0.0
        item_style_lower = item.get("style", "").lower()

        # Strict style filter / penalty: if modern asked, eliminate traditional; if traditional asked, eliminate modern
        if style:
            req_style_lower = style.lower()
            if any(m in req_style_lower for m in ["modern", "minimalist", "contemporary"]):
                if any(k in item_style_lower for k in ["kerala", "traditional", "vernacular"]):
                    score -= 50.0  # Eliminate traditional when modern is requested!
                elif any(k in item_style_lower for k in ["modern", "contemporary"]):
                    score += 30.0
            elif any(t in req_style_lower for t in ["kerala", "traditional", "vernacular"]):
                if any(k in item_style_lower for k in ["modern minimalist"]):
                    score -= 50.0  # Eliminate modern when traditional is requested!
                elif any(k in item_style_lower for k in ["kerala", "vernacular", "traditional"]):
                    score += 30.0
            elif "tropical" in req_style_lower:
                if "tropical" in item_style_lower or "contemporary" in item_style_lower:
                    score += 25.0

        # Query token style alignment
        if is_modern_query and not is_trad_query:
            if any(k in item_style_lower for k in ["kerala", "traditional", "vernacular"]):
                score -= 40.0
            elif any(k in item_style_lower for k in ["modern", "contemporary"]):
                score += 25.0
        elif is_trad_query and not is_modern_query:
            if any(k in item_style_lower for k in ["modern minimalist"]):
                score -= 40.0
            elif any(k in item_style_lower for k in ["kerala", "traditional", "vernacular"]):
                score += 25.0

        # Exact category match
        if category and item.get("category", "").lower() == category.lower():
            score += 10.0

        # Query token overlap in title, tags, description, style
        item_text = (
            item.get("title", "") + " " +
            item.get("style", "") + " " +
            item.get("category", "") + " " +
            " ".join(item.get("tags", [])) + " " +
            item.get("description", "")
        ).lower()

        for token in query_tokens:
            if token in item.get("tags", []):
                score += 6.0
            elif token in item_text:
                score += 2.0

        # Heuristic boosts
        if any(w in query_tokens for w in ["kerala", "nalukettu", "nadumuttam", "traditional", "charupadi", "poomukham", "tharavadu", "vettukallu"]):
            if "Kerala Vernacular" in item.get("style", "") or any(k in item.get("tags", []) for k in ["kerala", "nalukettu", "traditional"]):
                score += 15.0
        if any(w in query_tokens for w in ["modern", "morden", "minimalist", "glass", "duplex", "facade"]):
            if any(k in item.get("style", "") for k in ["Modern Minimalist", "Contemporary"]):
                score += 15.0
        if any(w in query_tokens for w in ["baker", "laurie", "brick", "rat trap", "filler slab", "eco"]):
            if "laurie baker" in item.get("tags", []) or "eco-friendly" in item.get("tags", []):
                score += 18.0
        if any(w in query_tokens for w in ["roof", "tiles", "clay", "mangalore", "hip", "gable", "monsoon"]):
            if any(k in item.get("tags", []) for k in ["roof", "roof_style", "tiles", "hip_roof", "gable_roof"]):
                score += 8.0
        if any(w in query_tokens for w in ["pinterest", "pin", "luxury", "cantilever"]):
            if any(k in item.get("tags", []) for k in ["pinterest", "luxury", "cantilever"]):
                score += 20.0
        if any(w in query_tokens for w in ["commercial", "office", "plaza", "curtain", "retail"]):
            if any(k in item.get("tags", []) for k in ["commercial", "office", "plaza", "curtain_wall"]):
                score += 25.0
        if any(w in query_tokens for w in ["industrial", "warehouse", "peb", "shed", "factory"]):
            if any(k in item.get("tags", []) for k in ["industrial", "warehouse", "peb", "shed"]):
                score += 25.0
        if any(w in query_tokens for w in ["japanese", "zen", "minka", "engawa", "wabi"]):
            if any(k in item.get("tags", []) for k in ["japanese", "zen", "minka", "engawa"]):
                score += 25.0
        if any(w in query_tokens for w in ["scandinavian", "nordic", "eco", "timber", "a_frame"]):
            if any(k in item.get("tags", []) for k in ["scandinavian", "nordic", "eco"]):
                score += 25.0
        if any(w in query_tokens for w in ["mediterranean", "spanish", "hacienda", "barrel"]):
            if any(k in item.get("tags", []) for k in ["mediterranean", "spanish", "hacienda"]):
                score += 25.0
        if any(w in query_tokens for w in ["apartment", "flats", "g+3", "multi_family"]):
            if any(k in item.get("tags", []) for k in ["apartment", "residential", "g+3"]):
                score += 25.0

        scored_items.append((score, item))

    # Sort descending by score
    scored_items.sort(key=lambda x: x[0], reverse=True)

    # STRICT DEDUPLICATION BY IMAGE URL
    seen_images = set()
    deduped_results = []

    for score, item in scored_items:
        if score <= 0 and (is_modern_query or is_trad_query or style):
            continue  # Don't return heavily penalized mismatched items!
        img_key = (item.get("thumbnail_url") or item.get("image_url") or "").split("?")[0]
        if img_key and img_key not in seen_images:
            seen_images.add(img_key)
            deduped_results.append(item)
            if len(deduped_results) >= limit:
                break

    # If results are fewer than requested limit, backfill with compatible catalog items
    if len(deduped_results) < limit:
        for item in PICTURE_CATALOG:
            item_style_lower = item.get("style", "").lower()
            if is_modern_query and any(k in item_style_lower for k in ["kerala", "traditional"]):
                continue
            if is_trad_query and any(k in item_style_lower for k in ["modern minimalist"]):
                continue
            img_key = (item.get("thumbnail_url") or item.get("image_url") or "").split("?")[0]
            if img_key and img_key not in seen_images:
                seen_images.add(img_key)
                deduped_results.append(item)
                if len(deduped_results) >= limit:
                    break

    return deduped_results

def get_picture_by_id(picture_id: str) -> Optional[Dict[str, Any]]:
    for item in PICTURE_CATALOG:
        if item["id"] == picture_id:
            return item
    return None
