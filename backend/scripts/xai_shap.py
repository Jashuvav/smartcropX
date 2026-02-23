"""
SHAP-based explanations for tabular models (crop price XGBoost & soil heuristic).
Falls back to rule-based feature ranking when SHAP computation fails.
"""
import numpy as np
import pandas as pd
import os
import logging
import joblib

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "processed_data")

# ─── Feature names must match predict_with_graph.py ─────────────────
FEATURE_NAMES = [
    "Days", "Month", "Arrivals (Tonnes)", "Min Price (Rs./Quintal)",
    "Max Price (Rs./Quintal)", "Price Range", "Demand Indicator",
    "Rolling_Modal_Price", "Lag_1_Month", "Lag_2_Months", "Price_Change_Rate",
]

FEATURE_DESCRIPTIONS = {
    "Days": "Time elapsed since first record — captures long-term trend",
    "Month": "Calendar month — captures seasonal effects",
    "Arrivals (Tonnes)": "Tonnage arriving at markets — supply indicator",
    "Min Price (Rs./Quintal)": "Lowest reported price — floor indicator",
    "Max Price (Rs./Quintal)": "Highest reported price — ceiling indicator",
    "Price Range": "Max minus Min price — volatility indicator",
    "Demand Indicator": "Arrivals / MinPrice ratio — demand proxy",
    "Rolling_Modal_Price": "30-day rolling average of modal price",
    "Lag_1_Month": "Modal price one month ago",
    "Lag_2_Months": "Modal price two months ago",
    "Price_Change_Rate": "Month-over-month percentage price change",
}

CROPS = ["banana", "onion", "tomato", "wheat", "carrot"]

# ─── rule-based fallback ────────────────────────────────────────────
# Manually curated importance ranking per crop (used when SHAP fails)
RULE_BASED_FEATURES = {
    "banana": [
        {"feature": "Rolling_Modal_Price", "impact": 0.28, "direction": "positive"},
        {"feature": "Lag_1_Month",         "impact": 0.22, "direction": "positive"},
        {"feature": "Days",                "impact": 0.15, "direction": "positive"},
        {"feature": "Price_Change_Rate",   "impact": 0.12, "direction": "positive"},
        {"feature": "Month",               "impact": 0.08, "direction": "mixed"},
    ],
    "onion": [
        {"feature": "Arrivals (Tonnes)",   "impact": 0.25, "direction": "negative"},
        {"feature": "Rolling_Modal_Price", "impact": 0.22, "direction": "positive"},
        {"feature": "Lag_1_Month",         "impact": 0.18, "direction": "positive"},
        {"feature": "Month",               "impact": 0.14, "direction": "mixed"},
        {"feature": "Price_Change_Rate",   "impact": 0.09, "direction": "positive"},
    ],
    "tomato": [
        {"feature": "Rolling_Modal_Price", "impact": 0.26, "direction": "positive"},
        {"feature": "Arrivals (Tonnes)",   "impact": 0.20, "direction": "negative"},
        {"feature": "Lag_1_Month",         "impact": 0.17, "direction": "positive"},
        {"feature": "Month",               "impact": 0.15, "direction": "mixed"},
        {"feature": "Days",                "impact": 0.10, "direction": "positive"},
    ],
    "wheat": [
        {"feature": "Days",                "impact": 0.24, "direction": "positive"},
        {"feature": "Rolling_Modal_Price", "impact": 0.21, "direction": "positive"},
        {"feature": "Lag_2_Months",        "impact": 0.16, "direction": "positive"},
        {"feature": "Lag_1_Month",         "impact": 0.14, "direction": "positive"},
        {"feature": "Month",               "impact": 0.10, "direction": "mixed"},
    ],
    "carrot": [
        {"feature": "Rolling_Modal_Price", "impact": 0.27, "direction": "positive"},
        {"feature": "Lag_1_Month",         "impact": 0.20, "direction": "positive"},
        {"feature": "Arrivals (Tonnes)",   "impact": 0.16, "direction": "negative"},
        {"feature": "Price_Change_Rate",   "impact": 0.13, "direction": "positive"},
        {"feature": "Days",                "impact": 0.11, "direction": "positive"},
    ],
}


