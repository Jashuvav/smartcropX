# Model Runtime Report

## Active Models
- Disease model: `backend/models/best_plantdoc_model.keras`
- Disease labels: `backend/models/plantdoc_class_names.json`
- Soil model: `backend/models/soil_classifier.keras`
- Soil labels: `backend/models/class_names.json`

## Startup Loading Status
- Backend startup preloads both models once into memory.
- Verified startup log showed:
  - soil classifier loaded successfully
  - plant disease predictor loaded successfully
  - backend API ready

## Runtime Behavior
- Inference service: `backend/services/image_models.py`
- API integration: `backend/main.py`
- Request handling uses in-memory bytes for prediction/explanation routes.
- Models are not reloaded per request.

## Preprocessing Details
- Image decode: OpenCV decode from bytes or file path
- Color space: BGR to RGB
- Resize: 224x224
- Disease preprocessing: `tf.keras.applications.efficientnet.preprocess_input`
- Soil preprocessing: `tf.keras.applications.mobilenet_v2.preprocess_input`
- Batch dimension: added before inference

## Confidence Thresholds
- Disease uncertain threshold: 0.55
- Soil uncertain threshold: 0.55
- Behavior: if below threshold, API returns `Uncertain` instead of a forced label

## Explainable AI
- Plain-language explanation: always returned
- Visual XAI:
  - first attempt: Grad-CAM on the loaded model graph
  - stable fallback: input-gradient saliency heatmap overlay
- Verified non-empty `xai_visual` payloads for both disease and soil explain endpoints

## API Response Format

### POST `/predict`
Returns:
- `disease`
- `confidence`
- `why`
- `xai_visual`
- `real_model_used`
- `model_source`
- `timings_ms`

### POST `/predict-soil`
Returns:
- `soil_type`
- `confidence`
- `why`
- `best_crops`
- `xai_visual`
- `real_model_used`
- `model_source`
- `timings_ms`

### POST `/api/disease/explain`
Returns:
- `status`
- `explanation`
- `xai_visual`

### POST `/api/soil/explain`
Returns:
- `status`
- `explanation`
- `xai_visual`

## Performance Notes
- Request flow avoids repeated disk writes for active prediction/explain routes.
- Backend logs preprocessing time, inference time, and total time per request.
- Example observed disease inference total was roughly 2.8s on CPU for a live request.

## Verification Summary
- Backend startup: passed
- Frontend production build: passed
- Disease API predictions: passed with real model responses
- Soil API predictions: passed with real model responses
- Visual XAI payload: passed for both explain endpoints
