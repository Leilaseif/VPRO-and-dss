import gspread
from oauth2client.service_account import ServiceAccountCredentials
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Set up the Google Sheets API credentials and scope
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.file"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name (change to your sheet's name)
sheet = client.open("VPRO_YouTube_Comments").sheet1

# Read all the comments from the sheet (adjust according to the column names in your sheet)
comments = sheet.col_values(3)  # Assuming comments are in the third column (C)

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get sentiment score
def get_sentiment_score(comment):
    score = analyzer.polarity_scores(comment)
    return score['compound']  # We'll use the compound score as the overall sentiment

# Analyze sentiment and print the results
for comment in comments:
    sentiment_score = get_sentiment_score(comment)
    print(f"Comment: {comment}\nSentiment Score: {sentiment_score}\n")

# Optional: Write sentiment scores to a new column (column D)
for i, comment in enumerate(comments, start=2):  # start=2 to start at the second row (assuming headers are in row 1)
    sentiment_score = get_sentiment_score(comment)
    sheet.update_cell(i, 4, sentiment_score)  # Update column D with the sentiment score
