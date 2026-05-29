import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_ROOT = BASE_DIR / "training" / "disease" / "dataset"
LOG_DIR = BASE_DIR / "training" / "disease" / "logs"
MODELS_DIR = BASE_DIR / "models"

IMG_SIZE = (224, 224)
BATCH_SIZE = 24
EPOCHS = 12
SEED = 42


def _build_datasets():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_ROOT / "train",
        label_mode="categorical",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        seed=SEED,
        shuffle=True,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_ROOT / "val",
        label_mode="categorical",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        seed=SEED,
        shuffle=False,
    )
    test_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_ROOT / "test",
        label_mode="categorical",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        seed=SEED,
        shuffle=False,
    )

    class_names = train_ds.class_names
    aug = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.12),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomContrast(0.2),
    ])

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.map(lambda x, y: (aug(x, training=True), y), num_parallel_calls=autotune)
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)
    test_ds = test_ds.prefetch(autotune)

    return train_ds, val_ds, test_ds, class_names


def _class_weights(dataset):
    counts = None
    for _, y in dataset:
        batch_counts = tf.reduce_sum(y, axis=0).numpy()
        counts = batch_counts if counts is None else counts + batch_counts

    total = float(np.sum(counts))
    classes = len(counts)
    weights = {i: total / (classes * float(c)) for i, c in enumerate(counts)}
    return weights


def _build_model(num_classes: int):
    base = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    )
    base.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = tf.keras.applications.efficientnet.preprocess_input(inputs)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base


def train() -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    train_ds, val_ds, test_ds, class_names = _build_datasets()
    cw = _class_weights(train_ds)

    model, base = _build_model(len(class_names))

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.4, patience=2, min_lr=1e-6),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(MODELS_DIR / "best_plantdoc_model.keras"),
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]

    history_head = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=max(4, EPOCHS // 2),
        callbacks=callbacks,
        class_weight=cw,
        verbose=1,
    )

    base.trainable = True
    for layer in base.layers[:-40]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_ft = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        initial_epoch=history_head.epoch[-1] + 1,
        callbacks=callbacks,
        class_weight=cw,
        verbose=1,
    )

    best_model = tf.keras.models.load_model(MODELS_DIR / "best_plantdoc_model.keras")
    test_loss, test_acc = best_model.evaluate(test_ds, verbose=0)

    all_true = []
    all_pred = []
    for x_batch, y_batch in test_ds:
        probs = best_model.predict(x_batch, verbose=0)
        all_pred.extend(np.argmax(probs, axis=1).tolist())
        all_true.extend(np.argmax(y_batch.numpy(), axis=1).tolist())

    cm = confusion_matrix(all_true, all_pred)
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, cmap="Greens")
    plt.title("Disease Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(LOG_DIR / "confusion_matrix.png", dpi=180)
    plt.close()

    with open(MODELS_DIR / "plantdoc_class_names.json", "w", encoding="utf-8") as f:
        json.dump({"classes": class_names}, f, indent=2)

    metrics = {
        "train_accuracy_final": float(history_ft.history["accuracy"][-1]),
        "val_accuracy_final": float(history_ft.history["val_accuracy"][-1]),
        "test_accuracy": float(test_acc),
        "test_loss": float(test_loss),
        "num_classes": len(class_names),
        "model_path": str(MODELS_DIR / "best_plantdoc_model.keras"),
        "labels_path": str(MODELS_DIR / "plantdoc_class_names.json"),
    }

    with open(LOG_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))
    return metrics


if __name__ == "__main__":
    train()
