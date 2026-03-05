"""
SmartCropX — Pesticide Recommendation Knowledge Base.

Maps (disease, crop) pairs to recommended pesticide, dosage, and instructions.
Covers five crops: Tomato, Rice, Wheat, Cotton, Potato.
"""

from typing import Optional, List, Dict

# ── Top-level KB: disease → crop-specific map ──────────────────────
# Each entry: { "pesticide": ..., "dosage": ..., "instructions": ... }

PESTICIDE_KB: Dict[str, Dict[str, dict]] = {
    # ── Tomato diseases ─────────────────────────────────────────────
    "early blight": {
        "Tomato": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.0–2.5 g/L of water",
            "instructions": (
                "Spray at first sign of brown concentric-ring lesions on lower leaves. "
                "Repeat every 7–10 days. Avoid spraying in direct sunlight. "
                "Pre-harvest interval: 5 days."
            ),
            "precautions": [
                "Wear protective gloves and mask while spraying.",
                "Do not apply within 5 days of harvest.",
                "Avoid spraying in windy conditions to prevent drift.",
            ],
        },
        "Potato": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": (
                "Apply preventively when conditions favour blight (warm, humid). "
                "Repeat at 7–14 day intervals. Do not mix with alkaline pesticides."
            ),
            "precautions": [
                "Do not mix with alkaline pesticides.",
                "Use personal protective equipment during application.",
                "Observe a 7-day pre-harvest interval.",
            ],
        },
        "_default": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Apply as foliar spray every 7–10 days at first symptom appearance.",
            "precautions": [
                "Wear gloves, mask, and eye protection.",
                "Avoid inhalation of spray mist.",
                "Keep away from water bodies.",
            ],
        },
    },
    "late blight": {
        "Tomato": {
            "pesticide": "Metalaxyl + Mancozeb (Ridomil Gold 68% WP)",
            "dosage": "2.5 g/L of water",
            "instructions": (
                "Use when night temperatures drop below 15 °C and humidity > 90 %. "
                "Alternate with contact fungicide to delay resistance. "
                "Maximum 3 applications per season."
            ),
            "precautions": [
                "Maximum 3 applications per season to prevent resistance.",
                "Do not apply during strong winds.",
                "Wash hands and exposed skin after handling.",
            ],
        },
        "Potato": {
            "pesticide": "Cymoxanil + Mancozeb",
            "dosage": "3.0 g/L of water",
            "instructions": (
                "Begin applications before disease onset during rainy periods. "
                "Repeat at 5–7 day intervals under high disease pressure."
            ),
            "precautions": [
                "Do not spray immediately before expected rainfall.",
                "Keep children and livestock away during spraying.",
                "Store unused solution safely away from food items.",
            ],
        },
        "_default": {
            "pesticide": "Metalaxyl + Mancozeb",
            "dosage": "2.5 g/L of water",
            "instructions": "Spray preventively in cool-wet conditions. Repeat every 7 days.",
            "precautions": [
                "Alternate with contact fungicides to manage resistance.",
                "Wear full protective clothing.",
                "Do not contaminate water sources.",
            ],
        },
    },
    "leaf curl": {
        "Tomato": {
            "pesticide": "Imidacloprid 17.8% SL (for whitefly vector)",
            "dosage": "0.3 mL/L of water",
            "instructions": (
                "Leaf curl is caused by Tomato Leaf Curl Virus transmitted by whiteflies. "
                "Control the vector with Imidacloprid. Remove and destroy infected plants. "
                "Use yellow sticky traps for monitoring."
            ),
            "precautions": [
                "Toxic to bees — avoid spraying during flowering.",
                "Do not apply near beehives or pollinator habitat.",
                "Wear mask and gloves during preparation and application.",
            ],
        },
        "Cotton": {
            "pesticide": "Thiamethoxam 25% WG",
            "dosage": "0.2 g/L of water",
            "instructions": (
                "Target whitefly population early in the season. "
                "Rotate with different chemistry to manage resistance."
            ),
            "precautions": [
                "Harmful to aquatic organisms — do not contaminate water.",
                "Rotate insecticide classes to delay resistance.",
                "Use protective equipment during application.",
            ],
        },
        "_default": {
            "pesticide": "Imidacloprid 17.8% SL",
            "dosage": "0.3 mL/L of water",
            "instructions": "Control insect vector (whiteflies) to manage viral leaf curl.",
            "precautions": [
                "Toxic to pollinators — do not spray on flowering crops.",
                "Wear protective gear during application.",
                "Keep away from fish ponds and water bodies.",
            ],
        },
    },
    "bacterial wilt": {
        "Tomato": {
            "pesticide": "Streptomycin Sulphate + Tetracycline (Streptocycline)",
            "dosage": "0.5 g/10 L of water (soil drench)",
            "instructions": (
                "Apply as soil drench around the root zone of affected plants. "
                "Uproot severely wilted plants to prevent spread. "
                "Use disease-free seedlings and practice crop rotation."
            ),
            "precautions": [
                "Avoid contact with skin — use rubber gloves.",
                "Do not mix with other chemicals.",
                "Dispose of uprooted plant material by burning.",
            ],
        },
        "Potato": {
            "pesticide": "Copper Oxychloride 50% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Drench soil after removing infected tubers. Rotate with non-solanaceous crops.",
            "precautions": [
                "Avoid repeated use in the same field to prevent copper accumulation.",
                "Wear gloves and eye protection.",
                "Do not apply to waterlogged soil.",
            ],
        },
        "_default": {
            "pesticide": "Streptocycline",
            "dosage": "0.5 g/10 L of water",
            "instructions": "Soil drench around roots. Remove infected plants.",
            "precautions": [
                "Use gloves when handling infected plants.",
                "Do not mix with other agrochemicals.",
                "Practice crop rotation for at least 3 years.",
            ],
        },
    },
    "fusarium wilt": {
        "Tomato": {
            "pesticide": "Carbendazim 50% WP",
            "dosage": "1.0 g/L of water (soil drench)",
            "instructions": (
                "Apply soil drench at transplanting. Repeat 15 days later. "
                "Use resistant varieties (F1 hybrids). Maintain soil pH 6.5–7.0."
            ),
            "precautions": [
                "Avoid excessive application — may affect beneficial soil organisms.",
                "Wear gloves and wash hands after use.",
                "Do not eat, drink, or smoke during application.",
            ],
        },
        "Cotton": {
            "pesticide": "Trichoderma viride (bio-agent)",
            "dosage": "10 g/kg seed (seed treatment) or 2.5 kg/ha (soil application)",
            "instructions": "Mix with FYM and apply at sowing. Complements chemical control.",
            "precautions": [
                "Store bio-agent in cool, dry place away from sunlight.",
                "Do not mix with chemical fungicides.",
                "Apply in the evening for best results.",
            ],
        },
        "_default": {
            "pesticide": "Carbendazim 50% WP",
            "dosage": "1.0 g/L of water",
            "instructions": "Soil drench at planting. Use resistant cultivars.",
            "precautions": [
                "Avoid skin contact — use protective gloves.",
                "Do not apply near water sources.",
                "Maintain recommended dosage — over-use promotes resistance.",
            ],
        },
    },
    "powdery mildew": {
        "Wheat": {
            "pesticide": "Propiconazole 25% EC (Tilt)",
            "dosage": "1.0 mL/L of water",
            "instructions": (
                "Spray at the first appearance of white powdery patches on leaves. "
                "One or two sprays at 15-day intervals are usually sufficient."
            ),
            "precautions": [
                "Do not exceed 2 applications per season.",
                "Observe a 35-day pre-harvest interval.",
                "Keep away from eyes — flush with water if contact occurs.",
            ],
        },
        "Tomato": {
            "pesticide": "Sulphur 80% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Dust or spray at early symptom stage. Avoid application above 35 °C.",
            "precautions": [
                "Do not apply when temperature exceeds 35 °C — may cause leaf burn.",
                "Avoid mixing with oil-based sprays.",
                "Wear dust mask during application.",
            ],
        },
        "_default": {
            "pesticide": "Sulphur 80% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Apply as dust or spray at first symptom. Avoid hot conditions.",
            "precautions": [
                "Avoid application in extreme heat (>35 °C).",
                "Use protective clothing and mask.",
                "Store in a cool, dry, ventilated area.",
            ],
        },
    },
    "rust": {
        "Wheat": {
            "pesticide": "Propiconazole 25% EC",
            "dosage": "1.0 mL/L of water",
            "instructions": (
                "Spray at first appearance of orange-brown pustules. "
                "Prefer resistant varieties like HD-3226. "
                "A second spray may be needed after 15 days under severe pressure."
            ),
            "precautions": [
                "Avoid spraying during strong wind.",
                "Observe pre-harvest interval of 35 days.",
                "Do not allow spray solution to contact edible parts directly.",
            ],
        },
        "_default": {
            "pesticide": "Propiconazole 25% EC",
            "dosage": "1.0 mL/L of water",
            "instructions": "Spray at first pustule appearance. Repeat after 15 days if needed.",
            "precautions": [
                "Wear gloves and long sleeves during application.",
                "Avoid contact with eyes and skin.",
                "Do not contaminate feed or foodstuffs.",
            ],
        },
    },
    "brown spot": {
        "Rice": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.5 g/L of water",
            "instructions": (
                "Apply when lesions appear on leaves at tillering or booting stage. "
                "Ensure balanced N-P-K fertilisation — deficiency of potassium worsens the disease."
            ),
            "precautions": [
                "Wear protective gear — avoid inhalation.",
                "Do not apply in standing water deeper than 5 cm.",
                "Safe interval: 5 days before grain harvest.",
            ],
        },
        "_default": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.5 g/L of water",
            "instructions": "Foliar spray when lesions appear. Ensure balanced nutrition.",
            "precautions": [
                "Use mask and gloves.",
                "Avoid contamination of water bodies.",
                "Observe recommended waiting period before harvest.",
            ],
        },
    },
    "blast": {
        "Rice": {
            "pesticide": "Tricyclazole 75% WP",
            "dosage": "0.6 g/L of water",
            "instructions": (
                "Spray at panicle initiation and repeated 10 days later. "
                "Avoid excessive nitrogen fertiliser. "
                "Use resistant varieties (e.g., Swarnamukhi, Pusa Basmati 1)."
            ),
            "precautions": [
                "Do not enter treated field for 24 hours.",
                "Wear full protective clothing during application.",
                "Avoid excessive nitrogen fertilisation to reduce susceptibility.",
            ],
        },
        "_default": {
            "pesticide": "Tricyclazole 75% WP",
            "dosage": "0.6 g/L of water",
            "instructions": "Spray at panicle initiation. Limit excess nitrogen.",
            "precautions": [
                "Wear mask, gloves, and protective clothing.",
                "Do not spray near water sources used for drinking.",
                "Wait 21 days before harvesting grain.",
            ],
        },
    },
    "sheath blight": {
        "Rice": {
            "pesticide": "Hexaconazole 5% EC",
            "dosage": "2.0 mL/L of water",
            "instructions": (
                "Spray at boot-leaf stage when water-soaked lesions appear on sheaths. "
                "Drain excess water from the field before application."
            ),
            "precautions": [
                "Drain field water before application for better efficacy.",
                "Avoid application during rain.",
                "Wear protective gloves and avoid skin contact.",
            ],
        },
        "_default": {
            "pesticide": "Hexaconazole 5% EC",
            "dosage": "2.0 mL/L of water",
            "instructions": "Spray on sheaths at symptom onset. Drain excess standing water.",
            "precautions": [
                "Use protective gear.",
                "Do not apply immediately before irrigation.",
                "Store in original container in a cool place.",
            ],
        },
    },
    "bacterial leaf blight": {
        "Rice": {
            "pesticide": "Copper Hydroxide 77% WP (Kocide)",
            "dosage": "2.0 g/L of water",
            "instructions": (
                "Apply at first sign of water-soaked lesions on leaf tips. "
                "Drain the field, reduce nitrogen, and apply potash. "
                "Biological option: seed treatment with Pseudomonas fluorescens @ 10 g/kg."
            ),
            "precautions": [
                "Repeated copper use may lead to soil toxicity — rotate treatments.",
                "Do not apply with acidic pesticides.",
                "Avoid skin and eye contact.",
            ],
        },
        "_default": {
            "pesticide": "Copper Hydroxide 77% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Spray at first symptom. Reduce nitrogen and improve drainage.",
            "precautions": [
                "Wear protective gear during application.",
                "Avoid excessive copper accumulation in soil.",
                "Keep away from aquatic habitats.",
            ],
        },
    },
    "boll rot": {
        "Cotton": {
            "pesticide": "Copper Oxychloride 50% WP",
            "dosage": "3.0 g/L of water",
            "instructions": (
                "Spray during boll formation when humidity is high. "
                "Remove rotten bolls from the field. "
                "Maintain proper plant spacing for air circulation."
            ),
            "precautions": [
                "Avoid copper accumulation — do not exceed recommended dose.",
                "Wear mask and gloves.",
                "Remove and destroy rotten bolls to prevent spread.",
            ],
        },
        "_default": {
            "pesticide": "Copper Oxychloride 50% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Spray during boll formation in humid conditions.",
            "precautions": [
                "Use protective equipment.",
                "Do not mix with other chemicals without expert advice.",
                "Dispose of empty containers safely.",
            ],
        },
    },
    "bollworm": {
        "Cotton": {
            "pesticide": "Emamectin Benzoate 5% SG",
            "dosage": "0.4 g/L of water",
            "instructions": (
                "Spray at 50 % flowering when larval counts exceed ETL. "
                "Install pheromone traps for monitoring. "
                "Rotate with Spinosad to manage resistance."
            ),
            "precautions": [
                "Highly toxic to fish — do not spray near water bodies.",
                "Rotate with other insecticide classes to prevent resistance.",
                "Do not apply more than twice per season.",
            ],
        },
        "_default": {
            "pesticide": "Emamectin Benzoate 5% SG",
            "dosage": "0.4 g/L of water",
            "instructions": "Spray when larval population exceeds economic threshold.",
            "precautions": [
                "Toxic to aquatic life — keep away from water bodies.",
                "Wear full protective clothing.",
                "Follow resistance management guidelines.",
            ],
        },
    },
    "aphids": {
        "Wheat": {
            "pesticide": "Dimethoate 30% EC",
            "dosage": "1.5 mL/L of water",
            "instructions": (
                "Spray when aphid colonies appear on ear heads. "
                "A single well-timed spray at ear-head stage is usually sufficient."
            ),
            "precautions": [
                "Highly toxic — handle with extreme care.",
                "Do not spray on a windy day.",
                "Observe a 14-day pre-harvest interval.",
            ],
        },
        "Cotton": {
            "pesticide": "Imidacloprid 17.8% SL",
            "dosage": "0.3 mL/L of water",
            "instructions": "Spray on undersides of leaves where colonies concentrate.",
            "precautions": [
                "Toxic to bees — spray in the evening when pollinators are inactive.",
                "Do not contaminate water bodies.",
                "Wash exposed skin thoroughly after use.",
            ],
        },
        "Potato": {
            "pesticide": "Thiamethoxam 25% WG",
            "dosage": "0.2 g/L of water",
            "instructions": "Systemic action — spray as soon as aphid colonies are noticed.",
            "precautions": [
                "Harmful to pollinators — avoid use during flowering.",
                "Do not apply near aquatic habitats.",
                "Use recommended dosage only.",
            ],
        },
        "_default": {
            "pesticide": "Dimethoate 30% EC",
            "dosage": "1.5 mL/L of water",
            "instructions": "Spray on affected foliage. Target undersides of leaves.",
            "precautions": [
                "Wear full protective clothing — toxic by inhalation.",
                "Keep children and livestock away from treated area.",
                "Do not spray near water sources.",
            ],
        },
    },
    "black scurf": {
        "Potato": {
            "pesticide": "Carbendazim 50% WP (seed tuber treatment)",
            "dosage": "2.0 g/L of water (dip tubers for 15 min)",
            "instructions": (
                "Treat seed potatoes before planting by dipping in solution for 15 minutes. "
                "Avoid planting infected tubers. Practice 3-year crop rotation."
            ),
            "precautions": [
                "Wear waterproof gloves during tuber dipping.",
                "Do not reuse treatment solution.",
                "Store treated tubers in a cool, ventilated place.",
            ],
        },
        "_default": {
            "pesticide": "Carbendazim 50% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Seed/tuber treatment before planting.",
            "precautions": [
                "Handle with protective gloves.",
                "Avoid contact with skin and eyes.",
                "Dispose of solution safely — do not pour into drains.",
            ],
        },
    },
    "common scab": {
        "Potato": {
            "pesticide": "Sulphur Dust / Soil acidification",
            "dosage": "25 kg/ha (broadcast before planting)",
            "instructions": (
                "Maintain soil pH below 5.5 by incorporating sulphur. "
                "Irrigate uniformly during tuber initiation. "
                "No effective chemical spray — cultural control is primary."
            ),
            "precautions": [
                "Wear dust mask when broadcasting sulphur.",
                "Check soil pH before application to avoid over-acidification.",
                "Keep sulphur away from ignition sources.",
            ],
        },
        "_default": {
            "pesticide": "Sulphur Dust",
            "dosage": "25 kg/ha",
            "instructions": "Lower soil pH with sulphur before planting. Keep moisture uniform.",
            "precautions": [
                "Use respiratory protection when handling dust.",
                "Test soil pH before application.",
                "Flammable — store away from heat.",
            ],
        },
    },
    "septoria leaf spot": {
        "Tomato": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": (
                "Spray at first appearance of small dark spots with grey centres. "
                "Repeat every 7–10 days. Remove lower infected leaves to reduce inoculum."
            ),
            "precautions": [
                "Irritant — avoid contact with skin and eyes.",
                "Observe a 7-day pre-harvest interval.",
                "Do not apply near fish ponds or water courses.",
            ],
        },
        "_default": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Spray at symptom onset. Remove infected plant debris.",
            "precautions": [
                "Wear protective clothing.",
                "Avoid inhalation of spray mist.",
                "Keep away from aquatic environments.",
            ],
        },
    },
    "anthracnose": {
        "Tomato": {
            "pesticide": "Mancozeb 75% WP + Carbendazim 50% WP",
            "dosage": "Mancozeb 2.0 g + Carbendazim 1.0 g per litre of water",
            "instructions": (
                "Apply when fruit starts ripening. "
                "Avoid overhead irrigation. Harvest promptly."
            ),
            "precautions": [
                "Do not apply after fruit colour break for edible crops.",
                "Wear gloves and face shield.",
                "Avoid overhead irrigation to reduce disease spread.",
            ],
        },
        "_default": {
            "pesticide": "Mancozeb + Carbendazim combination",
            "dosage": "2.0 g + 1.0 g per litre",
            "instructions": "Spray on fruits at colour-break stage. Avoid wetting fruits.",
            "precautions": [
                "Wear protective gear during mixing and spraying.",
                "Do not mix more solution than needed.",
                "Observe safe waiting period before harvest.",
            ],
        },
    },
    "mosaic virus": {
        "Tomato": {
            "pesticide": "No chemical cure — vector control with Imidacloprid 17.8% SL",
            "dosage": "0.3 mL/L of water (for aphid/thrip vectors)",
            "instructions": (
                "Remove and destroy infected plants immediately. "
                "Control sucking pests (aphids, thrips) to limit virus spread. "
                "Use virus-free certified seeds."
            ),
            "precautions": [
                "Burn or bury infected plants — do not compost.",
                "Disinfect tools after handling infected material.",
                "Toxic to bees — spray in the evening only.",
            ],
        },
        "Potato": {
            "pesticide": "Imidacloprid 17.8% SL (vector control)",
            "dosage": "0.3 mL/L of water",
            "instructions": "Control aphid vectors. Use virus-free seed tubers.",
            "precautions": [
                "Avoid spraying on flowering crops — harmful to pollinators.",
                "Handle with gloves and protective gear.",
                "Sterilise cutting tools between plants.",
            ],
        },
        "_default": {
            "pesticide": "Imidacloprid 17.8% SL (vector control)",
            "dosage": "0.3 mL/L of water",
            "instructions": "No direct cure. Control insect vectors and remove infected plants.",
            "precautions": [
                "Destroy infected plant material by burning.",
                "Toxic to pollinators — avoid flowering-period application.",
                "Use virus-free seeds and certified planting material.",
            ],
        },
    },
    "healthy": {
        "_default": {
            "pesticide": "None required",
            "dosage": "N/A",
            "instructions": (
                "Your plant appears healthy! Continue good agricultural practices: "
                "balanced fertilisation, proper irrigation, crop rotation, and regular scouting."
            ),
            "precautions": [],
        },
    },
}

