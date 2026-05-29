# Disease Model Training Report

## Dataset Source
- Source: Hugging Face dataset `GVJahnavi/Plant_village_subset`
- Acquisition: downloaded automatically during dataset preparation
- Final prepared path: `backend/training/disease/dataset/`

## Final Classes
- Apple__Apple_scab
- Apple__Black_rot
- Apple__Cedar_apple_rust
- Apple___healthy
- Blueberry___healthy
- Cherry_(including_sour)___Powdery_mildew
- Cherry_(including_sour)___healthy
- Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot
- Corn_(maize)___Common_rust_
- Corn_(maize)___Northern_Leaf_Blight
- Corn_(maize)___healthy
- Grape___Black_rot
- Grape___Esca_(Black_Measles)
- Grape___Leaf_blight_(Isariopsis_Leaf_Spot)
- Grape___healthy

## Dataset Preparation
- Maximum capped samples per class: 500
- Corrupt-image filtering: enabled
- Split structure:
  - train: `backend/training/disease/dataset/train/`
  - val: `backend/training/disease/dataset/val/`
  - test: `backend/training/disease/dataset/test/`
- Final counts by class are saved in `backend/training/disease/logs/dataset_summary.json`

## Model Architecture
- Framework: TensorFlow / Keras
- Backbone: EfficientNetB0
- Input size: 224x224 RGB
- Head: global average pooling + dropout + dense softmax
- Training strategy:
  - frozen-head phase
  - fine-tuning phase on last backbone blocks

## Training Configuration
- Batch size: 24
- Epoch target: 12
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
- Train accuracy: 0.9847
- Validation accuracy: 0.9842
- Test accuracy: 0.9852
- Test loss: 0.0418

## Artifacts
- Saved model: `backend/models/best_plantdoc_model.keras`
- Saved labels: `backend/models/plantdoc_class_names.json`
- Metrics: `backend/training/disease/logs/metrics.json`
- Confusion matrix: `backend/training/disease/logs/confusion_matrix.png`

## Notes
- This model is a real trained TensorFlow model and is the active backend runtime model for plant disease detection.
