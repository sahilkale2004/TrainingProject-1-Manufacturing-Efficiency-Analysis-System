# 🏭 Manufacturing Efficiency Analysis System

This project is an end-to-end Machine Learning web application designed to predict the production efficiency of manufacturing processes using real-time sensor and process data. 

### ✨ Key Features
- **FastAPI Backend**: Provides a blazing-fast REST API to serve predictions using a trained deep-learning model (`PyTorch`).
- **Streamlit Frontend**: A dynamic, interactive dashboard where operators can input machine, material, and operational metrics to instantly visualize the predicted efficiency score.
- **End-to-End ML Pipeline**: From processing datasets (scaling and encoding) via `scikit-learn` to training Neural Networks and serving them in modern web architectures.

---

## Workflow

### 1. Training (Google Colab)
1. Open `training/train.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Upload `training/manufacturing_dataset.csv`.
3. Run all cells.
4. Download `efficiency_model.pth` and `preprocessor.pkl`.

### 2. Local Setup
1. Move the downloaded files to the `model/` directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start Backend: `python backend/main.py`.
4. Start Frontend: `streamlit run frontend/app.py`.


