# ML Evaluation Power BI

Evaluate ML classification models and visualize results using Power BI PBIP (Power BI Project) format. The project demonstrates how to calculate and display standard classification metrics — accuracy, precision, recall, F1 score, and confusion matrices — using both Python visuals and native DAX measures.

## Project Structure

```
ml-eval-powerbi/
├── .env.example                           # Template — copy to .env and set DATA_FOLDER_PATH
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
│   ├── open_report.py                   # Inject data path from .env and open Power BI
│   ├── train_3class_model.py            # Train a 3-class sentiment classifier
│   ├── create_powerbi_report.py         # Generate Power BI report programmatically
│   ├── generate_html_report.py          # Generate standalone HTML report
│   └── generate_summary_report.py       # Generate summary statistics
├── reports/
│   ├── iris_toy_data/                   # Iris classification report
│   │   ├── iris_toy_data.pbip           # Power BI project file
│   │   ├── iris_toy_data.pbix           # Legacy Power BI file
│   │   ├── iris_toy_data.Report/        # Report definition (2 pages)
│   │   └── iris_toy_data.SemanticModel/ # Semantic model (TMDL)
│   └── sentiment_toy_data/              # Sentiment classification report
│       ├── sentiment_toy_data.pbip      # Power BI project file
│       ├── sentiment_toy_data.Report/   # Report definition (3 pages)
│       └── sentiment_toy_data.SemanticModel/ # Semantic model (TMDL)
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
| `Accuracy` | Correct / Total (displayed as %) |
| `True Positives` | Per-class TP count |
| `False Positives` | Per-class FP count |
| `False Negatives` | Per-class FN count |
| `Macro Precision` | Average of per-class TP/(TP+FP) (displayed as %) |
| `Macro Recall` | Average of per-class TP/(TP+FN) (displayed as %) |
| `Macro F1 Score` | Harmonic mean of macro precision and recall (displayed as %) |
| `Class Precision` | Per-class precision (displayed as %) |
| `Class Recall` | Per-class recall (displayed as %) |
| `Class F1 Score` | Per-class F1 (displayed as %) |
| `CM Count` | Confusion matrix cell count |
| `Avg Confidence` | Mean confidence score (sentiment report only) |

## Prerequisites

- **Power BI Desktop** (December 2025 or later) with PBIP format enabled
- **Python 3.9+** (for Python visuals and notebooks)
- Python packages: `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `numpy`, `python-dotenv`

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
pip install pandas matplotlib seaborn scikit-learn numpy jupyter python-dotenv
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

### 4. Configure the Data Source Path

The Power BI reports load CSV files from a `DataFolderPath` parameter. A launcher script reads the path from `.env` and injects it into the report before opening Power BI Desktop.

**One-time setup:**

```bash
copy .env.example .env
```

Edit `.env` and set the absolute path to your `data/` folder:

```
DATA_FOLDER_PATH=C:\Users\<you>\Downloads\ml-eval-powerbi\data
```

### 5. Open the Power BI Reports

Use the launcher script — it writes `DATA_FOLDER_PATH` from `.env` into the report's `expressions.tmdl` and then opens Power BI Desktop:

```bash
python scripts/open_report.py sentiment   # open sentiment report
python scripts/open_report.py iris        # open iris report
python scripts/open_report.py             # open both
```

> **Note:** Do not open `.pbip` files directly by double-clicking. The launcher script must run first to set the correct data path for your machine.

Click **Refresh** in Power BI Desktop after the report opens to load the data.

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
