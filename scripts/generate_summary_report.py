import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

# Resolve paths: prefer .env, fall back to relative project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
DATA_DIR = os.environ.get('DATA_FOLDER_PATH', os.path.join(PROJECT_ROOT, 'data'))
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

# Set style
sns.set_theme(style="whitegrid")

# Load data
df_results = pd.read_csv(os.path.join(DATA_DIR, 'sentiment_test_results.csv'))
df_cm = pd.read_csv(os.path.join(DATA_DIR, 'sentiment_confusion_matrix.csv'))

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Sentiment Analysis Performance Summary', fontsize=20)

# 1. Accuracy by Sentiment
acc_by_sent = df_results.groupby('actual_sentiment')['is_correct'].mean().sort_values()
sns.barplot(x=acc_by_sent.index, y=acc_by_sent.values, ax=axes[0, 0], hue=acc_by_sent.index, palette='viridis', legend=False)
axes[0, 0].set_title('Accuracy by Actual Sentiment')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_ylim(0, 1)

# 2. Accuracy by Platform
acc_by_platform = df_results.groupby('Platform')['is_correct'].mean().sort_values()
sns.barplot(x=acc_by_platform.index, y=acc_by_platform.values, ax=axes[0, 1], hue=acc_by_platform.index, palette='magma', legend=False)
axes[0, 1].set_title('Accuracy by Platform')
axes[0, 1].set_ylabel('Accuracy')
axes[0, 1].set_ylim(0, 1)
plt.setp(axes[0, 1].get_xticklabels(), rotation=45)

# 3. Confusion Matrix Heatmap
cm_pivot = df_cm.pivot(index='actual_sentiment', columns='predicted_sentiment', values='count').fillna(0)
sns.heatmap(cm_pivot, annot=True, fmt='.0f', cmap='Blues', ax=axes[1, 0])
axes[1, 0].set_title('Confusion Matrix')

# 4. Total Predictions by Sentiment
sent_counts = df_results['actual_sentiment'].value_counts()
axes[1, 1].pie(sent_counts, labels=sent_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
axes[1, 1].set_title('Distribution of Actual Sentiments')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
output_path = os.path.join(REPORTS_DIR, 'sentiment_analysis_summary.png')
plt.savefig(output_path)
print(f"Summary report saved to {os.path.abspath(output_path)}")
