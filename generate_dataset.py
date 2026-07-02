import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
from config import config

def generate_synthetic_data(num_records=500, random_seed=42):
    """Generates a realistic synthetic dataset for student productivity modeling."""
    np.random.seed(random_seed)
    
    # Generate independent lifestyle features
    sleep_hours = np.random.uniform(4.0, 9.5, num_records)
    study_hours = np.random.uniform(1.0, 10.0, num_records)
    stress_level = np.random.randint(1, 11, num_records)  # 1 (Low) to 10 (High)
    mood = np.random.randint(1, 4, num_records)            # 1: Low, 2: Neutral, 3: High
    break_count = np.random.randint(0, 7, num_records)
    
    data = pd.DataFrame({
        'Sleep_Hours': np.round(sleep_hours, 1),
        'Study_Hours': np.round(study_hours, 1),
        'Stress_Level': stress_level,
        'Mood': mood,
        'Break_Count': break_count
    })
    
    # Mathematical heuristic matrix for assigning realistic productivity targets
    # Base scoring formula
    score = (
        (data['Study_Hours'] * 3.5) + 
        (data['Sleep_Hours'] * 2.0) - 
        (data['Stress_Level'] * 2.5) + 
        (data['Mood'] * 4.0) + 
        (data['Break_Count'] * 1.5)
    )
    
    # Inject deterministic noise to replicate natural variance
    noise = np.random.normal(0, 3.5, num_records)
    final_score = score + noise
    
    # Assign target labels based on quantile thresholds
    low_thresh = np.percentile(final_score, 33)
    high_thresh = np.percentile(final_score, 66)
    
    productivity_level = []
    for s in final_score:
        if s <= low_thresh:
            productivity_level.append('Low')
        elif s <= high_thresh:
            productivity_level.append('Medium')
        else:
            productivity_level.append('High')
            
    data['Productivity_Level'] = productivity_level
    
    # Save target file
    output_path = os.path.join(config.DATASET_DIR, 'dataset.csv')
    data.to_csv(output_path, index=False)
    print(f"[SUCCESS] Synthetic dataset generated with {num_records} rows at: {output_path}")
    return data

def run_exploratory_data_analysis(df):
    """Generates and saves professional analytical graphs for the EDA dashboard."""
    sns.set_theme(style="darkgrid")
    palette = {'High': '#2ecc71', 'Medium': '#f1c40f', 'Low': '#e74c3c'}
    
    # 1. Countplot of Target Variable
    plt.figure(figsize=(6, 4))
    sns.countplot(x='Productivity_Level', data=df, order=['Low', 'Medium', 'High'], palette=palette)
    plt.title('Distribution of Productivity Levels', fontsize=12, fontweight='bold')
    plt.xlabel('Productivity Category')
    plt.ylabel('Student Count')
    plt.tight_layout()
    plt.savefig(os.path.join(config.PLOTS_DIR, 'countplot.png'), dpi=150)
    plt.close()
    
    # 2. Histogram of Study Hours vs Sleep Hours
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x='Study_Hours', kde=True, color='#3498db', label='Study Hours', alpha=0.6)
    sns.histplot(data=df, x='Sleep_Hours', kde=True, color='#9b59b6', label='Sleep Hours', alpha=0.4)
    plt.title('Distribution of Study and Sleep Durations', fontsize=12, fontweight='bold')
    plt.xlabel('Hours')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(config.PLOTS_DIR, 'histogram.png'), dpi=150)
    plt.close()

    # 3. Correlation Matrix Heatmap
    plt.figure(figsize=(6, 5))
    numeric_df = df.drop(columns=['Productivity_Level'])
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='Blues', fmt=".2f", linewidths=0.5, cbar=True)
    plt.title('Feature Correlation Matrix Heatmap', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(config.PLOTS_DIR, 'heatmap.png'), dpi=150)
    plt.close()

    # 4. Boxplot of Stress Levels Across Productivity Classes
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='Productivity_Level', y='Stress_Level', data=df, order=['Low', 'Medium', 'High'], palette=palette)
    plt.title('Stress Levels across Productivity Cohorts', fontsize=12, fontweight='bold')
    plt.xlabel('Productivity Level')
    plt.ylabel('Stress Range (1-10)')
    plt.tight_layout()
    plt.savefig(os.path.join(config.PLOTS_DIR, 'boxplot.png'), dpi=150)
    plt.close()

    # 5. Pairplot Segmented by Class Target
    plt.figure(figsize=(10, 8))
    pair_plot = sns.pairplot(df, hue='Productivity_Level', hue_order=['Low', 'Medium', 'High'], palette=palette, diag_kind='kde')
    pair_plot.fig.suptitle('Multivariate Feature Pairplot', y=1.02, fontsize=14, fontweight='bold')
    pair_plot.savefig(os.path.join(config.PLOTS_DIR, 'pairplot.png'), dpi=120)
    plt.close()
    
    print(f"[SUCCESS] All analytical charts saved down to: {config.PLOTS_DIR}")

if __name__ == '__main__':
    dataframe = generate_synthetic_data()
    run_exploratory_data_analysis(dataframe)