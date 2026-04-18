# ML Evaluation Power BI

Evaluate ML classification models and visualize results using Power BI PBIP (Power BI Project) format. The project demonstrates how to calculate and display standard classification metrics — accuracy, precision, recall, F1 score, and confusion matrices — using both Python visuals and native DAX measures.

## Project Structure

```
ml-eval-powerbi/
├── data/
│   ├── iris_test_results.csv            # Iris 3-class classification results (150 rows)
│   ├── sentiment_test_results.csv       # Sentiment 3-class classification results (50 rows)
│   ├── sentimentdataset.csv             # Raw sentiment dataset
│   ├── sentiment_confusion_matrix.csv   # Pre-computed confusion matrix
│   └── sentiment_f1_by_*.csv            # Pre-computed F1 scores by time period
├── notebooks/
│   ├── iris_toy_dataset.ipynb           # Iris model training and evaluation
│   └── sentiment_analysis.ipynb         # Sentiment model training and evaluation
├── scripts/
│   ├── train_3class_model.py            # Train a 3-class sentiment classifier
│   ├── create_powerbi_report.py         # Generate Power BI report programmatically
│   ├── generate_html_report.py          # Generate standalone HTML report
│   └── generate_summary_report.py       # Generate summary statistics
├── reports/
│   ├── iris_toy_data.pbip               # Iris classification Power BI project
│   ├── iris_toy_data.pbix               # Iris classification Power BI file (legacy)
│   ├── iris_toy_data.Report/            # Iris report definition (2 pages)
│   ├── iris_toy_data.SemanticModel/     # Iris semantic model (TMDL)
│   ├── sentiment_toy_data.pbip          # Sentiment classification Power BI project
│   ├── sentiment_toy_data.Report/       # Sentiment report definition (3 pages)
│   └── sentiment_toy_data.SemanticModel/# Sentiment semantic model (TMDL)
└── medium_mcp_server/                   # MCP server for Medium API integration
```

## Power BI Reports

### Iris Classification Report (`iris_toy_data.pbip`)

Two-page report for evaluating an Iris species classifier:

| Page | Visuals |
|------|---------|
| **Python Perf Metrics** | Bar chart (per-class metrics), confusion matrix heatmap, class-wise performance matrix — all rendered via Python/matplotlib |
| **DAX Metrics** | KPI cards (accuracy, macro precision/recall/F1), class-wise metrics table, confusion matrix — all computed in DAX |

### Sentiment Classification Report (`sentiment_toy_data.pbip`)

Three-page report for evaluating a sentiment classifier (positive/negative/neutral):

| Page | Visuals |
|------|---------|
| **Python Perf Metrics** | Bar chart, confusion matrix heatmap, class-wise performance matrix — Python/matplotlib |
| **DAX Metrics** | KPI cards (accuracy, macro precision/recall/F1, avg confidence), class-wise metrics table, confusion matrix — native DAX |
| **Metrics Over Time** | Classification metrics trend (accuracy, macro P/R/F1) and confidence/prediction counts over time — line charts using Date Hierarchy |

## DAX Measures

Both reports use the same pattern of DAX measures:

| Measure | Description |
|---------|-------------|
| `Total Predictions` | Total row count |
| `Correct Predictions` | Rows where actual = predicted |
| `Accuracy` | Correct / Total |
| `True Positives` | Per-class TP count |
| `False Positives` | Per-class FP count |
| `False Negatives` | Per-class FN count |
| `Macro Precision` | Average of per-class TP/(TP+FP) |
| `Macro Recall` | Average of per-class TP/(TP+FN) |
| `Macro F1 Score` | Harmonic mean of macro precision and recall |
| `Class Precision` | Per-class precision (for use in row context) |
| `Class Recall` | Per-class recall (for use in row context) |
| `Class F1 Score` | Per-class F1 (for use in row context) |
| `CM Count` | Confusion matrix cell count |
| `Avg Confidence` | Mean confidence score (sentiment report only) |

## Prerequisites

