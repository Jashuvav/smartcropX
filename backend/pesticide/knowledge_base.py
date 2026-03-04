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
        },
        "Potato": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": (
                "Apply preventively when conditions favour blight (warm, humid). "
                "Repeat at 7–14 day intervals. Do not mix with alkaline pesticides."
            ),
        },
        "_default": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Apply as foliar spray every 7–10 days at first symptom appearance.",
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
        },
        "Potato": {
            "pesticide": "Cymoxanil + Mancozeb",
            "dosage": "3.0 g/L of water",
            "instructions": (
                "Begin applications before disease onset during rainy periods. "
                "Repeat at 5–7 day intervals under high disease pressure."
            ),
        },
        "_default": {
            "pesticide": "Metalaxyl + Mancozeb",
            "dosage": "2.5 g/L of water",
            "instructions": "Spray preventively in cool-wet conditions. Repeat every 7 days.",
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
        },
        "Cotton": {
            "pesticide": "Thiamethoxam 25% WG",
            "dosage": "0.2 g/L of water",
            "instructions": (
                "Target whitefly population early in the season. "
                "Rotate with different chemistry to manage resistance."
            ),
        },
        "_default": {
            "pesticide": "Imidacloprid 17.8% SL",
            "dosage": "0.3 mL/L of water",
            "instructions": "Control insect vector (whiteflies) to manage viral leaf curl.",
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
        },
        "Potato": {
            "pesticide": "Copper Oxychloride 50% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Drench soil after removing infected tubers. Rotate with non-solanaceous crops.",
        },
        "_default": {
            "pesticide": "Streptocycline",
            "dosage": "0.5 g/10 L of water",
            "instructions": "Soil drench around roots. Remove infected plants.",
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
        },
        "Cotton": {
            "pesticide": "Trichoderma viride (bio-agent)",
            "dosage": "10 g/kg seed (seed treatment) or 2.5 kg/ha (soil application)",
            "instructions": "Mix with FYM and apply at sowing. Complements chemical control.",
        },
        "_default": {
            "pesticide": "Carbendazim 50% WP",
            "dosage": "1.0 g/L of water",
            "instructions": "Soil drench at planting. Use resistant cultivars.",
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
        },
        "Tomato": {
            "pesticide": "Sulphur 80% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Dust or spray at early symptom stage. Avoid application above 35 °C.",
        },
        "_default": {
            "pesticide": "Sulphur 80% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Apply as dust or spray at first symptom. Avoid hot conditions.",
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
        },
        "_default": {
            "pesticide": "Propiconazole 25% EC",
            "dosage": "1.0 mL/L of water",
            "instructions": "Spray at first pustule appearance. Repeat after 15 days if needed.",
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
        },
        "_default": {
            "pesticide": "Mancozeb 75% WP",
            "dosage": "2.5 g/L of water",
            "instructions": "Foliar spray when lesions appear. Ensure balanced nutrition.",
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
        },
        "_default": {
            "pesticide": "Tricyclazole 75% WP",
            "dosage": "0.6 g/L of water",
            "instructions": "Spray at panicle initiation. Limit excess nitrogen.",
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
        },
        "_default": {
            "pesticide": "Hexaconazole 5% EC",
            "dosage": "2.0 mL/L of water",
            "instructions": "Spray on sheaths at symptom onset. Drain excess standing water.",
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
        },
        "_default": {
            "pesticide": "Copper Hydroxide 77% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Spray at first symptom. Reduce nitrogen and improve drainage.",
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
        },
        "_default": {
            "pesticide": "Copper Oxychloride 50% WP",
            "dosage": "3.0 g/L of water",
            "instructions": "Spray during boll formation in humid conditions.",
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
        },
        "_default": {
            "pesticide": "Emamectin Benzoate 5% SG",
            "dosage": "0.4 g/L of water",
            "instructions": "Spray when larval population exceeds economic threshold.",
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
        },
        "Cotton": {
            "pesticide": "Imidacloprid 17.8% SL",
            "dosage": "0.3 mL/L of water",
            "instructions": "Spray on undersides of leaves where colonies concentrate.",
        },
        "Potato": {
            "pesticide": "Thiamethoxam 25% WG",
            "dosage": "0.2 g/L of water",
            "instructions": "Systemic action — spray as soon as aphid colonies are noticed.",
        },
        "_default": {
            "pesticide": "Dimethoate 30% EC",
            "dosage": "1.5 mL/L of water",
            "instructions": "Spray on affected foliage. Target undersides of leaves.",
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
        },
        "_default": {
            "pesticide": "Carbendazim 50% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Seed/tuber treatment before planting.",
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
        },
        "_default": {
            "pesticide": "Sulphur Dust",
            "dosage": "25 kg/ha",
            "instructions": "Lower soil pH with sulphur before planting. Keep moisture uniform.",
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
        },
        "_default": {
            "pesticide": "Chlorothalonil 75% WP",
            "dosage": "2.0 g/L of water",
            "instructions": "Spray at symptom onset. Remove infected plant debris.",
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
        },
        "_default": {
            "pesticide": "Mancozeb + Carbendazim combination",
            "dosage": "2.0 g + 1.0 g per litre",
            "instructions": "Spray on fruits at colour-break stage. Avoid wetting fruits.",
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
        },
        "Potato": {
            "pesticide": "Imidacloprid 17.8% SL (vector control)",
            "dosage": "0.3 mL/L of water",
            "instructions": "Control aphid vectors. Use virus-free seed tubers.",
        },
        "_default": {
            "pesticide": "Imidacloprid 17.8% SL (vector control)",
            "dosage": "0.3 mL/L of water",
            "instructions": "No direct cure. Control insect vectors and remove infected plants.",
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
        "disease": disease_lower.title(),
        "crop": crop_title or "General",
        "matched": True,
    }
