import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from dotenv import load_dotenv

# Resolve paths: prefer .env, fall back to relative project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
DATA_DIR = os.environ.get('DATA_FOLDER_PATH', os.path.join(PROJECT_ROOT, 'data'))
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

# Load data
df_results = pd.read_csv(os.path.join(DATA_DIR, 'sentiment_test_results.csv'))
df_month = pd.read_csv(os.path.join(DATA_DIR, 'sentiment_f1_by_month.csv'))
df_cm = pd.read_csv(os.path.join(DATA_DIR, 'sentiment_confusion_matrix.csv'))

# Calculate metrics
total_preds = len(df_results)
correct_preds = df_results['is_correct'].sum()
accuracy = correct_preds / total_preds

# Create a dashboard using Plotly
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Accuracy by Sentiment", "F1 Score Trend (Monthly)", "Confusion Matrix", "Accuracy by Platform"),
    vertical_spacing=0.15,
    specs=[[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "heatmap"}, {"type": "bar"}]]
)

# 1. Accuracy by Sentiment
acc_by_sent = df_results.groupby('actual_sentiment')['is_correct'].mean().reset_index()
fig.add_trace(
    go.Bar(x=acc_by_sent['actual_sentiment'], y=acc_by_sent['is_correct'], name="Accuracy"),
    row=1, col=1
)

# 2. F1 Score Trend
fig.add_trace(
    go.Scatter(x=df_month['Period'], y=df_month['F1_Score'], mode='lines+markers', name="F1 Score"),
    row=1, col=2
)

# 3. Confusion Matrix
# Pivot the confusion matrix if it's not already in a heatmap-friendly format
cm_pivot = df_cm.pivot(index='actual_sentiment', columns='predicted_sentiment', values='count')
fig.add_trace(
    go.Heatmap(z=cm_pivot.values, x=cm_pivot.columns, y=cm_pivot.index, colorscale='Blues', name="Confusion Matrix"),
    row=2, col=1
)

# 4. Accuracy by Platform
acc_by_platform = df_results.groupby('Platform')['is_correct'].mean().reset_index()
fig.add_trace(
    go.Bar(x=acc_by_platform['Platform'], y=acc_by_platform['is_correct'], name="Platform Accuracy"),
    row=2, col=2
)

fig.update_layout(height=800, width=1000, title_text=f"Sentiment Analysis Dashboard (Global Accuracy: {accuracy:.2%})", showlegend=False)

# Save to HTML
output_file = os.path.join(REPORTS_DIR, "sentiment_report_dashboard.html")
fig.write_html(output_file)
print(f"Dashboard created: {os.path.abspath(output_file)}")
