"""
Opens a Power BI .pbip report after injecting DATA_FOLDER_PATH from .env
into the DataFolderPath.tmdl parameter files.

Usage:
    python scripts/open_report.py sentiment   # opens sentiment_toy_data
    python scripts/open_report.py iris        # opens iris_toy_data
    python scripts/open_report.py             # opens both
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

DATA_FOLDER_PATH = os.environ.get('DATA_FOLDER_PATH')
if not DATA_FOLDER_PATH:
    print("ERROR: DATA_FOLDER_PATH is not set in .env")
    print("Copy .env.example to .env and set the path to your data folder.")
    sys.exit(1)

TMDL_TEMPLATE = 'expression DataFolderPath = "{path}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n\tlineageTag: {tag}\n\n\tannotation PBI_NavigationStepName = Navigation\n\n\tannotation PBI_ResultType = Text\n'

REPORTS = {
    'sentiment': {
        'tmdl': os.path.join(PROJECT_ROOT, 'reports', 'sentiment_toy_data',
                             'sentiment_toy_data.SemanticModel', 'definition',
                             'expressions.tmdl'),
        'pbip': os.path.join(PROJECT_ROOT, 'reports', 'sentiment_toy_data',
                             'sentiment_toy_data.pbip'),
        'tag': 'f1a2b3c4-d5e6-f7a8-b9c0-e1e2f3a4b500',
    },
    'iris': {
        'tmdl': os.path.join(PROJECT_ROOT, 'reports', 'iris_toy_data',
                             'iris_toy_data.SemanticModel', 'definition',
                             'expressions.tmdl'),
        'pbip': os.path.join(PROJECT_ROOT, 'reports', 'iris_toy_data',
                             'iris_toy_data.pbip'),
        'tag': 'f1a2b3c4-d5e6-f7a8-b9c0-e1e2f3a4b501',
    },
}


def inject_and_open(name):
    report = REPORTS[name]

    # Write the parameter file with the path from .env
    content = TMDL_TEMPLATE.format(path=DATA_FOLDER_PATH, tag=report['tag'])
    with open(report['tmdl'], 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{name}] Wrote DataFolderPath = {DATA_FOLDER_PATH}")

    # Open the .pbip file with the default handler (Power BI Desktop)
    print(f"[{name}] Opening {report['pbip']}")
    os.startfile(report['pbip'])


if __name__ == '__main__':
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(REPORTS.keys())

    for target in targets:
        if target not in REPORTS:
            print(f"Unknown report: {target}. Choose from: {', '.join(REPORTS.keys())}")
            sys.exit(1)
        inject_and_open(target)
