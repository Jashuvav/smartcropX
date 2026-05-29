# Soil Model Training Report

## Dataset Source
- Source type: curated labeled research dataset downloaded from `Phantom-fs/Soil-Classification-Dataset`
- Active source subset: `Orignal-Dataset` from the public GitHub repository
- Download URL: `https://codeload.github.com/Phantom-fs/Soil-Classification-Dataset/zip/refs/heads/main`
- Final prepared path: `backend/training/soil/dataset/`

## Final Classes
- Alluvial Soil
- Arid Soil
- Black Soil
- Laterite Soil
- Mountain Soil
- Red Soil
- Yellow Soil

## Dataset Preparation
- Downloaded from a published research dataset repository instead of a web crawl
- Deduplication: enabled using both SHA-256 file hashing and resized RGB signature filtering
- Corrupt-image filtering: enabled
- Normalization step: all copied split images re-encoded to JPEG to avoid invalid-format failures
- Final counts:
  - Alluvial Soil: 50
  - Arid Soil: 279
  - Black Soil: 234
  - Laterite Soil: 214
  - Mountain Soil: 191
  - Red Soil: 107
  - Yellow Soil: 65
- Split structure:
  - train: `backend/training/soil/dataset/train/`
  - val: `backend/training/soil/dataset/val/`
  - test: `backend/training/soil/dataset/test/`

## Model Architecture
- Framework: TensorFlow / Keras
- Backbone: MobileNetV2
- Input size: 224x224 RGB
- Head: global average pooling + dropout + dense softmax
- Training strategy:
  - frozen-head phase
  - fine-tuning phase on late backbone layers

## Training Configuration
- Batch size: 20
- Epoch target: 14
- Augmentations:
  - random horizontal flip
  - random rotation
  - random zoom
  - random contrast
- Optimization:
  - Adam
  - early stopping
  - reduce-on-plateau LR scheduling
  - model checkpointing
- Class imbalance handling: class weights computed from train split

## Metrics
- Train accuracy: 0.8539
- Validation accuracy: 0.7381
- Test accuracy: 0.7978
- Test loss: 0.6352

## Artifacts
- Saved model: `backend/models/soil_classifier.keras`
- Saved labels: `backend/models/class_names.json`
- Metrics: `backend/training/soil/logs/metrics.json`

## Notes
- This is a real trained TensorFlow model and is the active backend runtime model for soil prediction.
- The active training source no longer depends on Bing or `icrawler`.
- Test accuracy improved substantially over the previous crawl-built dataset and the runtime artifact path remained unchanged, so backend inference continues to read `backend/models/soil_classifier.keras` directly.
