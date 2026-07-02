# Smart Study Companion AI Engine 🚀

An advanced machine learning predictive optimization web application designed to evaluate, visualize, and classify student lifestyle and study habits into explicit real-time productivity insights.

## Core Structural Folders
- `generate_dataset.py`: Generates 500 records of synthetic student logs and outputs automated EDA charts to `/static/plots/`.
- `train.py`: Scales data vectors, scores 4 distinct pipeline classifiers (Logistic Regression, Decision Tree, Random Forest, KNN), and saves the best model setup to `/models/`.
- `predict.py`: Houses the operational study predictor class inference engine.
- `app.py`: Serves as the web routing engine, hosting the RESTful SQLite analytics framework layers.

## Step-by-Step Local Deployment Sequence

Ensure you are located inside the root project folder `SmartStudyCompanion/` within your VS Code terminal.

### 1. Initialize Virtual Environment Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate

pip install -r requirements.txt