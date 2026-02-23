"""
SmartCropX XAI Chatbot — rule-based agricultural knowledge assistant.
Provides farming advice, explains AI model predictions, and answers
crop-related questions without requiring any external API key.
"""

import re
import random
from datetime import datetime

# ── Knowledge base ───────────────────────────────────────────────────

CROP_INFO = {
    "tomato": {
        "season": "Kharif / Rabi (year-round in tropical regions)",
        "soil": "Well-drained loamy soil, pH 6.0–7.0",
        "water": "Regular watering; avoid waterlogging",
        "diseases": ["Early Blight", "Late Blight", "Leaf Curl Virus", "Septoria Leaf Spot", "Bacterial Spot"],
        "tips": [
            "Use disease-resistant varieties like Arka Rakshak.",
            "Apply neem-based pesticide for whitefly control.",
            "Mulching helps conserve moisture and suppress weeds.",
            "Prune lower leaves to improve air circulation.",
            "Rotate crops every season to prevent soil-borne diseases.",
        ],
        "price_factors": ["seasonal supply glut", "transportation cost", "cold storage availability", "monsoon impact", "demand spikes during festivals"],
    },
    "onion": {
        "season": "Rabi (October–March) and Kharif (June–September)",
        "soil": "Fertile, well-drained loamy soil, pH 6.0–7.5",
        "water": "Moderate; stop watering 2 weeks before harvest",
        "diseases": ["Purple Blotch", "Downy Mildew", "Basal Rot", "Thrips damage"],
        "tips": [
            "Treat seeds with fungicide before sowing.",
            "Apply sulphur-based fertiliser for pungency & yield.",
            "Avoid over-irrigation — it causes neck rot in storage.",
            "Harvest when 50% of tops fall over for best storage life.",
        ],
        "price_factors": ["monsoon rains affecting yield", "government export bans", "cold storage capacity", "local vs wholesale demand"],
    },
    "wheat": {
        "season": "Rabi (November–April)",
        "soil": "Loamy to clay-loam soil, pH 6.0–7.5",
        "water": "5–6 irrigations at critical growth stages",
        "diseases": ["Rust (Brown/Yellow/Black)", "Powdery Mildew", "Karnal Bunt", "Loose Smut"],
        "tips": [
            "Sow HD-3226 or DBW-187 for high yield in North India.",
            "First irrigation at Crown Root Initiation stage (21 days) is crucial.",
            "Use zero-tillage sowing to save water and fuel.",
            "Apply zinc sulphate at sowing for better grain quality.",
        ],
        "price_factors": ["MSP announcements", "global wheat prices", "export demand", "government buffer stock levels"],
    },
    "banana": {
        "season": "Year-round planting possible; matures in 11–14 months",
        "soil": "Deep, well-drained loamy soil rich in organic matter, pH 6.5–7.5",
        "water": "High water demand — drip irrigation recommended",
        "diseases": ["Panama Wilt (Fusarium)", "Sigatoka Leaf Spot", "Bunchy Top Virus", "Anthracnose"],
        "tips": [
            "Use tissue-culture plants for disease-free stock.",
            "De-sucker regularly to maintain only 1 follower.",
            "Apply potassium-rich fertiliser for bunch weight.",
            "Support plants with props after flowering to prevent toppling.",
        ],
        "price_factors": ["cluster-wise supply", "ripening chamber costs", "distance to urban market", "festival demand"],
    },
    "carrot": {
        "season": "Rabi (October–February)",
        "soil": "Deep sandy-loam soil free of stones, pH 6.0–6.8",
        "water": "Even, consistent moisture; avoid fluctuations",
        "diseases": ["Alternaria Leaf Blight", "Cavity Spot", "Carrot Rust Fly"],
        "tips": [
            "Thin seedlings to 5 cm spacing for uniform roots.",
            "Raised beds improve drainage and root shape.",
            "Cover shoulders with soil to prevent green tops.",
            "Harvest at 80–90 days for baby carrots, 100–120 for full size.",
        ],
        "price_factors": ["summer scarcity premium", "organic vs conventional pricing", "nearby processing unit demand"],
    },
}

