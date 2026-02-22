# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project evaluates the accuracy of AIML Taxonomy Prediction models by comparing predicted taxonomy values against actual case values. It consists of:

1. **SQL queries** that extract prediction data from the COSMIC Data Hub (Azure SQL)
2. **Power BI reports** (`.pbix` files) for visualizing prediction accuracy
3. **Jupyter notebooks** for data exploration and ML evaluation
4. **DAX measures** for calculating macro-averaged precision, recall, and F1 scores

## Data Architecture

### Source Database
- **Server**: cosmicdatahubprod.database.windows.net
- **Database**: CosmicDataHub
- **Authentication**: Azure Entra ID (DefaultAzureCredential)

### Key Tables
- `eh_cos_taxonomypredictionlog` - Stores ML model prediction responses (JSON)
- `eh_email` - Email metadata linked to cases
- `eh_queue` - Queue/mailbox configuration
- `eh_cos_taxonomypredictionconfig` - Prediction configuration settings
- `Hub.vw_Incident` - Case/incident view with actual taxonomy values

### Prediction Scenarios
Two prediction scenarios exist with different JSON response structures:
- **"Email To Case"**: `$.results[0].<Field>.value` and `$.results[0].<Field>.prob`
- **"New Case - Update taxonomy"**: `$.result.classification.<field>`

### Taxonomy Fields Evaluated
- CaseType, CaseSubType, CaseReason, CaseSubReason, Program, SubmitterCountry

## Working with the SQL Queries

The main query (`AIML Taxonomy Prediction.sql`) uses temp tables `#TaxonomyPredictions` and `#EmailRecipients`. When modifying:
- Apply date filters early in CTEs before computing ROW_NUMBER to improve performance
- Use `ROW_NUMBER() OVER (PARTITION BY CaseId ORDER BY createdon ASC)` to get first prediction per case
- Check `ISJSON(cos_response) = 1` before parsing JSON fields

## Python Database Connection

Connect using pyodbc with Azure Entra ID token authentication:
```python
from azure.identity import DefaultAzureCredential
import pyodbc, struct

credential = DefaultAzureCredential()
token = credential.get_token("https://database.windows.net/.default")
token_bytes = token.token.encode("UTF-16-LE")
token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)

conn = pyodbc.connect(connection_string, attrs_before={1256: token_struct})
```

Requires: `ODBC Driver 18 for SQL Server`

## DAX Measures Structure

The DAX measures in `DAX_Macro_Measures.txt` follow a consistent pattern for each taxonomy field:
- Macro Precision: Average of per-class TP/(TP+FP)
- Macro Recall: Average of per-class TP/(TP+FN)
- Macro F1 Score: Harmonic mean of precision and recall

All measures return BLANK() when filtered to no data (HasData check pattern).
