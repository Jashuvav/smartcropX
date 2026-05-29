# SmartCropX Code Audit Report

## Summary
This audit focused on active runtime paths, dead-code removal, model pipeline replacement, dependency repair, and end-to-end prediction stability.

## Problems Found And Actions Taken

| File / Area | Problem Found | Action Taken |
|---|---|---|
| backend/main.py | Prediction endpoints used temp-file-heavy flow and legacy sklearn-oriented runtime assumptions | Switched active prediction/explain endpoints to TensorFlow/Keras in-memory inference helpers and startup-loaded model service |
| backend/services/image_models.py | Active runtime used placeholder sklearn/joblib models instead of real deep-learning models; no stable visual XAI | Replaced with TensorFlow model loader, preprocessing parity, confidence thresholding, timing logs, plain-text explanations, and visual saliency/Grad-CAM fallback |
| backend/scripts/ml_image_models.py | Legacy compatibility path with stale model-loading expectations | Preserved as compatibility import wrapper to the active service layer |
| backend/training/ | Training pipeline missing after cleanup; no professional dataset/materialization flow | Added dataset preparation, disease training, soil training, and orchestration scripts |
| backend/requirements.txt | Runtime/training dependencies incomplete for TensorFlow path | Added TensorFlow, dataset, and crawler packages |
| frontend/src/pages/PlantDiseaseDetection.jsx | Result UI lacked optional visual XAI and only handled basic text output | Integrated visual XAI rendering while keeping clean text explanation |
| frontend/src/pages/SoilPredictor.jsx | Soil result UI did not render visual XAI | Integrated visual XAI rendering with existing result cards |
| frontend/package.json | Unused/dead dependency entries remained from earlier scaffolding | Removed unnecessary TS/type and web-vitals-related runtime clutter |
| frontend/src/index.js | Dead reportWebVitals scaffold | Removed unused import and invocation |
| root package.json / package-lock.json | Duplicate npm manifest at repo root | Removed duplicate root manifests and kept frontend manifest as canonical |
| backend legacy scripts | Dead debug/training/XAI/experimental scripts remained | Removed obsolete scripts and minimal test/debug files |
| stale datasets/temp folders | Old datasets, temp uploads, and experimental folders polluted runtime surface | Removed obsolete folders, temp artifacts, graph outputs, and unused frontend blockchain/truffle assets |
| .gitignore | Training artifacts and generated outputs not fully covered | Added ignores for generated datasets/logs while keeping final `.keras` model artifacts allowed |

## Files Removed

### Root
- package.json
- package-lock.json

### Frontend
- frontend/src/pages/ApiTestPage.jsx
- frontend/src/config/apiTest.js
- frontend/src/reportWebVitals.js
- frontend/src/logo.svg
- frontend/src/App.test.js
- frontend/src/setupTests.js
- frontend/tsconfig.json
- frontend/truffle-config.js
- frontend/contracts/
- frontend/migrations/
- frontend/test/
- frontend/truffle/
- frontend/tsc_output.txt

### Backend
- backend/backend.txt
- backend/frotnedn.txt
- backend/lib.txt
- backend/create_fallback_soil_model.py
- backend/debug_api.py
- backend/main_minimal.py
- backend/render_deploy_test.py
- backend/test_fallback_model.py
- backend/test_models.py
- backend/test_startup.py
- backend/verify_start.py
- backend/scripts/advanced_plantdoc_trainer.py
- backend/scripts/advanced_soil_trainer.py
- backend/scripts/clean_soil_dataset.py
- backend/scripts/deployment_ready_trainer.py
- backend/scripts/main.py
- backend/scripts/main_original.py
- backend/scripts/model_compatibility_optimizer.py
- backend/scripts/predict.py
- backend/scripts/predict_plantdoc.py
- backend/scripts/predict_soil.py
- backend/scripts/predict_with_graph.py
- backend/scripts/preprocess_data.py
- backend/scripts/preprocess_plantdoc.py
- backend/scripts/run_training_pipeline.py
- backend/scripts/strict_image_validator.py
- backend/scripts/train_models.py
- backend/scripts/train_plantdoc_model.py
- backend/scripts/train_soil_model.py
- backend/scripts/train_weather_model.py
- backend/scripts/trial.py
- backend/scripts/xai_gradcam.py
- backend/scripts/xai_shap.py
- backend/scripts/useless/
- backend/scripts/predicted_graphs/
- backend/PlantDocTmp/
- backend/processed_data/
- backend/Soil/
- backend/SoilDataset/
- backend/SoilTmpRepo2/
- backend/temp_uploads/
- backend/plantdoc.zip
- backend/uploaded_image.jpg
- backend/blockchain/

## Remaining Limitation
- backend/venv remains in the repo because an earlier locked native file blocked safe deletion. Runtime now uses it intentionally for TensorFlow/Keras training and inference.
- Soil model accuracy is materially lower than the disease model because the available automatic soil dataset source had to be built from crawled public images rather than a clean labeled benchmark image set.
