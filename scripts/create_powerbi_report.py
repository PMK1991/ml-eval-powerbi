"""
Power BI Report Setup Script
Run this to generate Power Query M code and DAX measures for manual import.
"""

import os
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
folder = os.environ.get('DATA_FOLDER_PATH', os.path.join(PROJECT_ROOT, 'data'))

print("=" * 60)
print("POWER BI MANUAL SETUP INSTRUCTIONS")
print("=" * 60)

print("""
STEP 1: Open Power BI Desktop

STEP 2: Get Data > Text/CSV
        Import these files from:
        {}

        Files to import:
        1. sentiment_test_results.csv
        2. sentiment_f1_by_day.csv
        3. sentiment_f1_by_week.csv
        4. sentiment_f1_by_month.csv
        5. sentiment_confusion_matrix.csv

STEP 3: After importing, go to Model view and add these DAX measures
        Right-click on 'sentiment_test_results' table > New measure

""".format(folder))

print("-" * 60)
print("DAX MEASURES (copy each one):")
print("-" * 60)

measures = [
    ("Total Predictions", "COUNTROWS('sentiment_test_results')"),
    ("Correct Predictions", "SUM('sentiment_test_results'[is_correct])"),
    ("Accuracy", "DIVIDE([Correct Predictions], [Total Predictions], 0)"),
    ("Macro F1 Score", """
VAR TotalClasses = DISTINCTCOUNT('sentiment_test_results'[actual_sentiment])
VAR CorrectByClass =
    SUMX(
        VALUES('sentiment_test_results'[actual_sentiment]),
        VAR CurrentClass = 'sentiment_test_results'[actual_sentiment]
        VAR TP = CALCULATE(
            COUNTROWS('sentiment_test_results'),
            'sentiment_test_results'[actual_sentiment] = CurrentClass,
            'sentiment_test_results'[predicted_sentiment] = CurrentClass
        )
        VAR FN = CALCULATE(
            COUNTROWS('sentiment_test_results'),
            'sentiment_test_results'[actual_sentiment] = CurrentClass,
            'sentiment_test_results'[predicted_sentiment] <> CurrentClass
        )
        VAR FP = CALCULATE(
            COUNTROWS('sentiment_test_results'),
            'sentiment_test_results'[actual_sentiment] <> CurrentClass,
            'sentiment_test_results'[predicted_sentiment] = CurrentClass
        )
        VAR Precision = DIVIDE(TP, TP + FP, 0)
        VAR Recall = DIVIDE(TP, TP + FN, 0)
        VAR F1 = DIVIDE(2 * Precision * Recall, Precision + Recall, 0)
        RETURN F1
    )
RETURN DIVIDE(CorrectByClass, TotalClasses, 0)
"""),
]

for name, expression in measures:
    print(f"\n{name} = {expression.strip()}")
    print()

print("-" * 60)
print("STEP 4: CREATE VISUALS")
print("-" * 60)
print("""
PAGE 1 - Overview:
- Card: Accuracy (format as %)
- Card: Total Predictions
- Card: Correct Predictions
- Card: Macro F1 Score (format as %)
- Bar Chart: actual_sentiment (Axis) vs Count of is_correct (Value)
- Line Chart (from f1_by_month): Period (Axis) vs F1_Score (Value)
- Line Chart (from f1_by_week): Period (Axis) vs F1_Score (Value)

PAGE 2 - Details:
- Matrix: actual_sentiment (Rows) vs predicted_sentiment (Columns) vs count (Values)
  [This creates the confusion matrix]
- Bar Chart: Platform (Axis) vs Accuracy (Value)
- Table: Text, actual_sentiment, predicted_sentiment, is_correct

STEP 5: Save as .pbix file
""")

print("=" * 60)
print("Script complete! Follow the instructions above.")
print("=" * 60)
