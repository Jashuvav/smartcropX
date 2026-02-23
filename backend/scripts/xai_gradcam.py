"""
Grad-CAM (Gradient-weighted Class Activation Mapping) for plant disease & soil models.
Generates heatmaps showing which image regions influenced the model's decision.
Falls back to a mock heatmap if the model is unavailable or incompatible.
"""
import numpy as np
import os
import io
import base64
import logging
from PIL import Image

logger = logging.getLogger(__name__)

# ─── helpers ────────────────────────────────────────────────────────
def _img_to_base64(pil_img: Image.Image, fmt: str = "PNG") -> str:
    """Convert a PIL image to a data-URI base64 string."""
    buf = io.BytesIO()
    pil_img.save(buf, format=fmt)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/{fmt.lower()};base64,{b64}"


def _apply_colormap(heatmap_np: np.ndarray) -> np.ndarray:
    """Apply a red-yellow-blue jet-like colormap to a [0..1] heatmap.
       Returns an RGB uint8 array."""
    import cv2
    heatmap_uint8 = np.uint8(255 * heatmap_np)
    coloured = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    return cv2.cvtColor(coloured, cv2.COLOR_BGR2RGB)


def _overlay(original: np.ndarray, heatmap_rgb: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    """Blend original image with coloured heatmap."""
    from PIL import Image as PILImage
    orig_resized = np.array(PILImage.fromarray(original).resize(
        (heatmap_rgb.shape[1], heatmap_rgb.shape[0])))
    blended = (alpha * heatmap_rgb.astype(np.float32)
               + (1 - alpha) * orig_resized.astype(np.float32))
    return np.clip(blended, 0, 255).astype(np.uint8)


# ─── true Grad-CAM ─────────────────────────────────────────────────
def _gradcam_real(model, img_array: np.ndarray, class_idx: int, img_size: tuple):
    """
    Compute Grad-CAM for a Keras CNN model.
    `img_array`  – preprocessed (1, H, W, 3) float tensor
    `class_idx`  – predicted (or target) class index
    `img_size`   – (H, W) of the original image for resizing the heatmap
    Returns heatmap as a numpy array of shape (H, W) in [0, 1].
    """
    import tensorflow as tf

    # Find the last Conv2D layer
    last_conv = None
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            last_conv = layer
            break
        # also check DepthwiseConv2D etc.
        if 'conv' in layer.name.lower() and hasattr(layer, 'output'):
            last_conv = layer
            break

    if last_conv is None:
        raise ValueError("No Conv2D layer found in the model – cannot compute Grad-CAM")

    # Build a GradientTape-compatible model.
    # For Sequential models that haven't been called through functional API,
    # we construct an explicit input tensor and thread through the layers.
    try:
        # Try functional-style access first
        model_input = model.input
        if isinstance(model_input, list):
            model_input = model_input[0]
        model_output = model.output
        if isinstance(model_output, list):
            model_output = model_output[0]
        grad_model = tf.keras.Model(
            inputs=model_input,
            outputs=[last_conv.output, model_output]
        )
    except (AttributeError, ValueError):
        # Sequential/unbuild model – create a new Input and forward manually
        inp = tf.keras.Input(shape=img_array.shape[1:])
        x = inp
        conv_output = None
        for layer in model.layers:
            x = layer(x)
            if layer.name == last_conv.name:
                conv_output = x
        grad_model = tf.keras.Model(inputs=inp, outputs=[conv_output, x])

    with tf.GradientTape() as tape:
        conv_out, predictions = grad_model(img_array)
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_out)              # (1, h, w, filters)
    weights = tf.reduce_mean(grads, axis=(1, 2))       # (1, filters)

    cam = tf.reduce_sum(conv_out * weights[:, tf.newaxis, tf.newaxis, :], axis=-1)  # (1, h, w)
    cam = tf.nn.relu(cam)[0]                           # (h, w)
    cam = cam / (tf.reduce_max(cam) + 1e-8)            # normalise → [0, 1]

    # Resize to original
    cam_np = cam.numpy()
    # Convert to uint8 for PIL resize compatibility
    cam_uint8 = np.uint8(cam_np * 255)
    cam_resized = np.array(
        Image.fromarray(cam_uint8).resize((img_size[1], img_size[0]), Image.BILINEAR)
    ).astype(np.float32) / 255.0
    return cam_resized


# ─── mock fallback ──────────────────────────────────────────────────
def _gradcam_mock(img_size: tuple):
    """Generate a plausible-looking mock Grad-CAM heatmap (centred Gaussian)."""
    h, w = img_size
    y = np.linspace(-1, 1, h)
    x = np.linspace(-1, 1, w)
    X, Y = np.meshgrid(x, y)
    # Off-centre Gaussian
    cx, cy = np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3)
    sigma = np.random.uniform(0.35, 0.6)
    heatmap = np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * sigma ** 2))
    heatmap = heatmap / (heatmap.max() + 1e-8)
    return heatmap


