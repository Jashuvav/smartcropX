"""TensorFlow image inference services for plant disease and soil prediction."""

from __future__ import annotations

import base64
import io
import json
import logging
import os
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

PLANT_MODEL_PATH = os.path.join(MODELS_DIR, "best_plantdoc_model.keras")
PLANT_LABELS_PATH = os.path.join(MODELS_DIR, "plantdoc_class_names.json")
SOIL_MODEL_PATH = os.path.join(MODELS_DIR, "soil_classifier.keras")
SOIL_LABELS_PATH = os.path.join(MODELS_DIR, "class_names.json")

LOW_CONF_DISEASE_THRESHOLD = 0.55
LOW_CONF_SOIL_THRESHOLD = 0.55

SOIL_CROP_MAP = {
    "Alluvial Soil": ["Rice", "Wheat", "Corn", "Sugarcane", "Cotton"],
    "Black Soil": ["Cotton", "Wheat", "Jowar", "Linseed", "Tobacco"],
    "Laterite Soil": ["Cashew", "Tea", "Coffee", "Rubber", "Coconut"],
    "Red Soil": ["Millet", "Groundnut", "Potato", "Tobacco", "Pulses"],
    "Yellow Soil": ["Groundnut", "Millet", "Pulses", "Maize", "Sesame"],
    "Arid Soil": ["Bajra", "Guar", "Date Palm", "Moth Bean", "Sesame"],
    "Mountain Soil": ["Tea", "Coffee", "Spices", "Apple", "Barley"],
}

SOIL_LABEL_NORMALIZATION = {
    "alluvial": "Alluvial Soil",
    "alluvial soil": "Alluvial Soil",
    "alluvial_soil": "Alluvial Soil",
    "black": "Black Soil",
    "black soil": "Black Soil",
    "black_soil": "Black Soil",
    "laterite": "Laterite Soil",
    "laterite soil": "Laterite Soil",
    "laterite_soil": "Laterite Soil",
    "red": "Red Soil",
    "red soil": "Red Soil",
    "red_soil": "Red Soil",
    "yellow": "Yellow Soil",
    "yellow soil": "Yellow Soil",
    "yellow_soil": "Yellow Soil",
    "arid": "Arid Soil",
    "arid soil": "Arid Soil",
    "arid_soil": "Arid Soil",
    "mountain": "Mountain Soil",
    "mountain soil": "Mountain Soil",
    "mountain_soil": "Mountain Soil",
    "clay": "Clay soil",
    "clay soil": "Clay soil",
    "clay_soil": "Clay soil",
}


@dataclass
class LoadedModel:
    model: tf.keras.Model
    labels: List[str]


@dataclass
class PredictionTiming:
    preprocess_ms: float
    inference_ms: float
    total_ms: float


def _read_labels(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict) and "classes" in data:
        return list(data["classes"])
    if isinstance(data, list):
        return list(data)
    raise ValueError(f"Unsupported label file format at {path}")


