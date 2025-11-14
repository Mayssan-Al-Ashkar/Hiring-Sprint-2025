"""
Train an ML price regressor (HistGradientBoostingRegressor) for repair cost.

Inputs:
  A CSV file with columns:
    image_path   : local filesystem path or http(s) URL to the image
    vehicle_type : one of [car, truck, motorcycle, scooter, boat]
    total_usd    : numeric ground-truth total repair cost in USD

Usage:
  # Activate your venv and install requirements in ml/requirements.txt
  # Prepare a CSV at ml/data/claims.csv
  python -m ml.train_price_gbm --csv ml/data/claims.csv --out ml/models/price_gbm.pkl

Notes:
  - This script uses the same YOLO model and feature pipeline as the service,
    so it must be executed from the project root (or adjust PYTHONPATH).
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import io
import math
import json
import numpy as np
import pandas as pd
import requests
from PIL import Image
from sklearn.ensemble import HistGradientBoostingRegressor
import joblib

from ml.services.inference import load_model, detect_from_numpy, load_price_map, aggregate_costs_for_classes
from ml.services.features import compute_features, FEATURE_NAMES


def read_image_any(path: str) -> np.ndarray:
    if path.startswith("http://") or path.startswith("https://"):
        resp = requests.get(path, timeout=15)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert("RGB")
        return np.array(img)
    else:
        img = Image.open(path).convert("RGB")
        return np.array(img)


def build_dataset(csv_path: Path) -> tuple[np.ndarray, np.ndarray]:
    price_map = load_price_map()
    df = pd.read_csv(csv_path)
    xs: list[np.ndarray] = []
    ys: list[float] = []
    model = load_model()  # ensure weights are loaded once
    for idx, row in df.iterrows():
        image_path = str(row["image_path"])
        vehicle_type = row.get("vehicle_type", "car")
        y = float(row["total_usd"])

        try:
            img = read_image_any(image_path)
        except Exception as e:
            print(f"[WARN] skip #{idx}: cannot read {image_path}: {e}")
            continue

        det = detect_from_numpy(img)
        rule_costs = aggregate_costs_for_classes(det["classes"], price_map, vehicle_type, det.get("areas"))
        feats = compute_features(det, vehicle_type, rule_costs["totals"]["min"], image_shape=(img.shape[0], img.shape[1]))

        xs.append(feats)
        ys.append(y)

    X = np.vstack(xs) if xs else np.zeros((0, len(FEATURE_NAMES)))
    y = np.asarray(ys, dtype=float)
    return X, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=str, required=True, help="Path to training CSV with image_path, vehicle_type, total_usd")
    ap.add_argument("--out", type=str, default=str(Path("ml") / "models" / "price_gbm.pkl"))
    ap.add_argument("--test_split", type=float, default=0.2)
    args = ap.parse_args()

    X, y = build_dataset(Path(args.csv))
    if X.shape[0] < 20:
        raise RuntimeError(f"Not enough samples ({X.shape[0]}) to train. Provide at least ~100 rows.")

    # Train simple HGBR on log1p(target)
    y_log = np.log1p(y)
    model = HistGradientBoostingRegressor(
        max_depth=6,
        learning_rate=0.05,
        max_iter=500,
        min_samples_leaf=20,
        l2_regularization=0.0,
        validation_fraction=0.1,
        random_state=42,
    )
    model.fit(X, y_log)

    # Save model and feature names
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"model": model, "feature_names": FEATURE_NAMES}
    joblib.dump(payload, out)
    print(f"[OK] saved model to {out} (n={X.shape[0]} samples)")


if __name__ == "__main__":
    main()