SOIL_TYPES = {
    "alluvial": {
        "description": "Deposited by rivers; very fertile and widely found in Indo-Gangetic plains.",
        "crops": ["Rice", "Wheat", "Sugarcane", "Maize", "Pulses"],
        "care": "Maintain with organic compost; test for micronutrient deficiency.",
    },
    "black": {
        "description": "Rich in clay and retains moisture well. Found in Deccan Plateau.",
        "crops": ["Cotton", "Soybean", "Wheat", "Jowar", "Sunflower"],
        "care": "Avoid waterlogging; add gypsum to improve structure.",
    },
    "red": {
        "description": "Iron-rich, well-drained, acidic soil found in southern & eastern India.",
        "crops": ["Groundnut", "Potato", "Millets", "Pulses", "Tobacco"],
        "care": "Add lime to correct acidity; enrich with organic matter.",
    },
    "laterite": {
        "description": "Leached soil, low in nutrients. Found in high-rainfall tropical areas.",
        "crops": ["Tea", "Coffee", "Cashew", "Rubber", "Coconut"],
        "care": "Heavy manuring required; use cover crops to prevent erosion.",
    },
    "sandy": {
        "description": "Coarse-textured, low water-holding capacity. Common in arid zones.",
        "crops": ["Millets", "Barley", "Pulses", "Watermelon"],
        "care": "Add organic matter to increase water retention; use drip irrigation.",
    },
    "clay": {
        "description": "Fine-grained, high water retention but poor drainage.",
        "crops": ["Rice", "Wheat", "Cotton"],
        "care": "Add sand/organic matter to improve drainage; avoid compaction.",
    },
}

DISEASE_EXPLANATIONS = {
    "early blight": "Caused by *Alternaria solani*. Brown concentric-ring spots on older leaves. Grad-CAM highlights the lesion rings. **Manage**: remove affected leaves, apply mancozeb fungicide, ensure good air circulation.",
    "late blight": "Caused by *Phytophthora infestans*. Water-soaked dark patches spreading rapidly. **Manage**: copper-based sprays, avoid overhead irrigation, use resistant varieties.",
    "leaf curl": "Viral disease spread by whiteflies. Leaves curl upward and thicken. **Manage**: control whiteflies with yellow sticky traps, neem oil; use virus-resistant varieties.",
    "septoria": "Caused by *Septoria lycopersici*. Small circular spots with grey centres. **Manage**: remove lower leaves, apply chlorothalonil, mulch to reduce splash.",
    "powdery mildew": "White powdery coating on leaves caused by *Erysiphe* spp. **Manage**: sulphur dust, baking soda spray, improve air circulation.",
    "rust": "Orange-brown pustules on leaves (wheat, beans). **Manage**: use resistant varieties, apply propiconazole fungicide.",
    "bacterial spot": "Water-soaked angular spots turning brown/black. **Manage**: copper bactericides, avoid working in wet fields, sanitise tools.",
    "healthy": "No disease detected — the leaf appears healthy. The Grad-CAM shows uniform, low activation across the leaf meaning the model found no distinctive disease features.",
    "panama wilt": "Fusarium oxysporum infects banana through roots. Leaves yellow from edges. **Manage**: use tissue-culture plants, soil solarisation, avoid flood irrigation.",
    "sigatoka": "Fungal leaf spot on banana — yellow streaks turning brown. **Manage**: de-leaf affected parts, apply propiconazole, maintain field hygiene.",
}

XAI_EXPLANATIONS = {
    "gradcam": "**Grad-CAM** (Gradient-weighted Class Activation Mapping) creates a heatmap showing which regions of the image influenced the model's decision most. Red/warm areas = high importance, blue/cool = low importance. It helps you see *where* the model is looking — for instance, it should highlight the diseased part of a leaf, not the background.",
    "shap": "**SHAP** (SHapley Additive exPlanations) shows how much each input feature pushed the prediction higher or lower compared to the average. Positive SHAP value = feature pushes prediction up; negative = pushes it down. For price prediction, it tells you which factors (season, past price, weather) were most influential.",
    "xai": "Explainable AI (XAI) makes AI predictions transparent. SmartCropX uses two techniques:\n\n🔬 **Grad-CAM** for image models (disease & soil detection) — highlights important image regions.\n📊 **SHAP** for tabular models (price prediction) — shows feature importances.\n\nThis helps farmers trust and understand the AI's recommendations.",
}

GENERAL_TIPS = [
    "Test your soil every season — even small pH changes affect yield significantly.",
    "Crop rotation breaks pest and disease cycles; never grow the same family back-to-back.",
    "Neem cake is an excellent organic fertiliser and natural pest deterrent.",
    "Drip irrigation can save 30–50% water compared to flood irrigation.",
    "Intercropping with legumes adds nitrogen to the soil naturally.",
    "Mulching with crop residue reduces water evaporation by up to 25%.",
    "Always scout your field once a week for early signs of pest or disease.",
    "Vermicompost has 5× more nitrogen than regular compost — worth the effort.",
    "Harvest crops in the early morning for the longest shelf life.",
    "Keeping farm records helps you track what works — even a simple diary counts.",
]