def ensure_models_trained(force_retrain: bool = False) -> None:
    del force_retrain
    required = [PLANT_MODEL_PATH, PLANT_LABELS_PATH, SOIL_MODEL_PATH, SOIL_LABELS_PATH]
    missing = [p for p in required if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(f"Missing TensorFlow model artifacts: {missing}")


@lru_cache(maxsize=2)
def _load_model_pair(model_path: str, labels_path: str) -> LoadedModel:
    print(f"Loading model: {model_path}")
    logger.info("Loading model from path=%s", model_path)
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as ex:
        print(f"Model load failed for {model_path}: {ex}")
        logger.exception("Model load failed path=%s", model_path)
        raise
    labels = _read_labels(labels_path)
    output_shape = model.output_shape
    if isinstance(output_shape, list):
        output_shape = output_shape[0]
    output_dim = int(output_shape[-1]) if output_shape and output_shape[-1] is not None else None
    if output_dim is None:
        raise ValueError(f"Unable to infer output dimension for model at {model_path}")
    if output_dim != len(labels):
        raise ValueError(
            f"Label/model mismatch for {model_path}: output_dim={output_dim}, labels={len(labels)}, labels_file={labels_path}"
        )
    logger.info(
        "Loaded model=%s labels_file=%s labels=%s output_dim=%d",
        os.path.basename(model_path),
        os.path.basename(labels_path),
        labels,
        output_dim,
    )
    return LoadedModel(model=model, labels=labels)


def _canonical_soil_label(label: str) -> str:
    key = label.strip().lower().replace("-", " ").replace("_", " ")
    key = " ".join(key.split())
    return SOIL_LABEL_NORMALIZATION.get(key, label)


def _read_and_resize_rgb(image_path: str, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Unable to read image")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img.astype(np.float32)


def _read_and_resize_rgb_bytes(image_bytes: bytes, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Unable to decode image bytes")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return img.astype(np.float32)


def _preprocess_for_model(model_path: str, rgb: np.ndarray) -> np.ndarray:
    del model_path
    # Training models already apply preprocess_input inside the model graph.
    # Runtime should only provide float32 batched RGB tensors.
    return np.expand_dims(rgb.astype(np.float32), axis=0)


def _format_vector(probabilities: np.ndarray, precision: int = 6) -> List[float]:
    return [round(float(v), precision) for v in probabilities.tolist()]


def _find_last_conv_layer(model: tf.keras.Model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer
        if isinstance(layer, tf.keras.Model):
            nested = _find_last_conv_layer(layer)
            if nested is not None:
                return nested
    return None


def _gradcam_overlay(model: tf.keras.Model, preprocessed: np.ndarray, original_rgb: np.ndarray, class_idx: int) -> str:
    target_layer = _find_last_conv_layer(model)
    if target_layer is None:
        raise ValueError("No convolutional layer found for Grad-CAM")
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [target_layer.output, model.output],
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(preprocessed)
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)
    pooled = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(conv_outputs * pooled, axis=-1)
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()

    heatmap = cv2.resize(heatmap, (original_rgb.shape[1], original_rgb.shape[0]))
    heatmap_uint8 = np.uint8(255 * heatmap)
    colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(cv2.cvtColor(original_rgb.astype(np.uint8), cv2.COLOR_RGB2BGR), 0.5, colored, 0.5, 0)

    with io.BytesIO() as buffer:
        Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)).save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _saliency_overlay(model: tf.keras.Model, preprocessed: np.ndarray, original_rgb: np.ndarray, class_idx: int) -> str:
    inputs = tf.convert_to_tensor(preprocessed)
    with tf.GradientTape() as tape:
        tape.watch(inputs)
        predictions = model(inputs, training=False)
        loss = predictions[:, class_idx]

    gradients = tape.gradient(loss, inputs)[0]
    saliency = tf.reduce_max(tf.abs(gradients), axis=-1).numpy()
    saliency = saliency / (np.max(saliency) + 1e-8)
    saliency = cv2.resize(saliency, (original_rgb.shape[1], original_rgb.shape[0]))
    heatmap_uint8 = np.uint8(255 * saliency)
    colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_TURBO)
    overlay = cv2.addWeighted(cv2.cvtColor(original_rgb.astype(np.uint8), cv2.COLOR_RGB2BGR), 0.55, colored, 0.45, 0)

    with io.BytesIO() as buffer:
        Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)).save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _top_predictions(probabilities: np.ndarray, labels: List[str], k: int = 2) -> List[Tuple[str, float]]:
    idx = np.argsort(probabilities)[::-1][:k]
    return [(labels[int(i)], float(probabilities[int(i)])) for i in idx]


def _disease_why(label: str, confidence: float, top2: List[Tuple[str, float]]) -> str:
    if confidence < LOW_CONF_DISEASE_THRESHOLD:
        return "Uncertain disease prediction. Please upload a clearer leaf image."

    alt = top2[1][0] if len(top2) > 1 else "another class"
    label_lower = label.lower()
    if "blight" in label_lower:
        hint = "dark lesions and spreading necrotic patches"
    elif "rust" in label_lower:
        hint = "rust-like spots and orange-brown pustules"
    elif "spot" in label_lower:
        hint = "clustered spots and localized discoloration"
    elif "healthy" in label_lower:
        hint = "uniform green tissue without visible lesions"
    else:
        hint = "texture and color patterns consistent with this disease class"

    return f"Predicted {label} because the leaf shows {hint}. Secondary candidate was {alt}."


