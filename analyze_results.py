import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


print("\n[1] Loading evaluation results...")

df = pd.read_csv(
    "results/hybrid_eval_results.csv"
)

print(df.head())

true_col = "true_label"
pred_col = "prediction"
conf_col = "confidence"

print("\n[2] Converting labels...")

def to_binary(x):

    x = str(x).lower()

    if x == "safe":
        return "safe"

    return "unsafe"

df["binary_true"] = df[true_col].apply(
    to_binary
)

df["binary_pred"] = df[pred_col].apply(
    to_binary
)

print(
    df[["binary_true", "binary_pred"]]
    .head()
)

print("\n[3] Computing metrics...")

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

print(classification_report(
    df["binary_true"],
    df["binary_pred"],
    zero_division=0
))



print("\n[4] Generating confusion matrix...")

cm = confusion_matrix(
    df["binary_true"],
    df["binary_pred"]
)

print(cm)

plt.figure(figsize=(6,6))

plt.imshow(cm)

plt.title("Confusion Matrix")

plt.xlabel("Predicted")
plt.ylabel("True")

plt.colorbar()

plt.savefig(
    "results/confusion_matrix_final.png"
)

print("[4 DONE] Saved confusion matrix")


print("\n[5] Generating accuracy curve...")

thresholds = np.arange(
    0.1,
    1.0,
    0.1
)

accuracies = []
recalls = []

for t in thresholds:

    temp_preds = []

    for conf, pred in zip(
        df[conf_col],
        df["binary_pred"]
    ):

        if conf >= t:
            temp_preds.append(pred)
        else:
            temp_preds.append("safe")

    acc = accuracy_score(
        df["binary_true"],
        temp_preds
    )

    rec = recall_score(
        df["binary_true"],
        temp_preds,
        pos_label="unsafe",
        zero_division=0
    )

    accuracies.append(acc)
    recalls.append(rec)


plt.figure(figsize=(8,5))

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

plt.grid(True)

plt.savefig(
    "results/accuracy_strictness_curve.png"
)

print("[5 DONE] Saved strictness curve")

print("\n[6] Category recall...")

if "category" in df.columns:

    categories = df["category"].unique()

    rows = []

    for cat in categories:

        sub = df[
            df["category"] == cat
        ]

        cat_recall = recall_score(
            sub["binary_true"],
            sub["binary_pred"],
            pos_label="unsafe",
            zero_division=0
        )

        rows.append({
            "category": cat,
            "recall": round(cat_recall, 4)
        })

    recall_df = pd.DataFrame(rows)

    print(recall_df)

    recall_df.to_csv(
        "results/category_recall.csv",
        index=False
    )

    print(
        "[6 DONE] Saved category recall"
    )


if "latency_ms" in df.columns:

    print("\n===== LATENCY =====")

    print(
        f"Average latency: "
        f"{df['latency_ms'].mean():.2f} ms"
    )

    print(
        f"P95 latency: "
        f"{df['latency_ms'].quantile(0.95):.2f} ms"
    )

print("\n===== EVERYTHING FINISHED =====")