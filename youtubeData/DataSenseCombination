import google.auth
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon (important for sentiment analysis)
nltk.download('vader_lexicon')

# Set up Google Sheets credentials and API
SPREADSHEET_ID = "1P-SoP7CxZgbgwPNWsaCY-hnMn0CuvH4xxsn5olBYDvI"  # Replace with your sheet ID
SHEET_NAME = "YouTubeComments"
GOOGLE_SHEETS_CREDENTIALS_FILE = "credentials.json"

# YouTube API credentials
YOUTUBE_API_KEY = "AIzaSyDQZELyCHV-4YOsIERs4SBIbBngm8oTAvA"

# Authenticate and build the YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Authenticate Google Sheets API client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# List of video IDs
VIDEO_IDS = [
    "skR0faWG0CE",
    "PhmQHqo1qSM",
    "ApoewgP9St0"
]

# Function to get YouTube comments
def get_youtube_comments(video_ids):
    all_comments = []

    for VIDEO_ID in video_ids:
        print(f"Fetching comments for video ID: {VIDEO_ID}")

        nextPageToken = None
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=VIDEO_ID,
                maxResults=100,
                pageToken=nextPageToken,
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

                all_comments.append([author_name, comment, published_at])  # Store as list for easy Google Sheets update

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break

    return all_comments

# Function to perform sentiment analysis
def analyze_sentiment(comments):
    sia = SentimentIntensityAnalyzer()
    sentiments = []

    for comment in comments:
        score = sia.polarity_scores(comment[1])['compound']
        if score >= 0.05:
            sentiment = 'Positive'
        elif score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        comment.append(sentiment)  # Add sentiment as a new column

    return comments

# Function to write data to Google Sheets
def write_to_google_sheets(comments_data):
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    sheet.clear()  # Clear existing data before writing new data

    # Add headers
    sheet.append_row(["Author", "Comment", "Published At", "Sentiment"])

    # Add new data
    for comment in comments_data:
        sheet.append_row(comment)

# Main execution
if __name__ == "__main__":
    # Step 1: Get comments from YouTube
    comments_data = get_youtube_comments(VIDEO_IDS)

    # Step 2: Perform sentiment analysis
    comments_with_sentiment = analyze_sentiment(comments_data)

    # Step 3: Write to Google Sheets
    write_to_google_sheets(comments_with_sentiment)

    print(f"✅ Successfully fetched, analyzed, and saved {len(comments_with_sentiment)} comments to Google Sheets.")