def _soil_why(label: str, confidence: float, top2: List[Tuple[str, float]]) -> str:
    if confidence < LOW_CONF_SOIL_THRESHOLD:
        return "Uncertain soil prediction. Please upload a clearer soil image."

    alt = top2[1][0] if len(top2) > 1 else "another soil class"
    hints = {
        "Alluvial Soil": "light mixed sediment texture and smooth granular appearance",
        "Black Soil": "dark dense texture with moisture-retaining visual traits",
        "Laterite Soil": "coarse weathered texture and brick-toned iron-rich granules",
        "Red Soil": "reddish hue and iron-rich coarse granular texture",
        "Yellow Soil": "yellowish mineral tone with dry loose granular structure",
        "Arid Soil": "pale dry surface texture with sparse organic matter cues",
        "Mountain Soil": "dark humus-rich texture with mixed rocky organic structure",
    }
    cue = hints.get(label, "dominant texture and color pattern")
    return f"Predicted {label} due to {cue}. Secondary candidate was {alt}."


def _predict(
    model_pair: LoadedModel,
    image_path: str,
    model_path: str,
    source_name: Optional[str] = None,
) -> Tuple[np.ndarray, float, str, PredictionTiming, str]:
    t0 = time.perf_counter()
    print("Image received")
    rgb = _read_and_resize_rgb(image_path)
    preprocessed = _preprocess_for_model(model_path, rgb)
    print("Preprocessed shape:", preprocessed.shape)
    t1 = time.perf_counter()

    probs = model_pair.model.predict(preprocessed, verbose=0)[0]
    print("Model output:", probs)
    if probs.ndim != 1:
        probs = np.squeeze(probs)
    class_idx = int(np.argmax(probs))
    if class_idx >= len(model_pair.labels):
        raise ValueError(f"Predicted class index {class_idx} is out of range for {len(model_pair.labels)} labels")
    confidence = float(probs[class_idx])
    mapped_label = model_pair.labels[class_idx]
    t2 = time.perf_counter()

    logger.info(
        "prediction_debug source=%s rgb_shape=%s tensor_shape=%s tensor_min=%.5f tensor_max=%.5f vector=%s pred_idx=%d mapped_label=%s confidence=%.5f",
        source_name or os.path.basename(image_path),
        tuple(rgb.shape),
        tuple(preprocessed.shape),
        float(np.min(preprocessed)),
        float(np.max(preprocessed)),
        _format_vector(probs),
        class_idx,
        mapped_label,
        confidence,
    )

    timings = PredictionTiming(
        preprocess_ms=(t1 - t0) * 1000.0,
        inference_ms=(t2 - t1) * 1000.0,
        total_ms=(t2 - t0) * 1000.0,
    )

    try:
        xai_visual = _gradcam_overlay(model_pair.model, preprocessed, rgb, class_idx)
    except Exception as ex:
        logger.warning("Grad-CAM generation failed: %s", ex)
        xai_visual = _saliency_overlay(model_pair.model, preprocessed, rgb, class_idx)

    return probs, confidence, mapped_label, timings, xai_visual


def _predict_from_rgb(
    model_pair: LoadedModel,
    rgb: np.ndarray,
    model_path: str,
    source_name: Optional[str] = None,
) -> Tuple[np.ndarray, float, str, PredictionTiming, str]:
    t0 = time.perf_counter()
    print("Image received")
    preprocessed = _preprocess_for_model(model_path, rgb)
    print("Preprocessed shape:", preprocessed.shape)
    t1 = time.perf_counter()

    probs = model_pair.model.predict(preprocessed, verbose=0)[0]
    print("Model output:", probs)
    if probs.ndim != 1:
        probs = np.squeeze(probs)
    class_idx = int(np.argmax(probs))
    if class_idx >= len(model_pair.labels):
        raise ValueError(f"Predicted class index {class_idx} is out of range for {len(model_pair.labels)} labels")
    confidence = float(probs[class_idx])
    mapped_label = model_pair.labels[class_idx]
    t2 = time.perf_counter()

    logger.info(
        "prediction_debug source=%s rgb_shape=%s tensor_shape=%s tensor_min=%.5f tensor_max=%.5f vector=%s pred_idx=%d mapped_label=%s confidence=%.5f",
        source_name or "uploaded_image",
        tuple(rgb.shape),
        tuple(preprocessed.shape),
        float(np.min(preprocessed)),
        float(np.max(preprocessed)),
        _format_vector(probs),
        class_idx,
        mapped_label,
        confidence,
    )

    timings = PredictionTiming(
        preprocess_ms=(t1 - t0) * 1000.0,
        inference_ms=(t2 - t1) * 1000.0,
        total_ms=(t2 - t0) * 1000.0,
    )

    try:
        xai_visual = _gradcam_overlay(model_pair.model, preprocessed, rgb, class_idx)
    except Exception as ex:
        logger.warning("Grad-CAM generation failed: %s", ex)
        xai_visual = _saliency_overlay(model_pair.model, preprocessed, rgb, class_idx)

    return probs, confidence, mapped_label, timings, xai_visual


