import json
from pathlib import Path

from prepare_datasets import main as prepare_main
from train_disease_model import train as train_disease
from train_soil_model import train as train_soil

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = BASE_DIR / "training" / "logs" / "training_summary.json"


def main() -> None:
    (BASE_DIR / "training" / "logs").mkdir(parents=True, exist_ok=True)
    prepare_main()

    disease_metrics = train_disease()
    soil_metrics = train_soil()

    summary = {
        "disease": disease_metrics,
        "soil": soil_metrics,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
