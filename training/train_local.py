import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import joblib
import os

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Load data
df = pd.read_csv('training/manufacturing_dataset.csv')

# Preprocessing logic from train.ipynb
# Drop Timestamp if it exists
if 'Timestamp' in df.columns:
    df = df.drop('Timestamp', axis=1)

# Define Target and Features
target = 'Efficiency_Score'
X = df.drop(target, axis=1)
y = df[target].values

# Identify Numerical and Categorical columns
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing Pipeline
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# Save Preprocessor
joblib.dump(preprocessor, 'model/preprocessor.pkl')
print("Preprocessor saved to 'model/preprocessor.pkl'.")

# Define Pytorch Model
class EfficiencyNet(nn.Module):
    def __init__(self, input_size):
        super(EfficiencyNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)

input_dim = X_train_processed.shape[1]
model = EfficiencyNet(input_dim)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Convert to Tensors
X_train_t = torch.FloatTensor(X_train_processed)
y_train_t = torch.FloatTensor(y_train).view(-1, 1)

# Training Loop
epochs = 200
print(f"Starting training for {epochs} epochs...")
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 50 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}')

# Save the model
torch.save(model.state_dict(), 'model/efficiency_model.pth')
print("Model and preprocessor saved to 'model/' folder.")