def predict_plant_image(image_path: str) -> Dict[str, object]:
    ensure_models_trained()
    pair = _load_model_pair(PLANT_MODEL_PATH, PLANT_LABELS_PATH)
    probs, confidence, label, _, _ = _predict(
        pair,
        image_path,
        PLANT_MODEL_PATH,
        source_name=Path(image_path).name,
    )
    top2 = _top_predictions(probs, pair.labels, k=2)
    uncertain_msg = "Uncertain disease prediction. Please upload a clearer leaf image."
    is_uncertain = confidence < LOW_CONF_DISEASE_THRESHOLD

    return {
        "disease": uncertain_msg if is_uncertain else label,
        "confidence": round(confidence, 4),
        "why": uncertain_msg if is_uncertain else _disease_why(label, confidence, top2),
    }


def predict_plant_bytes(image_bytes: bytes, filename: Optional[str] = None) -> Dict[str, object]:
    ensure_models_trained()
    pair = _load_model_pair(PLANT_MODEL_PATH, PLANT_LABELS_PATH)
    rgb = _read_and_resize_rgb_bytes(image_bytes)
    probs, confidence, label, _, _ = _predict_from_rgb(
        pair,
        rgb,
        PLANT_MODEL_PATH,
        source_name=filename,
    )
    top2 = _top_predictions(probs, pair.labels, k=2)
    uncertain_msg = "Uncertain disease prediction. Please upload a clearer leaf image."
    is_uncertain = confidence < LOW_CONF_DISEASE_THRESHOLD

    return {
        "disease": uncertain_msg if is_uncertain else label,
        "confidence": round(confidence, 4),
        "why": uncertain_msg if is_uncertain else _disease_why(label, confidence, top2),
    }


def predict_soil_image(image_path: str) -> Dict[str, object]:
    ensure_models_trained()
    pair = _load_model_pair(SOIL_MODEL_PATH, SOIL_LABELS_PATH)
    probs, confidence, raw_label, _, _ = _predict(
        pair,
        image_path,
        SOIL_MODEL_PATH,
        source_name=Path(image_path).name,
    )
    label = _canonical_soil_label(raw_label)
    top2 = _top_predictions(probs, pair.labels, k=2)
    uncertain_msg = "Uncertain soil prediction. Please upload a clearer soil image."
    is_uncertain = confidence < LOW_CONF_SOIL_THRESHOLD

    return {
        "soil_type": uncertain_msg if is_uncertain else label,
        "confidence": round(confidence, 4),
        "why": uncertain_msg if is_uncertain else _soil_why(label, confidence, top2),
        "best_crops": [] if is_uncertain else SOIL_CROP_MAP.get(label, ["Rice", "Wheat", "Maize", "Pulses"]),
    }


def predict_soil_bytes(image_bytes: bytes, filename: Optional[str] = None) -> Dict[str, object]:
    ensure_models_trained()
    pair = _load_model_pair(SOIL_MODEL_PATH, SOIL_LABELS_PATH)
    rgb = _read_and_resize_rgb_bytes(image_bytes)
    probs, confidence, raw_label, _, _ = _predict_from_rgb(
        pair,
        rgb,
        SOIL_MODEL_PATH,
        source_name=filename,
    )
    label = _canonical_soil_label(raw_label)
    top2 = _top_predictions(probs, pair.labels, k=2)
    uncertain_msg = "Uncertain soil prediction. Please upload a clearer soil image."
    is_uncertain = confidence < LOW_CONF_SOIL_THRESHOLD

    return {
        "soil_type": uncertain_msg if is_uncertain else label,
        "confidence": round(confidence, 4),
        "why": uncertain_msg if is_uncertain else _soil_why(label, confidence, top2),
        "best_crops": [] if is_uncertain else SOIL_CROP_MAP.get(label, ["Rice", "Wheat", "Maize", "Pulses"]),
    }


def explain_plant_prediction(image_path: str) -> Dict[str, str]:
    prediction = predict_plant_image(image_path)
    return {
        "explanation": str(prediction["why"]),
        "xai_visual": prediction.get("xai_visual", ""),
    }


def explain_soil_prediction(image_path: str) -> Dict[str, str]:
    prediction = predict_soil_image(image_path)
    return {
        "explanation": str(prediction["why"]),
        "xai_visual": prediction.get("xai_visual", ""),
    }
