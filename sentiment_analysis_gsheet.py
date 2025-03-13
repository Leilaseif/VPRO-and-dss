import gspread
from oauth2client.service_account import ServiceAccountCredentials
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Set up the Google Sheets API credentials and scope
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.file"]
creds = ServiceAccountCredentials.from_json_keyfile_name("carbon-facet-434318-b7-784eb604ce83.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet by name
sheet = client.open("VPRO_YouTube_Comments").sheet1  # You can change sheet1 to the correct tab if needed

# Read all the comments from the sheet (assuming comments are in column C, which is index 3)
comments = sheet.col_values(3)[1:]  # Skip the header row

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get sentiment score
def get_sentiment_score(comment):
    score = analyzer.polarity_scores(comment)
    return score['compound']  # Use the compound score as the overall sentiment

# Analyze sentiment and print the results
for i, comment in enumerate(comments, start=2):  # start=2 because rows start at 2 (skip header)
    sentiment_score = get_sentiment_score(comment)
    print(f"Comment: {comment}\nSentiment Score: {sentiment_score}\n")
    
    # Update the sentiment score in the 'Sentiment Score' column (Column D, which is index 4)
    sheet.update_cell(i, 4, sentiment_score)

print("Sentiment analysis and updates complete.")
