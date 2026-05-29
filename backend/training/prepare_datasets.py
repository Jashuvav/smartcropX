import json
import random
import shutil
import zipfile
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import requests
from PIL import Image, UnidentifiedImageError

BASE_DIR = Path(__file__).resolve().parents[1]
TRAINING_DIR = BASE_DIR / "training"
DISEASE_DIR = TRAINING_DIR / "disease"
SOIL_DIR = TRAINING_DIR / "soil"
MODELS_DIR = BASE_DIR / "models"

DISEASE_SPLITS = ["train", "val", "test"]
SOIL_SPLITS = ["train", "val", "test"]

CURATED_SOIL_DATASET_URL = "https://codeload.github.com/Phantom-fs/Soil-Classification-Dataset/zip/refs/heads/main"
CURATED_SOIL_DATASET_NAME = "Phantom-fs/Soil-Classification-Dataset"
CURATED_SOIL_SUBDIR = "Orignal-Dataset"

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def _clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _split_paths(items: List[Path], train_ratio: float = 0.7, val_ratio: float = 0.15) -> Dict[str, List[Path]]:
    random.shuffle(items)
    n = len(items)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    return {
        "train": items[:n_train],
        "val": items[n_train:n_train + n_val],
        "test": items[n_train + n_val:],
    }


def _copy_split_files(class_name: str, split_map: Dict[str, List[Path]], destination_root: Path) -> None:
    for split, files in split_map.items():
        target = destination_root / split / class_name
        target.mkdir(parents=True, exist_ok=True)
        for idx, src in enumerate(files):
            dst = target / f"{class_name.replace(' ', '_')}_{idx:04d}.jpg"
            with Image.open(src) as img:
                img.convert("RGB").save(dst, format="JPEG", quality=92)


def _safe_open_image(path: Path) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False


def _write_json(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def _download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, timeout=180, stream=True) as response:
        response.raise_for_status()
        with open(destination, "wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def _find_directory(root: Path, name: str) -> Path:
    for path in root.rglob(name):
        if path.is_dir():
            return path
    raise FileNotFoundError(f"Unable to locate {name} under {root}")


def _prepare_curated_soil_source(extract_root: Path) -> Path:
    archive_path = SOIL_DIR / "downloads" / "soil_classification_dataset.zip"
    if archive_path.exists():
        archive_path.unlink()
    _download_file(CURATED_SOIL_DATASET_URL, archive_path)

    _clean_dir(extract_root)
    with zipfile.ZipFile(archive_path) as archive:
        archive.extractall(extract_root)

    return _find_directory(extract_root, CURATED_SOIL_SUBDIR)


def _iter_image_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
            yield path


def _soil_class_name_from_folder(name: str) -> str:
    return name.replace("_", " ").strip()


def _hash_file(path: Path) -> str:
    digest = sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_plant_disease_dataset(max_per_class: int = 500) -> Dict[str, int]:
    from datasets import load_dataset

    dataset_root = DISEASE_DIR / "dataset"
    _clean_dir(dataset_root)

    ds = load_dataset("GVJahnavi/Plant_village_subset")
    label_names = ds["train"].features["label"].names
    class_buffers: Dict[str, List[Image.Image]] = {name: [] for name in label_names}

    for split_name in ds.keys():
        for row in ds[split_name]:
            class_name = label_names[int(row["label"])]
            if len(class_buffers[class_name]) < max_per_class:
                class_buffers[class_name].append(row["image"].convert("RGB"))

    # Keep classes with enough examples for stable training.
    selected = {k: v for k, v in class_buffers.items() if len(v) >= 80}
    if len(selected) < 5:
        raise RuntimeError("PlantVillage extraction yielded too few classes with enough samples")

    counts: Dict[str, int] = {}
    tmp_root = DISEASE_DIR / "_tmp_raw"
    _clean_dir(tmp_root)

    for class_name, images in selected.items():
        class_dir = tmp_root / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        for idx, arr in enumerate(images):
            out = class_dir / f"{class_name.replace(' ', '_')}_{idx}.jpg"
            arr.save(out, format="JPEG", quality=92)
        counts[class_name] = len(images)

    for class_dir in sorted(tmp_root.iterdir()):
        files = [p for p in class_dir.glob("*.jpg") if _safe_open_image(p)]
        split_map = _split_paths(files)
        _copy_split_files(class_dir.name, split_map, dataset_root)

    shutil.rmtree(tmp_root, ignore_errors=True)

    _write_json(DISEASE_DIR / "logs" / "dataset_summary.json", {
        "source": "huggingface::GVJahnavi/Plant_village_subset",
        "selected_classes": sorted(counts.keys()),
        "counts_per_class": counts,
        "max_per_class_cap": max_per_class,
    })
    return counts


def _dedupe_and_filter_images(class_dir: Path) -> List[Path]:
    seen_hashes = set()
    seen_signatures = set()
    kept: List[Path] = []

    for path in _iter_image_files(class_dir):
        if not _safe_open_image(path):
            path.unlink(missing_ok=True)
            continue

        file_hash = _hash_file(path)
        if file_hash in seen_hashes:
            path.unlink(missing_ok=True)
            continue

        with Image.open(path) as img:
            rgb = img.convert("RGB").resize((64, 64))
            key = tuple(np.asarray(rgb).reshape(-1)[::64].tolist())

        if key in seen_signatures:
            path.unlink(missing_ok=True)
            continue

        seen_hashes.add(file_hash)
        seen_signatures.add(key)
        kept.append(path)

    return kept


def prepare_soil_dataset(max_per_class: int = 0) -> Dict[str, int]:
    dataset_root = SOIL_DIR / "dataset"
    raw_root = SOIL_DIR / "_source_curated"

    _clean_dir(dataset_root)
    source_root = _prepare_curated_soil_source(raw_root)

    counts: Dict[str, int] = {}
    for class_dir in sorted(source_root.iterdir()):
        if not class_dir.is_dir():
            continue
        images = _dedupe_and_filter_images(class_dir)
        if max_per_class > 0:
            images = images[:max_per_class]
        if len(images) < 20:
            raise RuntimeError(f"Not enough clean images for class {class_dir.name}: {len(images)}")

        split_map = _split_paths(images)
        class_name = _soil_class_name_from_folder(class_dir.name)
        _copy_split_files(class_name, split_map, dataset_root)
        counts[class_name] = len(images)

    shutil.rmtree(raw_root, ignore_errors=True)

    _write_json(SOIL_DIR / "logs" / "dataset_summary.json", {
        "source": f"github::{CURATED_SOIL_DATASET_NAME}/{CURATED_SOIL_SUBDIR}",
        "download_url": CURATED_SOIL_DATASET_URL,
        "counts_per_class": counts,
        "max_per_class_cap": max_per_class,
    })

    # Persist class mappings for runtime.
    soil_labels = sorted(counts.keys())
    _write_json(MODELS_DIR / "class_names.json", {"classes": soil_labels})
    return counts


def main() -> None:
    (DISEASE_DIR / "logs").mkdir(parents=True, exist_ok=True)
    (SOIL_DIR / "logs").mkdir(parents=True, exist_ok=True)

    disease_counts = prepare_plant_disease_dataset()
    soil_counts = prepare_soil_dataset()

    print("Prepared disease dataset classes:", len(disease_counts))
    print("Prepared soil dataset classes:", len(soil_counts))


if __name__ == "__main__":
    main()
