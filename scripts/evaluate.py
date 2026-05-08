import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from app.classifier import ai_classifier


print("\n[1] Loading datasets...")

with open("data/redteam.json", "r", encoding="utf-8") as f:
    data1 = json.load(f)

with open("data/redteam_advanced.json", "r", encoding="utf-8") as f:
    data2 = json.load(f)

all_data = data1 + data2

print(f"Loaded {len(all_data)} prompts")


rows = []

for item in all_data:

    prompt = item.get("prompt", "")

    category = item.get(
        "category",
        "unknown"
    )

    label = item.get(
        "label",
        "unsafe"
    )

    rows.append({
        "prompt": prompt,
        "category": category,
        "true_label": label
    })

df = pd.DataFrame(rows)

print(df.head())


print("\n[2] Running hybrid classifier...")

predictions = []
detected_categories = []
confidences = []
latencies = []

for i, prompt in enumerate(df["prompt"]):

    start = time.time()

    verdict, detected_cat, confidence = (
        ai_classifier(prompt)
    )

    end = time.time()

    latency_ms = (
        (end - start) * 1000
    )

    predictions.append(verdict)
    detected_categories.append(detected_cat)
    confidences.append(round(confidence, 4))
    latencies.append(round(latency_ms, 2))

    print(
        f"[{i}] "
        f"{verdict} | "
        f"{detected_cat} | "
        f"{confidence:.4f}"
    )

print("\n[2 DONE]")


print("\n[3] Saving results...")

df["prediction"] = predictions
df["detected_category"] = detected_categories
df["confidence"] = confidences
df["latency_ms"] = latencies

df["correct"] = (
    df["true_label"] == df["prediction"]
)

os.makedirs("results", exist_ok=True)

df.to_csv(
    "results/hybrid_eval_results.csv",
    index=False
)

print("[3 DONE]")


print("\n[4] Computing metrics...")


def convert_binary(x):

    x = str(x).lower()

    if x == "safe":
        return "safe"

    return "unsafe"

df["binary_true"] = df["true_label"].apply(
    convert_binary
)

df["binary_pred"] = df["prediction"].apply(
    convert_binary
)


accuracy = accuracy_score(
    df["binary_true"],
    df["binary_pred"]
)

precision = precision_score(
    df["binary_true"],
    df["binary_pred"],
    pos_label="unsafe",
    zero_division=0
)

recall = recall_score(
    df["binary_true"],
    df["binary_pred"],
    pos_label="unsafe",
    zero_division=0
)

f1 = f1_score(
    df["binary_true"],
    df["binary_pred"],
    pos_label="unsafe",
    zero_division=0
)

print("\n===== FINAL METRICS =====")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\n===== CLASSIFICATION REPORT =====")

classification_report(
    df["binary_true"],
    df["binary_pred"],
    zero_division=0
)


print("\n[5] Generating confusion matrix...")
confusion_matrix(
    df["binary_true"],
    df["binary_pred"]
)

print(cm)

plt.figure(figsize=(5, 5))

plt.imshow(cm)

plt.title("Hybrid Confusion Matrix")

plt.xlabel("Predicted")
plt.ylabel("True")

plt.colorbar()

plt.savefig(
    "results/hybrid_confusion_matrix.png"
)

print("[5 DONE]")

print("\n[6] Generating accuracy curve...")

thresholds = np.arange(0.1, 1.0, 0.1)

accuracies = []
recalls = []

for t in thresholds:

    temp_preds = []

    for conf, pred in zip(
        df["confidence"],
        df["prediction"]
    ):

        if conf >= t:
            temp_preds.append(pred)
        else:
            temp_preds.append("safe")

    acc = accuracy_score(
        df["true_label"],
        temp_preds
    )

    rec = recall_score(
        df["true_label"],
        temp_preds,
        pos_label="unsafe",
        zero_division=0
    )

    accuracies.append(acc)
    recalls.append(rec)

plt.figure(figsize=(8, 5))

plt.plot(
    thresholds,
    accuracies,
    marker="o",
    label="Accuracy"
)

plt.plot(
    thresholds,
    recalls,
    marker="o",
    label="Recall"
)

plt.xlabel("Threshold")
plt.ylabel("Score")

plt.title(
    "Accuracy vs Strictness Curve"
)

plt.legend()

plt.savefig(
    "results/hybrid_accuracy_curve.png"
)

print("[6 DONE]")


print("\n===== LATENCY =====")

print(
    f"Average latency: "
    f"{np.mean(latencies):.2f} ms"
)

print(
    f"P95 latency: "
    f"{np.percentile(latencies,95):.2f} ms"
)

print("\n===== EVERYTHING FINISHED =====")