# All supported crops for the dropdown
SUPPORTED_CROPS = ["Tomato", "Rice", "Wheat", "Cotton", "Potato"]


def lookup_pesticide(disease: str, crop: Optional[str] = None) -> dict:
    """
    Look up pesticide recommendation for a given disease (+optional crop).
    Returns dict with keys: pesticide, dosage, instructions, disease, crop, matched.
    """
    disease_lower = disease.strip().lower()
    crop_title = crop.strip().title() if crop else None

    # Try exact key match first, then fuzzy substring match
    entry = PESTICIDE_KB.get(disease_lower)
    if entry is None:
        # fuzzy: if the user typed part of the disease name, try to match
        for key in PESTICIDE_KB:
            if key in disease_lower or disease_lower in key:
                entry = PESTICIDE_KB[key]
                disease_lower = key
                break

    if entry is None:
        return {
            "pesticide": "Consult local agricultural extension officer",
            "dosage": "N/A",
            "instructions": (
                f"No specific pesticide mapping found for '{disease}'. "
                "Please consult your nearest Krishi Vigyan Kendra (KVK) or "
                "agricultural extension officer for expert advice."
            ),
            "precautions": [
                "Always consult a certified agricultural expert before applying any pesticide.",
            ],
            "disease": disease,
            "crop": crop_title or "Unknown",
            "matched": False,
        }

    # Try crop-specific, then _default
    if crop_title and crop_title in entry:
        rec = entry[crop_title]
    elif "_default" in entry:
        rec = entry["_default"]
    else:
        rec = list(entry.values())[0]

    return {
        "pesticide": rec["pesticide"],
        "dosage": rec["dosage"],
        "instructions": rec["instructions"],
        "precautions": rec.get("precautions", []),
        "disease": disease_lower.title(),
        "crop": crop_title or "General",
        "matched": True,
    }
