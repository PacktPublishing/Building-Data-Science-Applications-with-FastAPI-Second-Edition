import os

import joblib
from sklearn.pipeline import Pipeline

# Load the model
model_file = os.path.join(os.path.dirname(__file__), "newsgroups_model.joblib")
loaded_model: tuple[Pipeline, list[str]] = joblib.load(model_file)
model, targets = loaded_model

# Run a prediction
p = model.predict(["computer cpu memory ram"])
print(targets[p[0]])
