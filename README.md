# ML Evaluation Power BI

This project evaluates the accuracy of ML classification models and visualizes results in Power BI.

## Project Structure

```
ml-eval-powerbi/
├── data/                   # Datasets and model output CSVs
│   ├── sentimentdataset.csv
│   ├── iris_test_results.csv
│   ├── sentiment_test_results.csv
│   ├── sentiment_confusion_matrix.csv
│   ├── sentiment_f1_by_day.csv
│   ├── sentiment_f1_by_week.csv
│   └── sentiment_f1_by_month.csv
├── notebooks/              # Jupyter notebooks for exploration
│   ├── iris_toy_dataset.ipynb
│   └── sentiment_analysis.ipynb
├── scripts/                # Python scripts
│   ├── train_3class_model.py
│   ├── create_powerbi_report.py
│   ├── generate_html_report.py
│   └── generate_summary_report.py
├── reports/                # Generated reports and Power BI files
│   └── iris_toy_data.pbix
└── medium_mcp_server/      # MCP server for Medium API integration
```

## Metrics

The project calculates macro-averaged precision, recall, and F1 scores for multi-class classification evaluation.
