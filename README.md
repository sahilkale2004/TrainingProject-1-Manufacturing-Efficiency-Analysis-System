# Manufacturing Efficiency Prediction

A machine learning system to predict manufacturing efficiency based on real-time sensor and process data.

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

### 3. Deployment
Same as Project 1, but using the specific commands for port 8001 and backend/main.py.