GREETINGS_IN = ["hello", "hi", "hey", "good morning", "good evening", "namaste", "howdy"]
GREETINGS_OUT = [
    "Hello! 🌱 I'm your SmartCropX AI assistant. Ask me about crops, diseases, soil, prices, or how our AI explanations work!",
    "Hey there! 🧑‍🌾 I can help with crop advice, disease identification, soil info, and explain how our AI models make decisions.",
    "Hi! 👋 Welcome to SmartCropX. Ask me anything about farming, or type 'help' to see what I can do!",
]


# ── Helpers ──────────────────────────────────────────────────────────

def _find_crop(text: str):
    for crop in CROP_INFO:
        if crop in text:
            return crop
    return None


def _find_soil(text: str):
    for soil in SOIL_TYPES:
        if soil in text:
            return soil
    return None


def _find_disease(text: str):
    for disease in DISEASE_EXPLANATIONS:
        if disease in text:
            return disease
    return None


# ── Main response logic ─────────────────────────────────────────────

def get_chat_response(message: str) -> dict:
    """Return a chatbot response dict with 'reply' and optional 'suggestions'."""
    text = message.lower().strip()

    # Greeting
    if any(g in text for g in GREETINGS_IN):
        return {
            "reply": random.choice(GREETINGS_OUT),
            "suggestions": ["What crops do you support?", "Explain Grad-CAM", "Soil tips", "Farming advice"],
        }

    # Help
    if text in ("help", "what can you do", "menu", "options"):
        return {
            "reply": (
                "I can help with:\n\n"
                "🌿 **Crop info** — ask about tomato, onion, wheat, banana, or carrot\n"
                "🦠 **Disease help** — ask about early blight, rust, leaf curl, etc.\n"
                "🌱 **Soil types** — ask about alluvial, black, red, laterite, sandy, clay\n"
                "📈 **Price factors** — ask 'what affects tomato price?'\n"
                "🔍 **XAI explained** — ask 'what is Grad-CAM?' or 'what is SHAP?'\n"
                "💡 **Farming tips** — say 'give me a tip'\n\n"
                "Just type naturally — I'll do my best to understand!"
            ),
            "suggestions": ["Tomato diseases", "What is SHAP?", "Onion price factors", "Soil types"],
        }

    # XAI explanations
    if any(k in text for k in ["grad-cam", "gradcam", "grad cam", "heatmap"]):
        return {"reply": XAI_EXPLANATIONS["gradcam"], "suggestions": ["What is SHAP?", "What is XAI?"]}
    if "shap" in text:
        return {"reply": XAI_EXPLANATIONS["shap"], "suggestions": ["What is Grad-CAM?", "What is XAI?"]}
    if any(k in text for k in ["xai", "explainable ai", "explainability", "explain ai", "how does ai work"]):
        return {"reply": XAI_EXPLANATIONS["xai"], "suggestions": ["What is Grad-CAM?", "What is SHAP?"]}

    # Disease questions
    disease = _find_disease(text)
    if disease:
        return {
            "reply": f"**{disease.title()}**\n\n{DISEASE_EXPLANATIONS[disease]}",
            "suggestions": ["Another disease", "What is Grad-CAM?", "Crop tips"],
        }
    if any(k in text for k in ["disease", "sick", "infection", "blight", "wilt", "fungus", "virus"]):
        crop = _find_crop(text)
        if crop:
            diseases = ", ".join(CROP_INFO[crop]["diseases"])
            return {
                "reply": f"Common **{crop.title()}** diseases:\n\n{diseases}\n\nAsk about any specific one for details, or upload an image on our Disease Detection page for AI analysis with Grad-CAM explanation!",
                "suggestions": [f"What is {CROP_INFO[crop]['diseases'][0]}?", "Explain Grad-CAM"],
            }
        return {
            "reply": "Which crop are you asking about? I have disease info for **tomato, onion, wheat, banana, and carrot**.",
            "suggestions": ["Tomato diseases", "Wheat diseases", "Banana diseases"],
        }

    # Price related
    if any(k in text for k in ["price", "cost", "market", "rate", "msp"]):
        crop = _find_crop(text)
        if crop:
            factors = "\n".join(f"• {f}" for f in CROP_INFO[crop]["price_factors"])
            return {
                "reply": f"**Factors affecting {crop.title()} prices:**\n\n{factors}\n\n📊 Our AI uses SHAP to show which features most influenced its price prediction. Try the Market Prediction page!",
                "suggestions": ["What is SHAP?", f"{crop.title()} growing tips"],
            }
        return {
            "reply": "I can explain price factors for **tomato, onion, wheat, banana, and carrot**. Which crop?",
            "suggestions": ["Tomato price", "Onion price", "Wheat price"],
        }

    # Soil questions
    soil = _find_soil(text)
    if soil:
        info = SOIL_TYPES[soil]
        crops_str = ", ".join(info["crops"])
        return {
            "reply": f"**{soil.title()} Soil**\n\n{info['description']}\n\n🌾 **Best crops:** {crops_str}\n🧪 **Care:** {info['care']}",
            "suggestions": ["Other soil types", "What is Grad-CAM?"],
        }
    if any(k in text for k in ["soil", "dirt", "land type", "earth"]):
        types = ", ".join(s.title() for s in SOIL_TYPES)
        return {
            "reply": f"I know about these soil types: **{types}**.\n\nAsk about any one, or upload a soil image on the Soil Detection page for AI classification with Grad-CAM heatmap!",
            "suggestions": ["Alluvial soil", "Black soil", "Red soil"],
        }

    # Crop info
    crop = _find_crop(text)
    if crop:
        info = CROP_INFO[crop]
        tip = random.choice(info["tips"])
        diseases = ", ".join(info["diseases"][:3])
        return {
            "reply": (
                f"**{crop.title()}**\n\n"
                f"📅 **Season:** {info['season']}\n"
                f"🌱 **Soil:** {info['soil']}\n"
                f"💧 **Water:** {info['water']}\n"
                f"🦠 **Common diseases:** {diseases}\n\n"
                f"💡 **Tip:** {tip}"
            ),
            "suggestions": [f"{crop.title()} diseases", f"{crop.title()} price factors", "Give me a tip"],
        }

    # Weather
    if any(k in text for k in ["weather", "rain", "temperature", "forecast", "climate"]):
        return {
            "reply": "🌦️ Check our **Weather Forecasting** page for ML-based predictions and extreme weather alerts for your region!\n\nOur model analyses historical weather patterns to forecast temperature, humidity, and rainfall.",
            "suggestions": ["How does AI predict weather?", "Crop tips"],
        }

    # General farming tips
    if any(k in text for k in ["tip", "advice", "suggest", "recommend", "help me farm", "farming"]):
        return {
            "reply": f"💡 **Farming Tip:**\n\n{random.choice(GENERAL_TIPS)}",
            "suggestions": ["Another tip", "Crop info", "Soil types"],
        }

    # Thank you
    if any(k in text for k in ["thank", "thanks", "great", "awesome", "helpful"]):
        return {
            "reply": "You're welcome! 😊 Happy farming! Ask me anything else anytime.",
            "suggestions": ["Crop info", "Farming tip", "What is XAI?"],
        }

    # Bye
    if any(k in text for k in ["bye", "goodbye", "see you", "exit", "quit"]):
        return {
            "reply": "Goodbye! 🌾 Wishing you a great harvest. Come back anytime!",
            "suggestions": [],
        }

    # SmartCropX meta
    if any(k in text for k in ["smartcropx", "smart crop", "about", "what is this", "who are you"]):
        return {
            "reply": (
                "I'm the **SmartCropX AI Assistant** 🤖\n\n"
                "SmartCropX is a full-stack smart agriculture platform featuring:\n\n"
                "🌿 AI Disease Detection (with Grad-CAM explanations)\n"
                "📈 Crop Price Prediction (with SHAP feature importance)\n"
                "🌦️ Weather Forecasting & Alerts\n"
                "🌱 Soil Classification (with Grad-CAM heatmaps)\n"
                "🔗 Blockchain Marketplace\n"
                "👥 Community Forum\n\n"
                "All AI predictions come with **Explainable AI** so you can understand *why* the model made its decision."
            ),
            "suggestions": ["What is Grad-CAM?", "What is SHAP?", "Crop info"],
        }

    # Fallback
    return {
        "reply": (
            "I'm not sure I understood that. 🤔 Try asking about:\n\n"
            "• A **crop** (tomato, wheat, onion, banana, carrot)\n"
            "• A **disease** (early blight, rust, leaf curl…)\n"
            "• A **soil type** (alluvial, black, red…)\n"
            "• **XAI** (Grad-CAM, SHAP)\n"
            "• Or just say **'help'** for a full menu!"
        ),
        "suggestions": ["Help", "Tomato info", "What is XAI?", "Farming tip"],
    }
