"""
Train sentiment classification model with 3 categories: Positive, Negative, Neutral
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv

# Resolve paths: prefer .env, fall back to relative project structure
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
DATA_DIR = os.environ.get('DATA_FOLDER_PATH', os.path.join(PROJECT_ROOT, 'data'))

# Sentiment mapping to 3 categories
POSITIVE = [
    'Positive', 'Joy', 'Excitement', 'Contentment', 'Gratitude', 'Happiness', 'Happy',
    'Love', 'Enthusiasm', 'Euphoria', 'Elation', 'Ecstasy', 'Admiration', 'Adoration',
    'Affection', 'Amazement', 'Amusement', 'Appreciation', 'Awe', 'Blessed', 'Calmness',
    'Captivation', 'Celebration', 'Charm', 'Compassion', 'Compassionate', 'Confidence',
    'Confident', 'Connection', 'Coziness', 'Creativity', 'Dazzle', 'Determination',
    'Empowerment', 'Enchantment', 'Energy', 'Engagement', 'Enjoyment', 'Exploration',
    'Freedom', 'Friendship', 'Fulfillment', 'Grandeur', 'Grateful', 'Harmony',
    'Heartwarming', 'Hope', 'Hopeful', 'Imagination', 'Inspiration', 'Inspired',
    'Intrigue', 'Kindness', 'Kind', 'Marvel', 'Mesmerizing', 'Mindfulness', 'Motivation',
    'Optimism', 'Overjoyed', 'Playful', 'Positivity', 'Pride', 'Proud', 'Radiance',
    'Rejuvenation', 'Relief', 'Resilience', 'Reverence', 'Romance', 'Satisfaction',
    'Serenity', 'Spark', 'Success', 'Surprise', 'Sympathy', 'Tenderness', 'Thrill',
    'Touched', 'Tranquility', 'Triumph', 'Vibrancy', 'Whimsy', 'Wonder', 'Wonderment',
    'Zest', 'Acceptance', 'Accomplishment', 'Adventure', 'Adrenaline', 'ArtisticBurst',
    'Breakthrough', 'Celestial Wonder', 'Colorful', 'Creative Inspiration', 'CulinaryOdyssey',
    'Culinary Adventure', 'DreamChaser', 'Elegance', 'FestiveJoy', 'Free-spirited',
    'Hypnotic', 'Iconic', 'Immersion', 'InnerJourney', 'Journey', 'Joy in Baking',
    'JoyfulReunion', 'Melodic', "Nature's Beauty", "Ocean's Freedom", 'PlayfulJoy',
    'Renewed Effort', 'Runway Creativity', 'Solace', 'Thrilling Journey', 'Winter Magic',
    'Whispers of the Past', 'Envisioning History', 'Arousal', 'Mischievous'
]

NEGATIVE = [
    'Negative', 'Anger', 'Anxiety', 'Fear', 'Fearful', 'Sadness', 'Sad', 'Despair',
    'Desperation', 'Devastated', 'Disappointment', 'Disappointed', 'Disgust', 'Frustration',
    'Frustrated', 'Grief', 'Hate', 'Heartache', 'Heartbreak', 'Helplessness', 'Isolation',
    'Jealousy', 'Jealous', 'Loneliness', 'Loss', 'Melancholy', 'Resentment', 'Shame',
    'Sorrow', 'Suffering', 'Betrayal', 'Bitter', 'Bitterness', 'Darkness', 'Desolation',
    'Embarrassed', 'EmotionalStorm', 'Envious', 'Envy', 'Exhaustion', 'Intimidation',
    'LostLove', 'Numbness', 'Overwhelmed', 'Pressure', 'Regret', 'Ruins', 'Bad',
    'Apprehensive', 'Dismissive'
]

NEUTRAL = [
    'Neutral', 'Ambivalence', 'Anticipation', 'Boredom', 'Confusion', 'Contemplation',
    'Curiosity', 'Indifference', 'Nostalgia', 'Pensive', 'Reflection', 'Solitude',
    'Suspense', 'Yearning', 'Bittersweet', 'Challenge', 'Emotion', 'Empathetic',
    'Miscalculation', 'Obstacle'
]

def categorize_sentiment(sentiment):
    sentiment = sentiment.strip()
    if sentiment in POSITIVE:
        return 'Positive'
    elif sentiment in NEGATIVE:
        return 'Negative'
    elif sentiment in NEUTRAL:
        return 'Neutral'
    else:
        # Default categorization based on common patterns
        neg_keywords = ['sad', 'anger', 'fear', 'hate', 'bad', 'negative', 'pain', 'hurt', 'loss', 'grief']
        pos_keywords = ['joy', 'happy', 'love', 'good', 'positive', 'excite', 'hope', 'peace', 'calm']

        sentiment_lower = sentiment.lower()
        for kw in neg_keywords:
            if kw in sentiment_lower:
                return 'Negative'
        for kw in pos_keywords:
            if kw in sentiment_lower:
                return 'Positive'
        return 'Neutral'

# Load data
df = pd.read_csv(os.path.join(DATA_DIR, 'sentimentdataset.csv'))
print(f'Dataset loaded: {df.shape}')

# Clean
df.columns = df.columns.str.strip()
df['Sentiment'] = df['Sentiment'].str.strip()

# Map to 3 categories
df['Sentiment_Category'] = df['Sentiment'].apply(categorize_sentiment)

print(f'\nSentiment distribution after categorization:')
print(df['Sentiment_Category'].value_counts())

# Parse timestamp
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Date'] = df['Timestamp'].dt.date
df['Year'] = df['Timestamp'].dt.year
df['Month'] = df['Timestamp'].dt.month
df['Week'] = df['Timestamp'].dt.isocalendar().week
df['Day'] = df['Timestamp'].dt.day

# Clean
df = df.dropna(subset=['Text', 'Sentiment_Category'])

# Encode
label_encoder = LabelEncoder()
df['sentiment_label'] = label_encoder.fit_transform(df['Sentiment_Category'])

# TF-IDF
tfidf = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X = tfidf.fit_transform(df['Text'].astype(str))
y = df['sentiment_label']

print(f'\nFeatures: {X.shape}')

# Split
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
    X, y, df.index, test_size=0.2, random_state=42, stratify=y
)
print(f'Train: {X_train.shape[0]}, Test: {X_test.shape[0]}')

# Train
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
target_names = label_encoder.classes_

print(f'\n{"="*50}')
print(f'RESULTS (3-Class Classification)')
print(f'{"="*50}')
print(f'Accuracy: {accuracy:.4f}')
print(f'Macro F1: {f1_score(y_test, y_pred, average="macro"):.4f}')

print(f'\nConfusion Matrix:')
cm = confusion_matrix(y_test, y_pred)
print(f'            {"  ".join([f"{n:>8}" for n in target_names])}')
for i, row in enumerate(cm):
    print(f'{target_names[i]:10} {row}')

print(f'\nClassification Report:')
print(classification_report(y_test, y_pred, target_names=target_names))

# Create test DataFrame
test_df = df.loc[idx_test].copy()
test_df['predicted_label'] = y_pred
test_df['predicted_sentiment'] = label_encoder.inverse_transform(y_pred)

# F1 by time
def calc_f1(group):
    return f1_score(group['sentiment_label'], group['predicted_label'], average='macro', zero_division=0)

f1_by_day = test_df.groupby('Date').apply(calc_f1).reset_index()
f1_by_day.columns = ['Date', 'F1_Score']

f1_by_week = test_df.groupby(['Year', 'Week']).apply(calc_f1).reset_index()
f1_by_week.columns = ['Year', 'Week', 'F1_Score']
f1_by_week['Period'] = f1_by_week['Year'].astype(str) + '-W' + f1_by_week['Week'].astype(str).str.zfill(2)

f1_by_month = test_df.groupby(['Year', 'Month']).apply(calc_f1).reset_index()
f1_by_month.columns = ['Year', 'Month', 'F1_Score']
f1_by_month['Period'] = f1_by_month['Year'].astype(str) + '-' + f1_by_month['Month'].astype(str).str.zfill(2)

# Save results
test_results = test_df[['Text', 'Sentiment', 'Sentiment_Category', 'predicted_sentiment',
                        'sentiment_label', 'predicted_label',
                        'Timestamp', 'Date', 'Year', 'Month', 'Week', 'Day', 'Platform', 'Country']].copy()
test_results.columns = ['Text', 'original_sentiment', 'actual_sentiment', 'predicted_sentiment',
                        'actual_label', 'predicted_label',
                        'Timestamp', 'Date', 'Year', 'Month', 'Week', 'Day', 'Platform', 'Country']
test_results['is_correct'] = (test_results['actual_label'] == test_results['predicted_label']).astype(int)

test_results.to_csv(os.path.join(DATA_DIR, 'sentiment_test_results.csv'), index=False)
f1_by_day.to_csv(os.path.join(DATA_DIR, 'sentiment_f1_by_day.csv'), index=False)
f1_by_week.to_csv(os.path.join(DATA_DIR, 'sentiment_f1_by_week.csv'), index=False)
f1_by_month.to_csv(os.path.join(DATA_DIR, 'sentiment_f1_by_month.csv'), index=False)

# Confusion matrix for Power BI
cm_data = []
for i, actual in enumerate(target_names):
    for j, predicted in enumerate(target_names):
        cm_data.append({'actual_sentiment': actual, 'predicted_sentiment': predicted, 'count': int(cm[i][j])})
pd.DataFrame(cm_data).to_csv(os.path.join(DATA_DIR, 'sentiment_confusion_matrix.csv'), index=False)

print(f'\n{"="*50}')
print('Files saved:')
print(f'  - sentiment_test_results.csv ({test_results.shape[0]} rows)')
print(f'  - sentiment_f1_by_day.csv')
print(f'  - sentiment_f1_by_week.csv')
print(f'  - sentiment_f1_by_month.csv')
print(f'  - sentiment_confusion_matrix.csv')