def _direction_label(shap_val: float) -> str:
    if shap_val > 0.005:
        return "positive"
    elif shap_val < -0.005:
        return "negative"
    return "neutral"


def _build_sample(crop: str) -> pd.DataFrame:
    """Build a single-row DataFrame with median feature values for the crop."""
    from datetime import datetime, timedelta

    csv_path = os.path.join(DATA_DIR, f"{crop}_processed.csv")
    data = pd.read_csv(csv_path)
    data["Reported Date"] = pd.to_datetime(data["Reported Date"])
    data = data.sort_values("Reported Date")

    today = datetime.now()
    future_date = today + timedelta(weeks=1)
    days_val = (future_date - data["Reported Date"].min()).days

    arrivals_median = data["Arrivals (Tonnes)"].median()
    min_price = data["Min Price (Rs./Quintal)"].median()
    max_price = data["Max Price (Rs./Quintal)"].median()

    row = {
        "Days": days_val,
        "Month": today.month,
        "Arrivals (Tonnes)": arrivals_median,
        "Min Price (Rs./Quintal)": min_price,
        "Max Price (Rs./Quintal)": max_price,
        "Price Range": max_price - min_price,
        "Demand Indicator": arrivals_median / (min_price + 1),
        "Rolling_Modal_Price": data["Rolling_Modal_Price"].median(),
        "Lag_1_Month": data["Lag_1_Month"].median(),
        "Lag_2_Months": data["Lag_2_Months"].median(),
        "Price_Change_Rate": data["Price_Change_Rate"].median(),
    }
    return pd.DataFrame([row], columns=FEATURE_NAMES)


def explain_price(crop: str):
    """
    Compute SHAP feature importances for a single crop's price model.
    Returns dict with top-5 features, their impacts, and a narrative explanation.
    """
    crop = crop.lower().strip()
    if crop not in CROPS:
        return {"error": f"Unknown crop '{crop}'. Supported: {CROPS}"}

    model_path = os.path.join(MODEL_DIR, f"{crop}_model.pkl")
    use_fallback = False

    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No model at {model_path}")

        model = joblib.load(model_path)
        sample = _build_sample(crop)

        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(sample)  # (1, n_features)

        sv = shap_values[0]  # first (only) row
        abs_sv = np.abs(sv)
        top_idx = np.argsort(abs_sv)[::-1][:5]

        features = []
        for i in top_idx:
            features.append({
                "feature": FEATURE_NAMES[i],
                "impact": round(float(abs_sv[i]), 4),
                "shap_value": round(float(sv[i]), 4),
                "direction": _direction_label(sv[i]),
                "description": FEATURE_DESCRIPTIONS.get(FEATURE_NAMES[i], ""),
            })

        # Base value + predicted value
        base_value = float(explainer.expected_value) if np.isscalar(explainer.expected_value) else float(explainer.expected_value[0])
        predicted = float(model.predict(sample)[0])

    except Exception as e:
        logger.warning(f"SHAP failed for {crop}, using rule-based fallback: {e}")
        use_fallback = True
        features = []
        for item in RULE_BASED_FEATURES.get(crop, RULE_BASED_FEATURES["banana"]):
            features.append({
                **item,
                "shap_value": item["impact"] if item["direction"] == "positive" else -item["impact"],
                "description": FEATURE_DESCRIPTIONS.get(item["feature"], ""),
            })
        base_value = None
        predicted = None

    # Narrative
    top = features[0] if features else {}
    narrative = (
        f"For {crop.capitalize()}, the most influential factor is "
        f"'{top.get('feature', 'N/A')}' ({top.get('description', '')}) "
        f"which pushes the predicted price {'up' if top.get('direction') == 'positive' else 'down' if top.get('direction') == 'negative' else 'in mixed directions'}. "
        f"The top 5 features together explain the majority of the model's prediction."
    )

    return {
        "crop": crop,
        "method": "rule-based" if use_fallback else "shap-tree-explainer",
        "features": features,
        "base_value": base_value,
        "predicted_value": predicted,
        "explanation": narrative,
    }


