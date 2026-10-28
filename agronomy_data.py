"""
Agronomic Reference Knowledge Base for Indian Agriculture
=========================================================
Contains authentic agronomic requirements for crops, regional soil classifications,
and agro-climatic profiles based on standard Indian agricultural research bodies:
- Indian Council of Agricultural Research (ICAR)
- National Bureau of Soil Survey and Land Use Planning (NBSS&LUP)
- Directorate of Economics and Statistics (DES), Ministry of Agriculture & Farmers Welfare
- Tamil Nadu Agricultural University (TNAU) Agritech Portal
- Food and Agriculture Organization (FAO) - Crop Water Information

This reference module is used by the Agricultural Intelligence Dashboard
to compare actual historical measurements with established agronomic benchmarks.
"""

from typing import Dict, Any, Tuple

# Mapping of CSV state names to GeoJSON property 'ST_NM'
STATE_NAME_GEOJSON_MAP: Dict[str, str] = {
    "Jammu and Kashmir": "Jammu & Kashmir",
}

def get_state_geojson_name(csv_state_name: str) -> str:
    """Returns the matching ST_NM in the GeoJSON boundary dataset."""
    return STATE_NAME_GEOJSON_MAP.get(csv_state_name, csv_state_name)


# ==============================================================================
# 1. STATE SOIL AND AGRO-CLIMATIC PROFILES
# Source: ICAR - NBSS&LUP & Planning Commission Agro-Climatic Regional Planning
# ==============================================================================
STATE_AGRO_PROFILES: Dict[str, Dict[str, Any]] = {
    "Andhra Pradesh": {
        "soils": ["Red Sandy Loam", "Coastal Alluvial", "Black Cotton Soil", "Laterite"],
        "zone": "Southern Plateau and Hills / East Coast Plains",
        "climate_desc": "Semi-arid to tropical wet-and-dry with monsoon influence",
        "primary_season": "Kharif & Rabi",
        "source": "ICAR-NBSS&LUP State Soil Survey"
    },
    "Arunachal Pradesh": {
        "soils": ["Red Loamy", "Forest & Mountain Soils", "Alluvial (Valleys)"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Sub-tropical to alpine with high annual rainfall",
        "primary_season": "Kharif / Whole Year",
        "source": "ICAR-NBSS&LUP North Eastern Regional Centre"
    },
    "Assam": {
        "soils": ["Alluvial (Brahmaputra Valley)", "Red & Lateritic", "Peaty / Marshy"],
        "zone": "Eastern Himalayan / Upper Brahmaputra Plains",
        "climate_desc": "Humid sub-tropical with heavy monsoon precipitation",
        "primary_season": "Autumn, Winter & Summer Rice (Ahu, Sali, Boro)",
        "source": "Assam Agricultural University & ICAR"
    },
    "Bihar": {
        "soils": ["Alluvial (North & South Ganga Plains)", "Sandy Loam", "Calcareous"],
        "zone": "Middle Gangetic Plain Region",
        "climate_desc": "Sub-tropical monsoon with hot summers and mild winters",
        "primary_season": "Kharif, Rabi & Zaid",
        "source": "ICAR-RCER Patna & NBSS&LUP"
    },
    "Chhattisgarh": {
        "soils": ["Red and Yellow (Matasi)", "Red Sandy (Bhatha)", "Black Soil (Kanhar)"],
        "zone": "Eastern Plateau and Hills Region",
        "climate_desc": "Tropical wet and dry (known as the 'Rice Bowl of Central India')",
        "primary_season": "Kharif (dominantly rainfed rice)",
        "source": "Indira Gandhi Krishi Vishwavidyalaya (IGKV) & NBSS&LUP"
    },
    "Delhi": {
        "soils": ["Alluvial Soils", "Sandy Loam"],
        "zone": "Upper Gangetic Plain / Trans-Gangetic Plain",
        "climate_desc": "Semi-arid with extreme temperatures (hot summers, chilly winters)",
        "primary_season": "Kharif & Rabi",
        "source": "ICAR-IARI New Delhi"
    },
    "Goa": {
        "soils": ["Laterite Soils", "Coastal Alluvium", "Sandy Loam"],
        "zone": "West Coast Plains and Ghats",
        "climate_desc": "Humid maritime tropical with heavy southwest monsoon",
        "primary_season": "Kharif (Sorod) & Rabi (Vaingan)",
        "source": "ICAR-Central Coastal Agricultural Research Institute (CCARI)"
    },
    "Gujarat": {
        "soils": ["Medium Black Soil", "Alluvial (North Gujarat)", "Saline / Alkaline (Kutch)", "Sandy Loam (Goradu)"],
        "zone": "Gujarat Plains and Hills Region",
        "climate_desc": "Semi-arid to arid in north/west; sub-humid in south",
        "primary_season": "Kharif & Rabi",
        "source": "Anand Agricultural University & ICAR-NBSS&LUP"
    },
    "Haryana": {
        "soils": ["Alluvial Soil (Sierozem)", "Sandy Loam", "Light Loam"],
        "zone": "Trans-Gangetic Plains Region",
        "climate_desc": "Semi-arid with extensive canal and tubewell irrigation network",
        "primary_season": "Kharif & Rabi",
        "source": "CCS Haryana Agricultural University & ICAR"
    },
    "Himachal Pradesh": {
        "soils": ["Brown Hill Soils", "Mountain / Forest Soils", "Sub-montane Podzolic"],
        "zone": "Western Himalayan Region",
        "climate_desc": "Temperate to sub-tropical in valleys; cold alpine in high altitudes",
        "primary_season": "Kharif & Rabi (Horticultural focus)",
        "source": "Dr. Y.S. Parmar University of Horticulture & Forestry"
    },
    "Jammu and Kashmir": {
        "soils": ["Mountain Meadow Soils", "Alluvial (Karewas of Kashmir)", "Brown Forest Soils"],
        "zone": "Western Himalayan Region",
        "climate_desc": "Temperate continental in Kashmir; sub-tropical in Jammu",
        "primary_season": "Kharif & Rabi",
        "source": "SKUAST Jammu & Kashmir / ICAR"
    },
    "Jharkhand": {
        "soils": ["Red Sandy Soils", "Lateritic Soils", "Gravelly Loams"],
        "zone": "Eastern Plateau and Hills Region",
        "climate_desc": "Sub-humid tropical with undulating plateau topography",
        "primary_season": "Kharif (predominantly rainfed)",
        "source": "Birsa Agricultural University & NBSS&LUP"
    },
    "Karnataka": {
        "soils": ["Red Loamy & Sandy (South Interior)", "Black Soil / Regur (North Interior)", "Lateritic (Coastal)"],
        "zone": "Southern Plateau and Hills / Coastal Plains",
        "climate_desc": "Semi-arid in Deccan plateau; humid maritime in coastal Konkan/Malabar",
        "primary_season": "Kharif, Rabi & Summer",
        "source": "University of Agricultural Sciences Bengaluru/Dharwad & ICAR"
    },
    "Kerala": {
        "soils": ["Laterite Soils (65% area)", "Coastal Alluvium", "Red Loam", "Forest Loam", "Acid Peaty (Kari)"],
        "zone": "West Coast Plains and Ghats Region",
        "climate_desc": "Tropical maritime with dual monsoons (SW & NE), high humidity",
        "primary_season": "Virippu (Autumn), Mundakan (Winter), Puncha (Summer)",
        "source": "Kerala Agricultural University (KAU) & NBSS&LUP"
    },
    "Madhya Pradesh": {
        "soils": ["Deep & Medium Black Soils (Malwa/Nimar)", "Alluvial (Chambal)", "Red & Yellow (Bundelkhand/Baghelkhand)"],
        "zone": "Central Plateau and Hills Region",
        "climate_desc": "Sub-tropical with distinct monsoon; major pulse & oilseed producer",
        "primary_season": "Kharif & Rabi",
        "source": "JNKVV Jabalpur & ICAR-IISS Bhopal"
    },
    "Maharashtra": {
        "soils": ["Black Cotton Soil (Regur/Vertisols)", "Laterite (Konkan)", "Coarse Shallow (Western Ghats)"],
        "zone": "Western Plateau and Hills Region",
        "climate_desc": "Semi-arid rain-shadow in Marathwada/Vidarbha; wet coastal Konkan",
        "primary_season": "Kharif & Rabi",
        "source": "MPKV Rahuri, PDKV Akola & ICAR-NBSS&LUP Nagpur"
    },
    "Manipur": {
        "soils": ["Red Loamy", "Alluvial (Imphal Valley)", "Lateritic"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Sub-tropical temperate with wet monsoon summers",
        "primary_season": "Kharif",
        "source": "Central Agricultural University Imphal"
    },
    "Meghalaya": {
        "soils": ["Red & Yellow Loams", "Laterite Soils", "Acidic Hill Soils"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Hyper-humid tropical montane (one of the wettest regions globally)",
        "primary_season": "Kharif / Whole Year",
        "source": "ICAR Research Complex for NEH Region, Umiam"
    },
    "Mizoram": {
        "soils": ["Red Sandy Loam", "Clayey Loam", "Forest Soils"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Moist tropical to sub-tropical with steep hill slope agriculture",
        "primary_season": "Kharif",
        "source": "ICAR NEH Regional Centre Mizoram"
    },
    "Nagaland": {
        "soils": ["Ferruginous Red Soils", "Clayey Loams", "Humus-rich Forest Soils"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Humid sub-tropical with terraced and jhum farming traditions",
        "primary_season": "Kharif",
        "source": "Nagaland University School of Agricultural Sciences & ICAR"
    },
    "Odisha": {
        "soils": ["Red Loamy", "Laterite", "Coastal Alluvial", "Black Soils (Western districts)"],
        "zone": "East Coast Plains and Hills Region",
        "climate_desc": "Tropical with coastal cyclonic events and strong southwest monsoon",
        "primary_season": "Kharif & Rabi",
        "source": "OUAT Bhubaneswar & ICAR-NRRI Cuttack"
    },
    "Puducherry": {
        "soils": ["Coastal Alluvium", "Red Loam", "Sedimentary Clay"],
        "zone": "East Coast Plains and Hills",
        "climate_desc": "Maritime tropical with northeast winter monsoon peaks",
        "primary_season": "Navarai, Sornavari, Samba",
        "source": "Department of Agriculture Puducherry & TNAU"
    },
    "Punjab": {
        "soils": ["Alluvial Soil (Typic Ustochrepts)", "Sandy Loam", "Silt Loam"],
        "zone": "Trans-Gangetic Plains Region",
        "climate_desc": "Semi-arid continental with intensive canal and tubewell irrigation",
        "primary_season": "Kharif (Rice/Cotton) & Rabi (Wheat)",
        "source": "Punjab Agricultural University (PAU) Ludhiana & ICAR"
    },
    "Sikkim": {
        "soils": ["Brown Forest Soils", "Podzolic Mountain Soils", "Acidic Hill Soils"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Temperate to alpine; certified 100% organic agricultural state",
        "primary_season": "Kharif & Rabi",
        "source": "ICAR National Organic Farming Research Institute (NOFRI) Tadong"
    },
    "Tamil Nadu": {
        "soils": ["Red Loam (Alfisols)", "Black Cotton (Vertisols)", "Coastal Alluvium", "Laterite"],
        "zone": "Southern Plateau and Hills / East Coast Plains",
        "climate_desc": "Tropical semi-arid with major precipitation from Northeast Monsoon (Oct-Dec)",
        "primary_season": "Kuruvai, Samba/Thaladi, Navarai",
        "source": "Tamil Nadu Agricultural University (TNAU) Coimbatore"
    },
    "Telangana": {
        "soils": ["Red Sandy Loam (Chalka 48%)", "Deep Black Cotton (Vertisols 25%)", "Laterite"],
        "zone": "Southern Plateau and Hills Region",
        "climate_desc": "Semi-arid tropical with hot dry summers and moderate monsoon",
        "primary_season": "Kharif (Vanakkalam) & Rabi (Yasangi)",
        "source": "PJTSAU Hyderabad & ICAR-CRIDA"
    },
    "Tripura": {
        "soils": ["Red and Yellow Soils", "Alluvial (River Valleys)", "Lateritic"],
        "zone": "Eastern Himalayan Region",
        "climate_desc": "Warm humid sub-tropical with plentiful rainfall",
        "primary_season": "Aush, Aman & Boro Rice",
        "source": "ICAR Research Complex Tripura Centre"
    },
    "Uttar Pradesh": {
        "soils": ["Alluvial Soil (Ganga-Yamuna Doab)", "Clayey Loam", "Red Sandy (Bundelkhand)"],
        "zone": "Upper & Middle Gangetic Plains",
        "climate_desc": "Humid sub-tropical with fertile multi-cropping plains",
        "primary_season": "Kharif, Rabi & Zaid",
        "source": "ICAR-IISR Lucknow & CSAUA&T Kanpur"
    },
    "Uttarakhand": {
        "soils": ["Brown Forest Soils", "Sub-Himalayan Hill Soils", "Alluvial (Tarai Region)"],
        "zone": "Western Himalayan Region",
        "climate_desc": "Sub-tropical in Tarai plains to cold temperate in montane hills",
        "primary_season": "Kharif & Rabi",
        "source": "G.B. Pant University of Agriculture and Technology (GBPUAT) Pantnagar"
    },
    "West Bengal": {
        "soils": ["Alluvial (Gangetic Plains)", "Red & Laterite (Purulia/Bankura)", "Coastal Saline (Sundarbans)", "Brown Hill (Darjeeling)"],
        "zone": "Lower Gangetic Plain & Eastern Himalayan",
        "climate_desc": "Tropical wet-and-dry to humid sub-tropical with intensive multi-season rice",
        "primary_season": "Aus, Aman & Boro",
        "source": "Bidhan Chandra Krishi Viswavidyalaya (BCKV) & ICAR"
    }
}


# ==============================================================================
# 2. CROP AGRONOMIC INTELLIGENCE PROFILES (55 CROPS)
# Sourced from: ICAR, TNAU Agritech Portal, FAO Crop Water Information
# ==============================================================================
CROP_AGRONOMIC_PROFILES: Dict[str, Dict[str, Any]] = {
    "Rice": {
        "category": "Cereal Grain",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Clay Loam", "Alluvial", "Silty Clay"],
        "water_req_mm": (1000, 1500),
        "temp_range_c": (20, 38),
        "season": "Kharif (Monsoon), Autumn & Summer (Boro)",
        "duration_days": (100, 150),
        "stages": [
            {"stage": "Sowing & Nursery", "pct": 18, "desc": "Seed germination and seedling raising in wet nurseries."},
            {"stage": "Transplanting & Tillering", "pct": 27, "desc": "Field puddling, seedling transplantation, and vigorous tiller emergence under standing water."},
            {"stage": "Panicle Initiation & Flowering", "pct": 30, "desc": "Critical water-sensitive reproductive phase where panicles emerge."},
            {"stage": "Grain Filling & Maturity", "pct": 25, "desc": "Milk to dough stage; water drained 10-15 days prior to harvest."}
        ],
        "source": "ICAR-National Rice Research Institute (NRRI) & FAO Land & Water"
    },
    "Wheat": {
        "category": "Cereal Grain",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Alluvial", "Clay Loam", "Silt Loam"],
        "water_req_mm": (450, 650),
        "temp_range_c": (10, 25),
        "season": "Rabi (Winter)",
        "duration_days": (100, 140),
        "stages": [
            {"stage": "Sowing & Crown Root Initiation (CRI)", "pct": 20, "desc": "First critical irrigation required at CRI stage (21 days after sowing)."},
            {"stage": "Tillering & Jointing", "pct": 30, "desc": "Rapid shoot and leaf area expansion under cool winter conditions."},
            {"stage": "Heading & Anthesis", "pct": 25, "desc": "Spike emergence and flowering; highly sensitive to sudden heat stress."},
            {"stage": "Dough & Physiological Ripening", "pct": 25, "desc": "Grain hardening as temperatures rise in spring before golden harvest."}
        ],
        "source": "ICAR-Indian Institute of Wheat and Barley Research (IIWBR)"
    },
    "Maize": {
        "category": "Cereal Grain",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Sandy Loam", "Alluvial", "Well-drained Black Soil"],
        "water_req_mm": (500, 800),
        "temp_range_c": (18, 30),
        "season": "Kharif, Rabi & Spring",
        "duration_days": (85, 120),
        "stages": [
            {"stage": "Germination & Early Vegetative", "pct": 20, "desc": "Knee-high stage; sensitive to waterlogging."},
            {"stage": "Tasseling & Silking", "pct": 35, "desc": "Peak water requirement; moisture stress during silking drastically impairs cob yield."},
            {"stage": "Grain Development", "pct": 25, "desc": "Kernel starch accumulation and cob expansion."},
            {"stage": "Dent & Maturity", "pct": 20, "desc": "Black layer formation at grain base signaling physiological ripeness."}
        ],
        "source": "ICAR-Indian Institute of Maize Research (IIMR)"
    },
    "Sugarcane": {
        "category": "Cash & Commercial",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Alluvial", "Medium Heavy Black Soils", "Loamy Soils with good drainage"],
        "water_req_mm": (1500, 2500),
        "temp_range_c": (20, 35),
        "season": "Whole Year (Perennial 10-14 months)",
        "duration_days": (300, 365),
        "stages": [
            {"stage": "Germination Phase", "pct": 15, "desc": "Bud sprouting and initial set establishment (up to 45 days)."},
            {"stage": "Formative & Tillering", "pct": 25, "desc": "Cane tillering and primary root system development (45-120 days)."},
            {"stage": "Grand Growth Phase", "pct": 40, "desc": "Rapid cane elongation and internode thickening with maximum water uptake."},
            {"stage": "Ripening & Sucrose Accumulation", "pct": 20, "desc": "Vegetative growth slows and sucrose synthesis peaks under cooler, dry weather."}
        ],
        "source": "ICAR-Indian Institute of Sugarcane Research (IISR)"
    },
    "Cotton(lint)": {
        "category": "Fiber & Cash Crop",
        "reporting_unit": "Bales of 170 kg",
        "soils": ["Deep Black Cotton Soil (Regur/Vertisols)", "Alluvial", "Red Sandy Loam"],
        "water_req_mm": (700, 1200),
        "temp_range_c": (21, 35),
        "season": "Kharif (Monsoon to Winter)",
        "duration_days": (150, 190),
        "stages": [
            {"stage": "Germination & Seedling", "pct": 15, "desc": "Square formation initiation; weed control is vital."},
            {"stage": "Squaring & Flowering", "pct": 35, "desc": "Yellow floral blooms open; sensitive to bollworm attacks and severe drought."},
            {"stage": "Boll Formation & Filling", "pct": 30, "desc": "Boll expansion and lint fiber development inside capsules."},
            {"stage": "Boll Bursting & Picking", "pct": 20, "desc": "Bolls burst open to display fluffy white lint; picked across 2-3 passes."}
        ],
        "source": "ICAR-Central Institute for Cotton Research (CICR)"
    },
    "Coconut": {
        "category": "Plantation Crop",
        "reporting_unit": "Thousand Nuts / Number of Nuts",
        "soils": ["Coastal Alluvium", "Lateritic Soils", "Red Sandy Loam"],
        "water_req_mm": (1300, 2300),
        "temp_range_c": (24, 34),
        "season": "Whole Year (Perennial Palm)",
        "duration_days": (365, 365),
        "stages": [
            {"stage": "Inflorescence Emergence", "pct": 25, "desc": "Spathe opening and female flower (button) emergence in leaf axils."},
            {"stage": "Button Setting & Young Nut", "pct": 25, "desc": "Pollination and tender nut development (tender coconut stage)."},
            {"stage": "Endosperm Development", "pct": 25, "desc": "Kernel formation and water volume transition inside the shell."},
            {"stage": "Maturity & Harvest", "pct": 25, "desc": "11-12 month cycle for copra harvest; bunches harvested monthly."}
        ],
        "source": "Coconut Development Board (CDB) & ICAR-CPCRI"
    },
    "Gram": {
        "category": "Pulse",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Sandy Loam to Clay Loam", "Light Alluvial", "Black Cotton Soil"],
        "water_req_mm": (250, 400),
        "temp_range_c": (15, 28),
        "season": "Rabi (Winter)",
        "duration_days": (90, 120),
        "stages": [
            {"stage": "Germination & Branching", "pct": 25, "desc": "Nipping/topping at 30-40 days to encourage extensive lateral branching."},
            {"stage": "Flowering Stage", "pct": 35, "desc": "Pink/white pea-like flowers; frost or sudden rainfall can induce flower drop."},
            {"stage": "Pod Development", "pct": 25, "desc": "Chickpea grain expansion within inflated pods."},
            {"stage": "Desiccation & Harvest", "pct": 15, "desc": "Foliage turns reddish-brown and leaves shed as pods dry."}
        ],
        "source": "ICAR-Indian Institute of Pulses Research (IIPR)"
    },
    "Arhar/Tur": {
        "category": "Pulse",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Alluvial", "Deep Red Soils", "Black Cotton Soils"],
        "water_req_mm": (600, 850),
        "temp_range_c": (20, 35),
        "season": "Kharif to Late Rabi",
        "duration_days": (150, 240),
        "stages": [
            {"stage": "Vegetative Branching", "pct": 35, "desc": "Deep taproot development making it highly drought tolerant."},
            {"stage": "Flower Bud Induction", "pct": 25, "desc": "Indeterminate flowering across multiple flushes."},
            {"stage": "Pod Filling", "pct": 25, "desc": "Pigeon pea seed enlargement; vulnerable to pod borers."},
            {"stage": "Pod Maturation", "pct": 15, "desc": "Leaves dry and drop; pods turn brown ready for threshing."}
        ],
        "source": "ICAR-IIPR Kanpur & ICRISAT"
    },
    "Groundnut": {
        "category": "Oilseed",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Sandy Loam", "Red Sandy", "Light Alluvial (Loose soil for peg penetration)"],
        "water_req_mm": (500, 700),
        "temp_range_c": (22, 32),
        "season": "Kharif & Summer / Rabi",
        "duration_days": (100, 130),
        "stages": [
            {"stage": "Emergence & Vegetative", "pct": 20, "desc": "Taproot establishment and symbiotic nitrogen-fixing nodule growth."},
            {"stage": "Flowering & Pegging", "pct": 35, "desc": "After pollination, pegs bend downward and penetrate loose soil to develop underground pods."},
            {"stage": "Pod Enlargement", "pct": 30, "desc": "Subterranean kernel development; soil moisture is crucial."},
            {"stage": "Harvest Maturity", "pct": 15, "desc": "Inner pod shell turns dark brown; plants pulled for field drying."}
        ],
        "source": "ICAR-Directorate of Groundnut Research (DGR)"
    },
    "Soyabean": {
        "category": "Oilseed & Pulse",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Vertisols (Black Soil)", "Loamy Alluvium"],
        "water_req_mm": (450, 700),
        "temp_range_c": (20, 32),
        "season": "Kharif (Monsoon)",
        "duration_days": (90, 110),
        "stages": [
            {"stage": "Germination & Trifoliate Emergence", "pct": 20, "desc": "Rhizobial nodulation and canopy expansion."},
            {"stage": "Flowering Flushes", "pct": 30, "desc": "Small purple/white flowers form along main stems and branches."},
            {"stage": "Pod Filling", "pct": 35, "desc": "Bean starch and oil deposition; moisture stress reduces seed size."},
            {"stage": "Defoliation & Ripening", "pct": 15, "desc": "Leaves yellow and drop completely, leaving clusters of dry pods."}
        ],
        "source": "ICAR-Indian Institute of Soybean Research (IISR) Indore"
    },
    "Rapeseed &Mustard": {
        "category": "Oilseed",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Sandy Loam to Clay Loam", "Alluvial Soils"],
        "water_req_mm": (300, 450),
        "temp_range_c": (10, 25),
        "season": "Rabi (Winter)",
        "duration_days": (105, 140),
        "stages": [
            {"stage": "Seedling & Rosette", "pct": 25, "desc": "Basal foliage rosette forms under cool autumn/winter weather."},
            {"stage": "Bolting & Golden Inflorescence", "pct": 30, "desc": "Bright yellow flowering canopy; susceptible to aphid infestation."},
            {"stage": "Siliqua (Pod) Development", "pct": 25, "desc": "Elongated pods fill with tiny high-oil oilseeds."},
            {"stage": "Harvest Dryness", "pct": 20, "desc": "Pods turn straw-yellow; harvested early morning to avoid seed shattering."}
        ],
        "source": "ICAR-Directorate of Rapeseed-Mustard Research (DRMR) Bharatpur"
    },
    "Potato": {
        "category": "Vegetable & Tuber",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Loose Sandy Loam", "Alluvial", "Humus-rich Loam"],
        "water_req_mm": (500, 700),
        "temp_range_c": (15, 24),
        "season": "Rabi (Plains) & Summer (Hills)",
        "duration_days": (80, 120),
        "stages": [
            {"stage": "Sprout Emergence", "pct": 20, "desc": "Seed tuber sprouting and underground stolon initiation."},
            {"stage": "Tuberization Induction", "pct": 30, "desc": "Stolon tips swell to initiate tubers; night temperatures <20°C are crucial."},
            {"stage": "Tuber Bulking", "pct": 35, "desc": "Rapid starch deposition and tuber sizing requiring consistent light irrigation."},
            {"stage": "Haulm Senescence & Skin Hardening", "pct": 15, "desc": "Vines dehaulmed 10-15 days prior to digging to set tuber skin."}
        ],
        "source": "ICAR-Central Potato Research Institute (CPRI) Shimla"
    },
    "Onion": {
        "category": "Vegetable & Condiment",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Sandy Loam", "Alluvial Loam", "Clay Loam with organic matter"],
        "water_req_mm": (400, 600),
        "temp_range_c": (13, 30),
        "season": "Kharif, Late Kharif & Rabi",
        "duration_days": (110, 150),
        "stages": [
            {"stage": "Nursery & Transplanting", "pct": 25, "desc": "6-7 week old seedlings transplanted into raised beds or flat beds."},
            {"stage": "Vegetative Leaf Emergence", "pct": 30, "desc": "Foliage sheath production; determines future bulb size potential."},
            {"stage": "Bulbing Stage", "pct": 30, "desc": "Triggered by day length and warm temperature; leaf bases swell."},
            {"stage": "Neck Fall & Curing", "pct": 15, "desc": "Tops collapse naturally at neck; bulbs lifted and sun-cured."}
        ],
        "source": "ICAR-Directorate of Onion and Garlic Research (DOGR) Pune"
    },
    "Jute": {
        "category": "Fiber & Cash Crop",
        "reporting_unit": "Bales of 180 kg",
        "soils": ["Rich Alluvial", "Sandy Loam", "River Delta Silt"],
        "water_req_mm": (1000, 1500),
        "temp_range_c": (24, 38),
        "season": "Kharif (Pre-monsoon to Monsoon)",
        "duration_days": (120, 150),
        "stages": [
            {"stage": "Germination & Weeding", "pct": 20, "desc": "Rapid early emergence in hot humid conditions."},
            {"stage": "Stem Elongation", "pct": 45, "desc": "Unbranched tall reed-like stalks grow up to 3-4 meters."},
            {"stage": "Pod Emergence / Small Pod Stage", "pct": 20, "desc": "Best fiber quality obtained when harvested at early pod stage."},
            {"stage": "Retting & Fiber Extraction", "pct": 15, "desc": "Bundles submerged in slow-moving water for biological retting."}
        ],
        "source": "ICAR-Central Research Institute for Jute and Allied Fibres (CRIJAF)"
    },
    "Banana": {
        "category": "Fruit & Plantation",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Rich Clay Loam", "Alluvial", "Well-drained Coastal Soil"],
        "water_req_mm": (1200, 2000),
        "temp_range_c": (20, 35),
        "season": "Whole Year",
        "duration_days": (300, 365),
        "stages": [
            {"stage": "Vegetative Growth", "pct": 40, "desc": "Pseudostem expansion and broad leaf emergence from underground rhizome."},
            {"stage": "Shooting & Bunch Emergence", "pct": 25, "desc": "Inflorescence pushes through central throat and bends downward."},
            {"stage": "Fruit Development & Fingers Filling", "pct": 25, "desc": "Hands of bananas swell; bunch covers placed for protection."},
            {"stage": "Harvest Ripeness", "pct": 10, "desc": "Fingers become less angular and turn rounded dark-green."}
        ],
        "source": "ICAR-National Research Centre for Banana (NRCB) Tiruchirappalli"
    },
    "Bajra": {
        "category": "Coarse Cereal / Millet",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Sandy Loam", "Light Alluvial", "Arid Sandy Soils"],
        "water_req_mm": (350, 500),
        "temp_range_c": (22, 38),
        "season": "Kharif (Monsoon)",
        "duration_days": (80, 100),
        "stages": [
            {"stage": "Seedling & Tillering", "pct": 25, "desc": "Exceptional drought and heat tolerance mechanism kicks in."},
            {"stage": "Stem Elongation & Booting", "pct": 30, "desc": "Erect cylindrical spiky head emerges inside leaf sheath."},
            {"stage": "Flowering & Grain Filling", "pct": 30, "desc": "Protogynous flowering; pearl-like grains fill the dense spike."},
            {"stage": "Maturity", "pct": 15, "desc": "Earheads turn brownish-grey and grains harden."}
        ],
        "source": "ICAR-Indian Institute of Millets Research (IIMR) Hyderabad"
    },
    "Jowar": {
        "category": "Coarse Cereal / Millet",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Black Cotton Soil (Regur)", "Clayey Loam", "Alluvial"],
        "water_req_mm": (400, 600),
        "temp_range_c": (20, 35),
        "season": "Kharif & Rabi",
        "duration_days": (95, 125),
        "stages": [
            {"stage": "Vegetative & Root Expansion", "pct": 30, "desc": "Extensive adventitious root system develops to combat drought."},
            {"stage": "Booting & Panicle Emergence", "pct": 30, "desc": "Large floral panicle emerges at the top of the canopy."},
            {"stage": "Grain Filling", "pct": 25, "desc": "Sorghum grains swell from milky to dough phase."},
            {"stage": "Physiological Maturity", "pct": 15, "desc": "Hardened grains display black layer at hilum."}
        ],
        "source": "ICAR-Indian Institute of Millets Research (IIMR)"
    },
    "Ragi": {
        "category": "Coarse Cereal / Nutri-Cereal",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Red Loam", "Sandy Loam", "Lateritic"],
        "water_req_mm": (350, 550),
        "temp_range_c": (18, 32),
        "season": "Kharif & Summer",
        "duration_days": (95, 125),
        "stages": [
            {"stage": "Seedling & Tillering", "pct": 25, "desc": "Fine fibrous roots establish; finger millet tillers aggressively."},
            {"stage": "Finger Head Emergence", "pct": 35, "desc": "Characteristic digitated floral head resembling open bird fingers emerges."},
            {"stage": "Grain Filling", "pct": 25, "desc": "Tiny calcium- and iron-rich grains develop on finger spikelets."},
            {"stage": "Maturity & Drying", "pct": 15, "desc": "Earheads turn brown and curve inward."}
        ],
        "source": "ICAR-IIMR & TNAU Agritech Portal"
    },
    "Barley": {
        "category": "Cereal Grain",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Sandy Loam to Loamy Alluvium", "Saline/Alkaline tolerant"],
        "water_req_mm": (300, 450),
        "temp_range_c": (12, 25),
        "season": "Rabi (Winter)",
        "duration_days": (90, 120),
        "stages": [
            {"stage": "Crown Root & Tillering", "pct": 25, "desc": "Hardy winter cereal adapted to dry and saline soils."},
            {"stage": "Stem Elongation & Heading", "pct": 35, "desc": "Awned spikes emerge; tolerant to moisture stress compared to wheat."},
            {"stage": "Grain Development", "pct": 25, "desc": "Grains fill rapidly before summer heat arrives."},
            {"stage": "Golden Ripeness", "pct": 15, "desc": "Moisture content drops below 14% for malting/grain harvest."}
        ],
        "source": "ICAR-IIWBR Karnal"
    },
    "Moong(Green Gram)": {
        "category": "Pulse",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Loam", "Sandy Loam", "Alluvial"],
        "water_req_mm": (300, 450),
        "temp_range_c": (22, 35),
        "season": "Kharif, Summer & Spring",
        "duration_days": (60, 75),
        "stages": [
            {"stage": "Quick Germination", "pct": 20, "desc": "Short-duration crop suited for catch cropping and green manuring."},
            {"stage": "Flowering Flushes", "pct": 35, "desc": "Yellow blooms appear in leaf axils; indeterminate growth."},
            {"stage": "Pod Filling", "pct": 30, "desc": "Slender green pods turn dark as green gram seeds fill."},
            {"stage": "Pod Drying & Picking", "pct": 15, "desc": "Pods harvested in 2 picking cycles to avoid shattering."}
        ],
        "source": "ICAR-IIPR Kanpur"
    },
    "Urad": {
        "category": "Pulse",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Loamy Alluvial", "Black Cotton Soil", "Clay Loam"],
        "water_req_mm": (350, 500),
        "temp_range_c": (22, 35),
        "season": "Kharif, Rabi (Rice fallows) & Summer",
        "duration_days": (70, 90),
        "stages": [
            {"stage": "Vegetative Canopy", "pct": 25, "desc": "Dense trifoliate leaves with rich nitrogen-fixing root nodules."},
            {"stage": "Flowering", "pct": 35, "desc": "Clustered pale-yellow flowers form along racemes."},
            {"stage": "Pod Development", "pct": 25, "desc": "Erect cylindrical hairy pods fill with black seeds."},
            {"stage": "Harvest", "pct": 15, "desc": "Pods turn blackish-grey; plants cut close to ground."}
        ],
        "source": "ICAR-IIPR Kanpur"
    },
    "Turmeric": {
        "category": "Spice & Condiment",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Sandy Clay Loam", "Red Loam", "Alluvial Loam"],
        "water_req_mm": (1000, 1600),
        "temp_range_c": (20, 35),
        "season": "Kharif to Whole Year (9 months)",
        "duration_days": (240, 270),
        "stages": [
            {"stage": "Rhizome Sprouting", "pct": 20, "desc": "Mother rhizomes emerge through thick mulch under warm monsoon showers."},
            {"stage": "Vegetative Tillering", "pct": 35, "desc": "Broad green leaves form; continuous moist root environment required."},
            {"stage": "Rhizome Bulking", "pct": 30, "desc": "Finger and mother rhizomes accumulate curcumin pigment and starch."},
            {"stage": "Foliage Drying & Harvest", "pct": 15, "desc": "Leaves turn yellow and dry completely; rhizomes carefully dug."}
        ],
        "source": "ICAR-Indian Institute of Spices Research (IISR) Kozhikode"
    },
    "Ginger": {
        "category": "Spice & Condiment",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Rich Humus Loam", "Sandy Loam", "Lateritic Loam"],
        "water_req_mm": (1200, 1800),
        "temp_range_c": (19, 32),
        "season": "Kharif to Whole Year (8-9 months)",
        "duration_days": (210, 260),
        "stages": [
            {"stage": "Sprouting Phase", "pct": 20, "desc": "Rhizome seed pieces germinate under heavy straw/leaf mulching."},
            {"stage": "Tillering & Shoot Elongation", "pct": 40, "desc": "Multiple pseudostems form with light, frequent irrigation."},
            {"stage": "Rhizome Expansion", "pct": 25, "desc": "Pungent ginger fingers expand underground."},
            {"stage": "Senescence & Digging", "pct": 15, "desc": "Stems yellow and lodge; rhizomes harvested for green or dry ginger."}
        ],
        "source": "ICAR-Indian Institute of Spices Research (IISR)"
    },
    "Black pepper": {
        "category": "Spice & Plantation",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Virgin Red Laterite", "Forest Loam (Western Ghats)"],
        "water_req_mm": (1500, 2500),
        "temp_range_c": (20, 35),
        "season": "Whole Year (Perennial Vine)",
        "duration_days": (365, 365),
        "stages": [
            {"stage": "Flushing & Spike Emergence", "pct": 25, "desc": "Spikes emerge on vine nodes following early summer pre-monsoon showers."},
            {"stage": "Pollination & Berry Setting", "pct": 30, "desc": "Rainwater-mediated pollination along hanging spikes."},
            {"stage": "Berry Enlargement", "pct": 30, "desc": "Green berries swell along 8-15 cm hanging spikes."},
            {"stage": "Harvest Maturity", "pct": 15, "desc": "One or two berries in each spike turn red/orange, signaling harvest."}
        ],
        "source": "ICAR-IISR Kozhikode & Spices Board India"
    },
    "Cardamom": {
        "category": "Spice & Plantation",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Forest Loam rich in organic matter", "Acidic Hill Soil (pH 5.0-6.0)"],
        "water_req_mm": (1500, 3000),
        "temp_range_c": (10, 32),
        "season": "Whole Year (Perennial Shade Crop)",
        "duration_days": (365, 365),
        "stages": [
            {"stage": "Panicle Emergence", "pct": 25, "desc": "Floral tillers emerge from base of pseudostem in evergreen forest shade."},
            {"stage": "Flowering & Bee Pollination", "pct": 35, "desc": "White and violet lip flowers visited by honeybees."},
            {"stage": "Capsule Development", "pct": 25, "desc": "Three-celled green capsules develop along decumbent panicles."},
            {"stage": "Picking & Curing", "pct": 15, "desc": "Capsules harvested at 30-40 day intervals and cured in curing houses."}
        ],
        "source": "Indian Cardamom Research Institute (ICRI) & Spices Board"
    },
    "Dry chillies": {
        "category": "Spice & Cash Crop",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Well-drained Black Soils", "Sandy Loam", "Alluvial"],
        "water_req_mm": (600, 900),
        "temp_range_c": (20, 35),
        "season": "Kharif & Rabi",
        "duration_days": (120, 160),
        "stages": [
            {"stage": "Transplanting & Growth", "pct": 25, "desc": "Hardy nursery seedlings planted on ridges or raised beds."},
            {"stage": "Branching & Flowering", "pct": 30, "desc": "White solitary flowers initiate continuous pod setting."},
            {"stage": "Fruit Maturation", "pct": 30, "desc": "Green pods transition to bright glossy red with capsaicin synthesis."},
            {"stage": "Harvest & Sun Drying", "pct": 15, "desc": "Ripe red chillies hand-picked and spread on drying yards."}
        ],
        "source": "TNAU Agritech Portal & Spices Board India"
    },
    "Garlic": {
        "category": "Spice & Vegetable",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Rich Sandy Loam", "Well-drained Alluvial", "Clay Loam"],
        "water_req_mm": (400, 600),
        "temp_range_c": (12, 28),
        "season": "Rabi (Winter)",
        "duration_days": (120, 150),
        "stages": [
            {"stage": "Clove Sprouting", "pct": 20, "desc": "Individual cloves planted root-down; roots establish in cool soil."},
            {"stage": "Vegetative Foliage", "pct": 35, "desc": "Flat strap-like leaves form; frost resistant."},
            {"stage": "Bulb Differentiation", "pct": 30, "desc": "Underground bulb divides into compound cloves within papery sheath."},
            {"stage": "Maturity & Curing", "pct": 15, "desc": "Leaves dry down 60-70%; bulbs lifted and cured in shade."}
        ],
        "source": "ICAR-Directorate of Onion and Garlic Research (DOGR)"
    },
    "Sunflower": {
        "category": "Oilseed",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Black Soils", "Sandy Loam", "Alluvial"],
        "water_req_mm": (400, 600),
        "temp_range_c": (18, 32),
        "season": "Kharif, Rabi & Spring",
        "duration_days": (85, 105),
        "stages": [
            {"stage": "Emergence & Star Stage", "pct": 25, "desc": "Rapid early vegetative development with heliotropic flower tracking."},
            {"stage": "Ray Floret Opening & Anthesis", "pct": 30, "desc": "Golden disc opens; insect pollination ensures high seed set."},
            {"stage": "Achene (Seed) Filling", "pct": 30, "desc": "Oil and protein deposition inside head; high water need."},
            {"stage": "Bract Senescence", "pct": 15, "desc": "Back of the sunflower head turns lemony yellow to brown."}
        ],
        "source": "ICAR-Indian Institute of Oilseeds Research (IIOR) Hyderabad"
    },
    "Tobacco": {
        "category": "Commercial & Cash Crop",
        "reporting_unit": "Metric Tonnes",
        "soils": ["Deep Black Soils (FCV)", "Light Sandy Loam", "Alluvial"],
        "water_req_mm": (500, 750),
        "temp_range_c": (20, 35),
        "season": "Rabi / Autumn",
        "duration_days": (110, 140),
        "stages": [
            {"stage": "Seedling to Rosette", "pct": 25, "desc": "Tiny seeds raised in specialized nursery beds then transplanted."},
            {"stage": "Rapid Leaf Elongation", "pct": 35, "desc": "Large broad commercial leaves expand; topping removes flower bud."},
            {"stage": "Desuckering & Leaf Ripening", "pct": 25, "desc": "Axillary suckers removed so plant energy concentrates into cured leaf body."},
            {"stage": "Priming & Curing", "pct": 15, "desc": "Leaves harvested leaf-by-leaf as they ripen from bottom upwards."}
        ],
        "source": "ICAR-Central Tobacco Research Institute (CTRI) Rajahmundry"
    }
}

# Default fallback generator for crops not explicitly itemized in deep detail
DEFAULT_AGRONOMIC_TEMPLATE = {
    "category": "Field Crop / Miscellaneous",
    "reporting_unit": "Metric Tonnes",
    "soils": ["Loamy Alluvial", "Sandy Loam", "Clay Loam"],
    "water_req_mm": (400, 750),
    "temp_range_c": (18, 32),
    "season": "Kharif / Rabi",
    "duration_days": (90, 130),
    "stages": [
        {"stage": "Germination & Early Vegetative", "pct": 25, "desc": "Root establishment and canopy emergence."},
        {"stage": "Active Growth & Tillering", "pct": 35, "desc": "Biomass accumulation and flowering bud induction."},
        {"stage": "Seed/Fruit Development", "pct": 25, "desc": "Grain or fruit bulking phase."},
        {"stage": "Ripening & Harvest", "pct": 15, "desc": "Desiccation and physiological harvest readiness."}
    ],
    "source": "ICAR General Agronomy Manual & Directorate of Economics and Statistics"
}

def get_crop_profile(crop_name: str) -> Dict[str, Any]:
    """Retrieves the agronomic benchmark profile for any crop with graceful fallback."""
    clean_name = crop_name.strip()
    if clean_name in CROP_AGRONOMIC_PROFILES:
        return CROP_AGRONOMIC_PROFILES[clean_name]
    
    # Generic category heuristics
    res = dict(DEFAULT_AGRONOMIC_TEMPLATE)
    lower = clean_name.lower()
    if "pulse" in lower or "gram" in lower:
        res["category"] = "Pulse"
        res["water_req_mm"] = (300, 500)
    elif "oilseed" in lower or "seed" in lower:
        res["category"] = "Oilseed"
        res["water_req_mm"] = (350, 600)
    elif "millet" in lower:
        res["category"] = "Nutri-Cereal / Millet"
        res["water_req_mm"] = (300, 450)
    elif "nut" in lower or "coconut" in lower or "arecanut" in lower:
        res["category"] = "Plantation Crop"
        res["reporting_unit"] = "Thousand Nuts / Number of Nuts"
        res["water_req_mm"] = (1200, 2000)
    return res

def get_state_profile(state_name: str) -> Dict[str, Any]:
    """Retrieves regional soil types, agro-climatic zone and source citation for a state."""
    clean_name = state_name.strip()
    return STATE_AGRO_PROFILES.get(clean_name, {
        "soils": ["Alluvial Loam", "Red Sandy", "Black Soil"],
        "zone": "Indian Agro-Climatic Region",
        "climate_desc": "Sub-tropical to tropical monsoon",
        "primary_season": "Kharif & Rabi",
        "source": "ICAR-NBSS&LUP General Soil Survey"
    })
