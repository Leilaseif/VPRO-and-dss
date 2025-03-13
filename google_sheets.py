from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name
spreadsheet = client.open("VPRO_YouTube_Comments")
sheet = spreadsheet.sheet1

# Fetch all the comments from the sheet
comments = sheet.col_values(3)  # Assuming column 3 contains the comments

# Set up the Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

# Analyze sentiment of each comment
sentiments = []
for comment in comments:
    score = sia.polarity_scores(comment)['compound']  # Compound score is a good overall sentiment score
    if score >= 0.05:
        sentiment = 'Sad'  # Positive sentiment
    elif score <= -0.05:
        sentiment = 'Happy'    # Negative sentiment
    else:
        sentiment = 'Neutral'  # Neutral sentiment
    sentiments.append(sentiment)

# Add sentiment column to your existing Google Sheet data
comments_with_sentiments = sheet.get_all_records()  # This will get all data from the sheet

# Update the sheet with the sentiment values in a new column
for i, sentiment in enumerate(sentiments, start=2):  # Assuming the first row is headers
    sheet.update_cell(i, 4, sentiment)  # Update the 4th column (sentiment column)
