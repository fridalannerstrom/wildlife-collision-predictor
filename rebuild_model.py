import pandas as pd
import lzma
import cloudpickle
from sklearn.ensemble import RandomForestClassifier

# 1. Ladda datan
df = pd.read_csv("data/cleaned_data.csv")

# 2. Ta bort irrelevanta kolumner
drop_cols = ["Animal_ID", "Collision_ID", "Date", "Time"]
df = df.drop(columns=drop_cols, errors="ignore")

# 3. Ta bort rader med saknade värden
df = df.dropna()

# 4. Separera X och y
X = df.drop(columns=["Animal_Outcome"])
y = df["Animal_Outcome"]

# 5. One-hot encoding av kategoriska kolumner
X = pd.get_dummies(X)

# 6. Träna modellen
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# 7. Spara modellen komprimerad
with lzma.open("model/model.pkl.xz", "wb") as f:
    cloudpickle.dump(model, f)

print("✅ Modellen har tränats och sparats som model.pkl.xz!")