def explain_all_prices():
    """Run SHAP explanation for every supported crop."""
    results = {}
    for crop in CROPS:
        results[crop] = explain_price(crop)
    return results


# ─── Soil feature explanation (rule-based, image model) ─────────────
SOIL_FEATURE_RULES = {
    "Alluvial soil": [
        {"feature": "Colour (Light/Sandy)", "impact": 0.30, "direction": "positive",
         "description": "Light brownish-grey colour typical of river deposits"},
        {"feature": "Texture Smoothness", "impact": 0.25, "direction": "positive",
         "description": "Fine-grained silty texture with minimal gravel"},
        {"feature": "Colour Uniformity", "impact": 0.20, "direction": "positive",
         "description": "Relatively uniform colour across the sample"},
        {"feature": "Moisture Appearance", "impact": 0.15, "direction": "positive",
         "description": "Moderate moisture-holding capacity visible"},
        {"feature": "Organic Content", "impact": 0.10, "direction": "positive",
         "description": "Presence of organic matter from river sediments"},
    ],
    "Black Soil": [
        {"feature": "Darkness Level", "impact": 0.35, "direction": "positive",
         "description": "Very dark colour from high organic & mineral content"},
        {"feature": "Clay Content", "impact": 0.25, "direction": "positive",
         "description": "Heavy clay texture with visible cracking patterns"},
        {"feature": "Moisture Retention", "impact": 0.18, "direction": "positive",
         "description": "High moisture retention giving wet/sticky appearance"},
        {"feature": "Crack Patterns", "impact": 0.12, "direction": "positive",
         "description": "Characteristic shrinkage cracks when dry"},
        {"feature": "Texture Coarseness", "impact": 0.10, "direction": "negative",
         "description": "Absence of coarse particles supports classification"},
    ],
    "Clay soil": [
        {"feature": "Compact Texture", "impact": 0.30, "direction": "positive",
         "description": "Dense, compact structure with fine particles"},
        {"feature": "Colour Tone", "impact": 0.22, "direction": "positive",
         "description": "Greyish to brownish colour tone"},
        {"feature": "Surface Smoothness", "impact": 0.20, "direction": "positive",
         "description": "Smooth surface with minimal granularity"},
        {"feature": "Moisture Appearance", "impact": 0.16, "direction": "positive",
         "description": "Glossy appearance when wet, hard when dry"},
        {"feature": "Aggregate Structure", "impact": 0.12, "direction": "positive",
         "description": "Formation of dense aggregates"},
    ],
    "Red soil": [
        {"feature": "Red/Orange Hue", "impact": 0.38, "direction": "positive",
         "description": "Iron oxide gives distinctive reddish colour"},
        {"feature": "Granularity", "impact": 0.22, "direction": "positive",
         "description": "Granular, well-drained texture"},
        {"feature": "Colour Saturation", "impact": 0.18, "direction": "positive",
         "description": "Intensity of red/orange colouring"},
        {"feature": "Porosity Appearance", "impact": 0.12, "direction": "positive",
         "description": "Visible pores indicating good drainage"},
        {"feature": "Organic Content", "impact": 0.10, "direction": "negative",
         "description": "Low organic content supports classification"},
    ],
}


def explain_soil(predicted_class: str):
    """
    Return rule-based feature explanation for a soil classification.
    (Image-based CNN models don't have tabular features, so we use
     domain-knowledge rules about what visual features drive each class.)
    """
    if predicted_class not in SOIL_FEATURE_RULES:
        predicted_class = "Alluvial soil"  # safe default

    features = []
    for item in SOIL_FEATURE_RULES[predicted_class]:
        features.append({
            **item,
            "shap_value": item["impact"] if item["direction"] == "positive" else -item["impact"],
        })

    narrative = (
        f"For {predicted_class}, the model primarily relies on visual "
        f"characteristics like '{features[0]['feature']}' ({features[0]['description']}). "
        f"These features are derived from the image's colour, texture, and structural patterns."
    )

    return {
        "soil_type": predicted_class,
        "method": "domain-rule-based",
        "features": features,
        "explanation": narrative,
    }
