import os
import json
import logging
import joblib
import pandas as pd
import numpy as np
from config import config

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# Machine Learning Classification Candidates
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

# Configure robust production-grade logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_and_evaluate_models():
    """Trains multiple classifiers using cross-validation, isolates performance, and exports artifacts."""
    dataset_path = os.path.join(config.DATASET_DIR, 'dataset.csv')
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(
            "The training source 'dataset.csv' was not found. Please run generate_dataset.py first."
        )
        
    # Data Ingestion
    df = pd.read_csv(dataset_path)
    
    # Feature-Target Isolation
    X = df.drop(columns=['Productivity_Level'])
    y = df['Productivity_Level']
    
    # Define an optimized robust 5-Fold validation pipeline split matrix
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Upgraded Model Configurations with hyperparameter regularizations
    models = {
        'Logistic Regression': LogisticRegression(max_iter=2000, C=1.0, solver='lbfgs', random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=6, min_samples_split=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_leaf=2, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=9, weights='distance', metric='euclidean')
    }
    
    performance_metrics = {}
    best_overall_score = 0.0
    best_model_name = None
    best_model_instance = None
    final_scaler_instance = None
    
    logging.info("Initializing Cross-Validation Engine...")
    print("\n======================= STRATIFIED CROSS-VALIDATION REPORT =======================")
    
    for name, model in models.items():
        fold_accuracies = []
        fold_precisions = []
        fold_recalls = []
        fold_f1_scores = []
        accumulated_confusion_matrix = np.zeros((3, 3), dtype=int)
        
        # Execute Cross-Validation Loop
        for train_idx, test_idx in skf.split(X, y):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            # Feature Scaling isolated per fold split to eliminate data leakage risks
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train and predict
            model.fit(X_train_scaled, y_train)
            predictions = model.predict(X_test_scaled)
            
            # Metrics aggregation
            acc = accuracy_score(y_test, predictions)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, predictions, average='macro', zero_division=0)
            matrix = confusion_matrix(y_test, predictions, labels=['Low', 'Medium', 'High'])
            
            fold_accuracies.append(acc)
            fold_precisions.append(prec)
            fold_recalls.append(rec)
            fold_f1_scores.append(f1)
            accumulated_confusion_matrix += matrix
            
        # Calculate mean performance properties across splits
        mean_accuracy = float(np.mean(fold_accuracies))
        mean_precision = float(np.mean(fold_precisions))
        mean_recall = float(np.mean(fold_recalls))
        mean_f1 = float(np.mean(fold_f1_scores))
        
        performance_metrics[name] = {
            'accuracy': mean_accuracy,
            'precision': mean_precision,
            'recall': mean_recall,
            'f1_score': mean_f1,
            'confusion_matrix': accumulated_confusion_matrix.tolist()
        }
        
        print(f"| Model: {name:<20} | CV Acc: {mean_accuracy:.4f} | Prec: {mean_precision:.4f} | F1: {mean_f1:.4f} |")
        
        # Keep track of the top performing strategy variant
        if mean_accuracy > best_overall_score:
            best_overall_score = mean_accuracy
            best_model_name = name
            best_model_instance = model

    print("==================================================================================\n")
    logging.info("Promoting architectural deployment candidate...")
    logging.info("Winner strategy: %s with mean performance: %s", best_model_name, f"{best_overall_score:.4f}")
    
    # Execute a final structural fitting across the complete available data vector space
    final_scaler = StandardScaler()
    X_full_scaled = final_scaler.fit_transform(X)
    best_model_instance.fit(X_full_scaled, y)
    
    # Serialize optimal operational artifacts safely down to target locations
    joblib.dump(best_model_instance, os.path.join(config.MODEL_DIR, 'best_model.pkl'))
    joblib.dump(final_scaler, os.path.join(config.MODEL_DIR, 'scaler.pkl'))
    
    metadata = {
        'winning_model': best_model_name,
        'metrics': performance_metrics
    }
    
    with open(os.path.join(config.MODEL_DIR, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    logging.info("[SUCCESS] Pipeline model artifacts successfully exported to /models/")

if __name__ == '__main__':
    train_and_evaluate_models()