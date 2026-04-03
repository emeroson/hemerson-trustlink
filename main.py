import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve
)

# =========================
# 📥 1. CHARGEMENT DATA
# =========================
print("📥 Chargement des données...")

data = pd.read_csv(
    "creditcard.csv",
    sep=";",  # ⚠️ important
    engine="python",
    on_bad_lines="skip"
)

# Nettoyage noms colonnes
data.columns = data.columns.str.strip()

print("✅ Données chargées")
print("Colonnes :", data.columns)

# =========================
# 🧹 2. NETTOYAGE
# =========================
print("🧹 Nettoyage...")

data = data.apply(pd.to_numeric, errors='coerce')
data = data.dropna()

print("✅ Nettoyage terminé")

# =========================
# 📊 3. FEATURES / TARGET
# =========================
if "Class" not in data.columns:
    raise Exception("❌ La colonne 'Class' est introuvable → problème CSV")

X = data.drop("Class", axis=1)
y = data["Class"]

print("Fraudes :", sum(y == 1))
print("Normales :", sum(y == 0))

# =========================
# ⚖️ 4. SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================
# 📏 5. SCALING
# =========================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# 🤖 6. MODÈLE
# =========================
model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

print("🚀 Entraînement du modèle...")
model.fit(X_train, y_train)
print("✅ Modèle entraîné")

# =========================
# 🎯 7. PROBABILITÉS
# =========================
y_proba = model.predict_proba(X_test)[:, 1]

# =========================
# 🔥 8. SEUIL OPTIMAL
# =========================
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)

f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
best_index = np.argmax(f1_scores)
best_threshold = thresholds[best_index]

print(f"🎯 Meilleur seuil : {best_threshold:.4f}")

# =========================
# 🎯 9. PRÉDICTION
# =========================
y_pred = (y_proba > best_threshold).astype(int)

# =========================
# 📊 10. ÉVALUATION
# =========================
print("\n📊 Accuracy :", accuracy_score(y_test, y_pred))

print("\n📊 Rapport de classification :")
print(classification_report(y_test, y_pred))

print("\n📊 Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# =========================
# 🔥 11. ROC AUC
# =========================
auc = roc_auc_score(y_test, y_proba)
print("\n🔥 ROC AUC :", auc)

# =========================
# 📈 12. TAUX FRAUDE
# =========================
fraud_rate = (sum(y_pred) / len(y_pred)) * 100
print(f"\n🚨 Taux de fraude détecté : {fraud_rate:.2f}%")

# =========================
# 💾 13. SAUVEGARDE
# =========================
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\n💾 Modèle sauvegardé (model.pkl, scaler.pkl)")