- **Power BI Desktop** (December 2025 or later) with PBIP format enabled
- **Python 3.9+** (for Python visuals and notebooks)
- Python packages: `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `numpy`

### Enable PBIP Format in Power BI Desktop

1. Open Power BI Desktop
2. Go to **File > Options and settings > Options**
3. Under **Preview features**, enable:
   - **Power BI Project (.pbip) save format**
   - **Store semantic model in TMDL format**
4. Restart Power BI Desktop

## Steps to Reproduce

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/ml-eval-powerbi.git
cd ml-eval-powerbi
```

### 2. Install Python Dependencies

```bash
pip install pandas matplotlib seaborn scikit-learn numpy jupyter
```

### 3. Generate the Datasets (Optional)

The datasets are already included in `data/`. To regenerate:

**Iris dataset:**
```bash
jupyter notebook notebooks/iris_toy_dataset.ipynb
# Run all cells — outputs data/iris_test_results.csv
```

**Sentiment dataset:**
```bash
jupyter notebook notebooks/sentiment_analysis.ipynb
# Run all cells — outputs data/sentiment_test_results.csv
```

Or train the sentiment model directly:
```bash
python scripts/train_3class_model.py
```

### 4. Open the Power BI Reports

**Option A — Open the PBIP project (recommended):**

1. Open Power BI Desktop
2. Go to **File > Open report > Browse this device**
3. Navigate to `reports/` and open either:
   - `iris_toy_data.pbip` (Iris classification)
   - `sentiment_toy_data.pbip` (Sentiment classification)
4. When prompted, update the data source path:
   - Go to **Transform Data > Data Source Settings**
   - Update the CSV file path to point to the `data/` folder on your machine
5. Click **Refresh** to load the data

**Option B — Open the legacy PBIX file:**

1. Open `reports/iris_toy_data.pbix` directly in Power BI Desktop
2. Update the data source path as described above

### 5. Update the Data Source Path

The PBIP semantic model references a local CSV path. To update it:

1. Open the `.tmdl` file for the table in:
   ```
   reports/<report>.SemanticModel/definition/tables/<table>.tmdl
   ```
2. Find the `partition` section and update the `File.Contents()` path:
   ```
   File.Contents("C:\<your-path>\ml-eval-powerbi\data\<dataset>.csv")
   ```
3. Save and reopen the report in Power BI Desktop

### 6. Verify the Reports

After loading, verify each page:

- **Python Perf Metrics**: Should show matplotlib-rendered bar charts, confusion matrix heatmap, and class-wise performance matrix
- **DAX Metrics**: Should show KPI cards with accuracy/precision/recall/F1 values, a class-wise metrics table, and a confusion matrix
- **Metrics Over Time** (sentiment only): Should show line charts tracking metrics over the date range

## Datasets

### Iris Test Results (`iris_test_results.csv`)

| Column | Description |
|--------|-------------|
| `sepal_length`, `sepal_width`, `petal_length`, `petal_width` | Feature values |
| `actual_species` | Ground truth label (setosa, versicolor, virginica) |
| `predicted_species` | Model prediction |
| `confidence_score` | Prediction confidence (0-1) |

### Sentiment Test Results (`sentiment_test_results.csv`)

| Column | Description |
|--------|-------------|
| `text` | Input text |
| `actual_sentiment` | Ground truth label (positive, negative, neutral) |
| `predicted_sentiment` | Model prediction |
| `confidence_score` | Prediction confidence (0-1) |
| `prediction_date` | Timestamp of prediction (Jan-Apr 2026) |

## Metrics Explained

- **Accuracy**: Proportion of correct predictions across all classes
- **Macro Precision**: Unweighted average of per-class precision — treats all classes equally regardless of support
- **Macro Recall**: Unweighted average of per-class recall
- **Macro F1 Score**: Harmonic mean of macro precision and macro recall (not the average of per-class F1 scores)
- **Confusion Matrix**: Shows actual vs. predicted class counts; diagonal cells are correct predictions
