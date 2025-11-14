from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
from io import BytesIO
import base64

from ml.services.inference import (
    load_price_map,
    detect_from_numpy,
    aggregate_costs_for_classes,
    compare_before_after,
    normalize_class_key,
)

app = FastAPI(title="Car Damage Estimation API")


def read_image_file(file: UploadFile) -> np.ndarray:
    data = file.file.read()
    img = Image.open(BytesIO(data)).convert("RGB")
    return np.array(img)


def image_to_b64(img_rgb: np.ndarray) -> str:
    pil = Image.fromarray(img_rgb.astype("uint8"), "RGB")
    buf = BytesIO()
    pil.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


@app.post("/predict")
async def predict(image: UploadFile = File(...), vehicle_type: str | None = None):
    img = read_image_file(image)
    det = detect_from_numpy(img)
    price_map = load_price_map()
    cost_summary = aggregate_costs_for_classes(det["classes"], price_map, vehicle_type)

    per_class_costs = cost_summary["per_class_costs"]
    dets = []
    for idx, cls in enumerate(det["classes"]):
        norm = normalize_class_key(cls)
        each = per_class_costs.get(norm, {}).get("min_each")
        conf_list = det.get("confidences", [])
        dets.append({
            "class": cls,
            "confidence": float(conf_list[idx]) if idx < len(conf_list) else None,
            "each_cost_usd": float(each) if each is not None else None,
        })

    return JSONResponse({
        "classes": det["classes"],
        "detections": dets,
        "counts": cost_summary["counts"],
        "per_class_costs": cost_summary["per_class_costs"],
        "totals": cost_summary["totals"],
        "annotated_image_b64": image_to_b64(det["annotated_image"]),
    })


@app.post("/compare")
async def compare(before: UploadFile = File(...), after: UploadFile = File(...), vehicle_type: str | None = None):
    before_img = read_image_file(before)
    after_img = read_image_file(after)
    price_map = load_price_map()
    # Use new-damage costs with vehicle_type
    summary = compare_before_after(before_img, after_img, price_map)
    # Recompute cost summary with vehicle_type for deltas
    expanded_new = []
    for cls, n in summary["new_damage_counts"].items():
        expanded_new.extend([cls] * n)
    vt_costs = aggregate_costs_for_classes(expanded_new, price_map, vehicle_type)
    summary["new_damage_costs"] = vt_costs
    return JSONResponse({
        "before_counts": summary["before_counts"],
        "after_counts": summary["after_counts"],
        "new_damage_counts": summary["new_damage_counts"],
        "new_damage_costs": summary["new_damage_costs"],
        "before_annotated_b64": image_to_b64(summary["before"]["annotated_image"]),
        "after_annotated_b64": image_to_b64(summary["after"]["annotated_image"]),
    })


