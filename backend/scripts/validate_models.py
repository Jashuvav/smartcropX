from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable, Dict, List

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from services.image_models import (  # noqa: E402
    LOW_CONF_DISEASE_THRESHOLD,
    LOW_CONF_SOIL_THRESHOLD,
    ensure_models_trained,
    predict_plant_image,
    predict_soil_image,
)

TEST_SAMPLES_DIR = ROOT_DIR / "test_samples"
SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def _sample_images(folder: Path) -> List[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Missing sample folder: {folder}")

    images = sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES)
    if not images:
        raise FileNotFoundError(f"No sample images found in {folder}")
    return images


def _run_suite(
    suite_name: str,
    folder: Path,
    predict_fn: Callable[[str], Dict[str, object]],
    label_key: str,
    threshold: float,
) -> Dict[str, object]:
    images = _sample_images(folder)
    processed = 0

    print(f"\n[{suite_name}] samples={len(images)}")
    for image_path in images:
        result = predict_fn(str(image_path))
        confidence = float(result.get("confidence", 0.0))
        predicted_label = str(result.get(label_key, "Unknown"))
        is_uncertain = predicted_label == "Uncertain" or confidence < threshold
        print(
            f"- {image_path.name}: predicted={predicted_label} confidence={confidence:.4f} uncertain={str(is_uncertain).lower()}"
        )
        processed += 1

    return {
        "status": "ok",
        "processed": processed,
    }


def main() -> int:
    try:
        ensure_models_trained()
        disease_result = _run_suite(
            "disease",
            TEST_SAMPLES_DIR / "disease",
            predict_plant_image,
            "disease",
            LOW_CONF_DISEASE_THRESHOLD,
        )
        soil_result = _run_suite(
            "soil",
            TEST_SAMPLES_DIR / "soil",
            predict_soil_image,
            "soil_type",
            LOW_CONF_SOIL_THRESHOLD,
        )
    except Exception as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    total_processed = int(disease_result["processed"]) + int(soil_result["processed"])
    print("\nSummary")
    print(f"- disease model status: {disease_result['status']}")
    print(f"- soil model status: {soil_result['status']}")
    print(f"- total test images processed: {total_processed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
