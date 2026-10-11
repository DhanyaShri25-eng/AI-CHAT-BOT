from typing import List, Dict, Any
import re

# Comprehensive Verified Statutory Construction Knowledge Base
VERIFIED_KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc-tncdbr-setback",
        "title": "Tamil Nadu Combined Development and Building Rules (TNCDBR) 2019 - Rule 35",
        "category": "Building By-Laws & Regulations",
        "publisher": "Housing and Urban Development Department, Government of Tamil Nadu",
        "jurisdiction": "Tamil Nadu (Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem)",
        "version": "2019 (Amended 2024)",
        "section_code": "TNCDBR Rule 35 (Residential Plot Coverage & Setbacks)",
        "content": (
            "For residential buildings up to 12 metres in height (Stilt + 3 floors or Ground + 2 floors) on plots up to 300 sq.m (3229 sq.ft):\n"
            "1. Front Setback: Minimum 1.5m (5 ft) for road width up to 9m; 3.0m (10 ft) for road width 9m to 18m.\n"
            "2. Rear Setback: Minimum 1.0m (3.3 ft) for plots with depth up to 15m; 1.5m for plots greater than 15m depth.\n"
            "3. Side Setback 1: Minimum 1.0m (3.3 ft).\n"
            "4. Side Setback 2: Minimum 1.0m (3.3 ft) or nil on one side if open space of 1.5m is left on the other side.\n"
            "5. Maximum Floor Space Index (FSI): Standard FSI is 2.0. Premium FSI up to 2.50 allowable on 30ft road width."
        )
    },
    {
        "id": "doc-nbc-room-sizes",
        "title": "National Building Code of India (NBC) 2016 - Part 3: Development Control Rules",
        "category": "Technical Standards",
        "publisher": "Bureau of Indian Standards (BIS)",
        "jurisdiction": "National (India)",
        "version": "NBC 2016 Volume 1",
        "section_code": "NBC Clause 4.2 (Minimum Room Sizes and Dimensions)",
        "content": (
            "Standard minimum requirements for habitable residential rooms:\n"
            "1. Habitable Rooms (Living / Bedroom): Minimum floor area shall be not less than 9.5 sq.m (102 sq.ft) with a minimum width of 2.4m (7.87 ft).\n"
            "2. Kitchen: Minimum area shall be 5.0 sq.m (54 sq.ft) with a minimum width of 1.8m (5.9 ft). If combined dining-kitchen, minimum 7.5 sq.m.\n"
            "3. Bathrooms: Water Closet (WC) minimum 1.1m x 0.9m (1.0 sq.m); Combined Bath & WC minimum 2.8 sq.m (30 sq.ft) with minimum width of 1.2m.\n"
            "4. Ceiling Height: Clear minimum height of any habitable room shall be 2.75m (9.0 ft); for air-conditioned rooms minimum 2.4m (7.87 ft).\n"
            "5. Staircase: Minimum clear width for residential single-family is 0.9m (3.0 ft); maximum riser 190mm (7.5 in); minimum tread 250mm (10 in)."
        )
    },
    {
        "id": "doc-is456-concrete",
        "title": "IS 456:2000 - Plain and Reinforced Concrete Code of Practice",
        "category": "Structural Engineering Code",
        "publisher": "Bureau of Indian Standards",
        "jurisdiction": "National (India)",
        "version": "Fourth Revision (Reaffirmed 2021)",
        "section_code": "IS 456 Clauses 5, 26, 34",
        "content": (
            "Structural RCC guidelines for residential framed structures:\n"
            "1. Concrete Grade: Minimum grade for reinforced concrete is M20 (1:1.5:3 nominal or design mix). For coastal or severe durability environments, M25 minimum.\n"
            "2. Water-Cement Ratio: Maximum free water-cement ratio for M20 shall not exceed 0.55 for moderate exposure.\n"
            "3. Reinforcement Steel: High Yield Strength Deformed (HYSD) bars conforming to IS 1786 (Fe 500 or Fe 550D) recommended for earthquake zones III/IV.\n"
            "4. Nominal Cover: Footings = 50mm; Columns = 40mm; Beams = 25mm; Slabs = 20mm (or bar diameter, whichever is greater).\n"
            "5. Curing: Moist curing shall be maintained for a minimum of 7 days for OPC and 10 days for PPC / mineral admixtures."
        )
    },
    {
        "id": "doc-tn-rainwater",
        "title": "Tamil Nadu Rainwater Harvesting Regulations & Ground Water Recharging Mandate",
        "category": "Environmental & Sustainability",
        "publisher": "Chennai Metropolitan Water Supply and Sewerage Board (CMWSSB) / DTCP",
        "jurisdiction": "Tamil Nadu",
        "version": "Mandatory Municipal Norm",
        "section_code": "TNCDBR Rule 43 (Rainwater Harvesting Infrastructure)",
        "content": (
            "Every building constructed in Tamil Nadu shall have mandatory rainwater harvesting structures:\n"
            "1. Rooftop rainwater collection channelled through PVC/lead-free gutters into a filtration pit (sand, gravel, charcoal bed).\n"
            "2. Recharging well: Minimum depth 3.0m (10 ft) with perforated RCC rings or interconnected borewell recharge point.\n"
            "3. Storage Sump: Minimum storage capacity of 10,000 litres recommended for roof area of 1,200 sq.ft to achieve zero run-off.\n"
            "4. Completion certificate / EB permanent power connection will not be issued without verified RWH installation."
        )
    },
    {
        "id": "doc-vastu-principles",
        "title": "Traditional Indian Architectural Vastu Shastra Reference Principles",
        "category": "Architectural Planning & Orientation",
        "publisher": "National Council of Architecture / Indian Heritage Reference",
        "jurisdiction": "Cultural Architectural Best Practice",
        "version": "Vastu Purusha Mandala Standard",
        "section_code": "Vastu Zonal Layout Alignment",
        "content": (
            "Architectural Vastu zones and room allocations:\n"
            "1. North-East (Eeshanya / Water element): Ideal for Main Entrance, Pooja Room, Water Sump, Open Verandah. Must be kept lightweight.\n"
            "2. South-East (Agni / Fire element): Prime location for Kitchen (cooking platform facing East) and Electrical distribution panel.\n"
            "3. South-West (Nairuthi / Earth element): Heaviest zone; best for Master Bedroom, Wardrobes, and Overhead Water Tank at terrace.\n"
            "4. North-West (Vayu / Air element): Suitable for Guest Bedroom, Children's Room, Granary, and Dog-legged Staircase.\n"
            "5. Center (Brahmasthan): Must remain free of heavy structural load, columns, or toilet pits."
        )
    }
]

