import os

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart_study_secret_key_2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE = os.path.join(BASE_DIR, 'database.db')
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    PLOTS_DIR = os.path.join(BASE_DIR, 'static', 'plots')
    
    # Ensure directories exist upon configuration import
    for directory in [DATASET_DIR, MODEL_DIR, PLOTS_DIR]:
        os.makedirs(directory, exist_ok=True)

config = Config()