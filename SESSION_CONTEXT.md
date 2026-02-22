# Session Context - Social Media Sentiment Analysis
**Date**: February 12, 2026
**Project**: AIML Taxonomy Prediction - Sentiment Analysis Extension

---

## What Was Done

### 1. Dataset Acquisition
- Downloaded Kaggle dataset using API: `kaggle datasets download -d kashishparmar02/social-media-sentiments-analysis-dataset`
- File: `sentimentdataset.csv` (732 rows, 15 columns)
- Original dataset had 191 unique sentiment labels

### 2. Sentiment Categorization
Mapped 191 sentiments into 3 broad categories:
- **Positive** (461 samples): Joy, Excitement, Love, Happiness, etc.
- **Negative** (179 samples): Anger, Sadness, Fear, Anxiety, etc.
- **Neutral** (92 samples): Curiosity, Boredom, Contemplation, etc.

### 3. Model Training
- **Algorithm**: RandomForestClassifier (100 estimators)
- **Features**: TF-IDF vectorization (max 5000 features, unigrams + bigrams)
- **Split**: 80% train (585), 20% test (147)

### 4. Results
| Metric | Value |
|--------|-------|
| Accuracy | 76.87% |
| Macro F1 | 60.75% |

**Per-class performance:**
| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Positive | 75% | 99% | 85% |
| Negative | 85% | 47% | 61% |
| Neutral | 100% | 22% | 36% |

### 5. Files Created

#### Data Files
| File | Description |
|------|-------------|
| `sentimentdataset.csv` | Original Kaggle dataset |
| `sentiment_test_results.csv` | Test predictions with original & categorized sentiments |
| `sentiment_f1_by_day.csv` | F1 scores aggregated by day |
| `sentiment_f1_by_week.csv` | F1 scores aggregated by week |
| `sentiment_f1_by_month.csv` | F1 scores aggregated by month |
| `sentiment_confusion_matrix.csv` | 3x3 confusion matrix in long format |

#### Code Files
| File | Description |
|------|-------------|
| `sentiment_analysis.ipynb` | Main Jupyter notebook (updated for 3-class) |
| `train_3class_model.py` | Standalone Python script for training |
| `create_powerbi_report.py` | Instructions for Power BI manual setup |

#### Existing Project Files
| File | Description |
|------|-------------|
| `iris_toy_dataset.ipynb` | Reference notebook (Iris classification) |
| `iris_test_results.csv` | Reference output format |
| `AIML Taxonomy Prediction.sql` | Main SQL query for taxonomy predictions |
| `DAX_Macro_Measures.txt` | DAX measures for Power BI |

---

## What Was NOT Completed

### Power BI Integration
- PBIP (Power BI Project) format did not work
- Manual import instructions provided in `create_powerbi_report.py`
- **TODO**: Import CSVs into Power BI Desktop manually and create visuals

---

## Key Code References

### Sentiment Categorization Function
Located in `train_3class_model.py` (lines 10-70):
- `POSITIVE`, `NEGATIVE`, `NEUTRAL` lists define category mappings
- `categorize_sentiment()` function handles unmapped sentiments via keyword matching

### Model Training Pipeline
```python
# TF-IDF + RandomForest
tfidf = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
```

### F1 Calculation by Time Period
```python
def calc_f1(group):
    return f1_score(group['sentiment_label'], group['predicted_label'], average='macro', zero_division=0)

f1_by_day = test_df.groupby('Date').apply(calc_f1)
f1_by_week = test_df.groupby(['Year', 'Week']).apply(calc_f1)
f1_by_month = test_df.groupby(['Year', 'Month']).apply(calc_f1)
```

---

## To Resume Tomorrow

### Option 1: Re-run the model
```bash
cd C:\Users\praskulkarni\Downloads\aiml_taxonomy_prediction
python train_3class_model.py
```

### Option 2: Run the Jupyter notebook
Open `sentiment_analysis.ipynb` and run all cells.

### Option 3: Power BI Setup
1. Open Power BI Desktop
2. Get Data > Text/CSV
3. Import: `sentiment_test_results.csv`, `sentiment_f1_by_*.csv`
4. Add DAX measures from `create_powerbi_report.py`
5. Create visuals (cards, bar charts, line charts, matrix)

---

## Potential Improvements
1. **Class Imbalance**: Neutral class has low recall (22%) - consider SMOTE or class weights
2. **Feature Engineering**: Add sentiment lexicons, word embeddings
3. **Model Tuning**: Try other classifiers (XGBoost, SVM, Neural Networks)
4. **Cross-validation**: Use k-fold CV for more robust evaluation

---

## Environment
- Python 3.11
- Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn
- Kaggle CLI installed and configured
- Power BI Desktop available (PBIP feature not enabled)