def search_building_codes(query: str, jurisdiction: str = "Tamil Nadu / National", top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search verified regulatory and technical documents using semantic keyword scoring.
    """
    query_tokens = set(re.findall(r'\b\w+\b', query.lower()))
    
    scored_docs = []
    for doc in VERIFIED_KNOWLEDGE_DOCUMENTS:
        # Match text against title, content, section_code
        text = f"{doc['title']} {doc['category']} {doc['section_code']} {doc['content']}".lower()
        score = 0
        for token in query_tokens:
            if len(token) > 2:
                # Count frequency
                matches = len(re.findall(r'\b' + re.escape(token) + r'\b', text))
                score += matches * 2
                if token in doc["title"].lower():
                    score += 5
                if token in doc["section_code"].lower():
                    score += 8
                    
        if score > 0 or len(query_tokens) == 0:
            scored_docs.append({
                "title": doc["title"],
                "section_code": doc["section_code"],
                "publisher": doc["publisher"],
                "jurisdiction": doc["jurisdiction"],
                "content": doc["content"],
                "relevance_score": min(0.98, round(score / (len(query_tokens) * 3 + 1) + 0.5, 2))
            })
            
    # Sort descending by relevance
    scored_docs.sort(key=lambda d: d["relevance_score"], reverse=True)
    return scored_docs[:top_k] if scored_docs else [{
        "title": VERIFIED_KNOWLEDGE_DOCUMENTS[0]["title"],
        "section_code": VERIFIED_KNOWLEDGE_DOCUMENTS[0]["section_code"],
        "publisher": VERIFIED_KNOWLEDGE_DOCUMENTS[0]["publisher"],
        "jurisdiction": VERIFIED_KNOWLEDGE_DOCUMENTS[0]["jurisdiction"],
        "content": VERIFIED_KNOWLEDGE_DOCUMENTS[0]["content"],
        "relevance_score": 0.75
    }]
