import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import joblib
import pandas as pd
import numpy as np
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "processed_data")
GRAPH_DIR = os.path.join(os.path.dirname(__file__), "predicted_graphs")
os.makedirs(GRAPH_DIR, exist_ok=True)

models = {
    "banana": os.path.join(MODEL_DIR, "banana_model.pkl"),
    "onion": os.path.join(MODEL_DIR, "onion_model.pkl"),
    "tomato": os.path.join(MODEL_DIR, "tomato_model.pkl"),
    "wheat": os.path.join(MODEL_DIR, "wheat_model.pkl"),
    "carrot": os.path.join(MODEL_DIR, "carrot_model.pkl")
}

FEATURE_NAMES = [
    "Days", "Month", "Arrivals (Tonnes)", "Min Price (Rs./Quintal)", "Max Price (Rs./Quintal)",
    "Price Range", "Demand Indicator", "Rolling_Modal_Price", "Lag_1_Month", "Lag_2_Months", "Price_Change_Rate"
]

# Metadata for each crop (category, recommendation, trend computed dynamically)
CROP_META = {
    "banana": {"category": "fruit", "recommendation": "Prices expected to rise in coming weeks. Consider delaying harvest if possible to maximize profits. Good time for banana farmers to secure forward contracts."},
    "onion": {"category": "vegetable", "recommendation": "Steady price increase trend suggests holding inventory if storage conditions permit. Moderate upward trajectory indicates stable demand."},
    "tomato": {"category": "vegetable", "recommendation": "Focus on quality over quantity to secure premium pricing. Consider local direct-to-consumer sales for better margins."},
    "wheat": {"category": "grain", "recommendation": "Consider futures contracts to lock in higher prices. Good opportunity for wheat farmers to plan expanded planting for next season."},
    "carrot": {"category": "vegetable", "recommendation": "Strong upward trend indicates high demand. Consider staggered harvesting to benefit from peak prices."},
}

def get_price_predictions():
    all_results = []
    today = datetime.now()
    weeks_ahead = 5

    for crop in models:
        try:
            model = joblib.load(models[crop])
            data = pd.read_csv(os.path.join(DATA_DIR, f"{crop}_processed.csv"))
            data["Reported Date"] = pd.to_datetime(data["Reported Date"])
            data = data.sort_values(by="Reported Date")

            future_dates = [today + timedelta(weeks=i) for i in range(1, weeks_ahead + 1)]
            future_days = np.array([(d - data["Reported Date"].min()).days for d in future_dates])

            arrivals_median = data["Arrivals (Tonnes)"].median()
            min_price_median = data["Min Price (Rs./Quintal)"].median()
            max_price_median = data["Max Price (Rs./Quintal)"].median()
            price_range_median = max_price_median - min_price_median
            demand_indicator_median = arrivals_median / (min_price_median + 1)
            rolling_price_median = data["Rolling_Modal_Price"].median()
            lag_1_month_median = data["Lag_1_Month"].median()
            lag_2_months_median = data["Lag_2_Months"].median()
            price_change_rate_median = data["Price_Change_Rate"].median()

            demand_variation = np.linspace(0.95, 1.05, weeks_ahead)
            price_change_variation = np.linspace(-0.02, 0.02, weeks_ahead)

            input_data = pd.DataFrame({
                "Days": future_days,
                "Month": [d.month for d in future_dates],
                "Arrivals (Tonnes)": arrivals_median * demand_variation,
                "Min Price (Rs./Quintal)": min_price_median * demand_variation,
                "Max Price (Rs./Quintal)": max_price_median * demand_variation,
                "Price Range": price_range_median * demand_variation,
                "Demand Indicator": demand_indicator_median * demand_variation,
                "Rolling_Modal_Price": rolling_price_median * demand_variation,
                "Lag_1_Month": lag_1_month_median * demand_variation,
                "Lag_2_Months": lag_2_months_median * demand_variation,
                "Price_Change_Rate": price_change_rate_median + price_change_variation
            }, columns=FEATURE_NAMES)

            predicted_prices = model.predict(input_data)

            if crop == "banana":
                unit = "Rs./Dozen"
                prices = (predicted_prices / 100) * 1.5
            else:
                unit = "Rs./Kg"
                prices = predicted_prices / 100

            prediction_list = [
                {"date": future_dates[i].strftime("%Y-%m-%d"), "price": round(float(prices[i]), 2)}
                for i in range(weeks_ahead)
            ]


            plt.figure(figsize=(10, 5))
            plt.plot(future_dates, predicted_prices, linestyle="dotted", color="red", marker="x", label="Predicted Prices")
            plt.xlabel("Date")
            plt.ylabel("Modal Price (Rs./Quintal)")
            plt.title(f"Prediction for {crop.capitalize()}")
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{crop}_prediction_{timestamp}.png"
            filepath = os.path.join(GRAPH_DIR, filename)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()

            print(f"✅ Saved plot for {crop} at {filepath}")

            # Compute trend
            first_price = prices[0]
            last_price = prices[-1]
            pct = ((last_price - first_price) / first_price) * 100 if first_price else 0
            trend = "up" if pct > 1 else ("down" if pct < -1 else "stable")

            meta = CROP_META.get(crop, {"category": "other", "recommendation": "Monitor price trends and plan accordingly."})

            all_results.append({
                "crop": crop,
                "unit": unit,
                "predictions": prediction_list,
                "graph_url": f"/graphs/{filename}",
                "trend": trend,
                "category": meta["category"],
                "recommendation": meta["recommendation"]
            })

        except Exception as e:
            all_results.append({
                "crop": crop,
                "error": str(e)
            })

    return all_results