# ─── public API ─────────────────────────────────────────────────────
def explain_disease_image(image_path: str):
    """
    Run Grad-CAM on the plant disease model for the given image.
    Returns a dict with base64 heatmap, overlay, prediction, confidence, and top regions.
    Falls back to mock heatmap if the model or TF ops fail.
    """
    import cv2

    if not os.path.exists(image_path):
        return {"error": f"Image not found: {image_path}"}

    original = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    orig_h, orig_w = original.shape[:2]
    use_fallback = False
    prediction_info = {}

    try:
        from predict_plantdoc import load_model, load_class_names, get_healthy_classes
        model = load_model()
        class_names = load_class_names()
        healthy = get_healthy_classes()

        # Preprocess for the model (224×224)
        img = cv2.resize(original, (224, 224)).astype(np.float32) / 255.0
        img_batch = np.expand_dims(img, axis=0)

        preds = model.predict(img_batch)[0]
        pred_idx = int(np.argmax(preds))
        pred_class = class_names[pred_idx]
        confidence = float(preds[pred_idx])
        health_status = "HEALTHY" if pred_class in healthy else "DISEASED"

        prediction_info = {
            "class": pred_class,
            "confidence": round(confidence, 4),
            "status": health_status,
        }

        # Grad-CAM
        try:
            heatmap = _gradcam_real(model, img_batch, pred_idx, (orig_h, orig_w))
        except Exception as gc_err:
            logger.warning(f"Grad-CAM failed, using mock: {gc_err}", exc_info=True)
            heatmap = _gradcam_mock((orig_h, orig_w))
            use_fallback = True

    except Exception as model_err:
        logger.warning(f"Disease model unavailable, using mock: {model_err}", exc_info=True)
        heatmap = _gradcam_mock((orig_h, orig_w))
        use_fallback = True
        prediction_info = {
            "class": "Unknown (model unavailable)",
            "confidence": 0.0,
            "status": "UNKNOWN",
        }

    # Build coloured heatmap + overlay images
    heatmap_rgb = _apply_colormap(heatmap)
    overlay_rgb = _overlay(original, heatmap_rgb, alpha=0.45)

    heatmap_pil = Image.fromarray(heatmap_rgb)
    overlay_pil = Image.fromarray(overlay_rgb)

    # Identify top-activation regions
    regions = _top_regions(heatmap, k=3)

    return {
        "prediction": prediction_info,
        "heatmap": _img_to_base64(heatmap_pil),
        "overlay": _img_to_base64(overlay_pil),
        "regions": regions,
        "method": "mock-gradcam" if use_fallback else "grad-cam",
        "explanation": (
            f"The highlighted areas show the image regions that most influenced the model's "
            f"prediction of '{prediction_info.get('class', 'N/A')}'. "
            f"Brighter/warmer colours indicate stronger influence."
        ),
    }


def explain_soil_image(image_path: str):
    """
    Run Grad-CAM on the soil classifier model for the given image.
    Returns a dict with base64 heatmap, overlay, prediction, confidence, and regions.
    Falls back to mock heatmap if the model fails.
    """
    import cv2

    if not os.path.exists(image_path):
        return {"error": f"Image not found: {image_path}"}

    original = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    orig_h, orig_w = original.shape[:2]
    use_fallback = False
    prediction_info = {}

    SOIL_CLASSES = ['Alluvial soil', 'Black Soil', 'Clay soil', 'Red soil']
    IMG_SIZE = (180, 180)

    try:
        import tensorflow as tf
        MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "soil_classifier.keras")
        model = tf.keras.models.load_model(MODEL_PATH)

        img = cv2.resize(original, IMG_SIZE).astype(np.float32) / 255.0
        img_batch = np.expand_dims(img, axis=0)

        preds = model.predict(img_batch)[0]
        pred_idx = int(np.argmax(preds))
        pred_class = SOIL_CLASSES[pred_idx]
        confidence = float(preds[pred_idx]) * 100

        prediction_info = {
            "prediction": pred_class,
            "confidence": round(confidence, 2),
        }

        try:
            heatmap = _gradcam_real(model, img_batch, pred_idx, (orig_h, orig_w))
        except Exception as gc_err:
            logger.warning(f"Soil Grad-CAM failed, using mock: {gc_err}")
            heatmap = _gradcam_mock((orig_h, orig_w))
            use_fallback = True

    except Exception as model_err:
        logger.warning(f"Soil model unavailable, using mock: {model_err}")
        heatmap = _gradcam_mock((orig_h, orig_w))
        use_fallback = True
        prediction_info = {
            "prediction": "Unknown (model unavailable)",
            "confidence": 0.0,
        }

    heatmap_rgb = _apply_colormap(heatmap)
    overlay_rgb = _overlay(original, heatmap_rgb, alpha=0.45)

    heatmap_pil = Image.fromarray(heatmap_rgb)
    overlay_pil = Image.fromarray(overlay_rgb)

    regions = _top_regions(heatmap, k=3)

    return {
        "prediction": prediction_info,
        "heatmap": _img_to_base64(heatmap_pil),
        "overlay": _img_to_base64(overlay_pil),
        "regions": regions,
        "method": "mock-gradcam" if use_fallback else "grad-cam",
        "explanation": (
            f"The highlighted areas show the soil texture/colour regions that most influenced "
            f"the model's prediction of '{prediction_info.get('prediction', 'N/A')}'. "
            f"Brighter/warmer colours indicate stronger influence."
        ),
    }


# ─── helper: top-activation regions ────────────────────────────────
def _top_regions(heatmap: np.ndarray, k: int = 3):
    """Return the k highest-activation regions as {x, y, intensity} dicts."""
    from scipy import ndimage

    # Threshold at 70% of max
    thresh = heatmap > 0.7 * heatmap.max()
    labelled, n_features = ndimage.label(thresh)
    regions = []
    for i in range(1, n_features + 1):
        ys, xs = np.where(labelled == i)
        if len(ys) == 0:
            continue
        cy, cx = int(ys.mean()), int(xs.mean())
        intensity = float(heatmap[ys, xs].mean())
        regions.append({"x": cx, "y": cy, "intensity": round(intensity, 3), "size": int(len(ys))})

    regions.sort(key=lambda r: r["intensity"], reverse=True)
    return regions[:k]
