from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Download VADER lexicon (important)
nltk.download('vader_lexicon')

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet
spreadsheet = client.open("VPRO_YouTube_Comments")
sheet = spreadsheet.sheet1

# Fetch comments from column C (assuming comments are in column 3)
comments = sheet.col_values(3)[1:]  # Skip header row

# Set up Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Analyze sentiment for each comment
sentiments = []
for comment in comments:
    score = sia.polarity_scores(comment)['compound']
    if score >= 0.05:
        sentiment = 'Positive'  # Positive sentiment
    elif score <= -0.05:
        sentiment = 'Negative'    # Negative sentiment
    else:
        sentiment = 'Neutral'
    sentiments.append(sentiment)

# Batch update Sentiment column (D)
sentiment_column = [['Sentiment']] + [[s] for s in sentiments]  # Add header + values
sheet.update(f"H1:H{len(sentiments) + 1}", sentiment_column)  # Update all at once

print("✅ Sentiment analysis updated successfully!")
