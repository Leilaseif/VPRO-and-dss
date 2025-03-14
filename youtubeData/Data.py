import google.auth
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets credentials and API
SPREADSHEET_ID = "1P-SoP7CxZgbgwPNWsaCY-hnMn0CuvH4xxsn5olBYDvI"
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
    "skR0faWG0CE",  # Replace with actual video IDs
    "PhmQHqo1qSM",  # Another video ID
    "ApoewgP9St0"
]

# Function to get YouTube comments
def get_youtube_comments(video_ids):
    all_comments = []

    for VIDEO_ID in video_ids:
        print(f"Fetching comments for video ID: {VIDEO_ID}")

        # Pagination setup
        nextPageToken = None
        
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=VIDEO_ID,
                maxResults=100,
                pageToken=nextPageToken,
            )
            response = request.execute()

            # Extract and store the comments
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                author_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

                # Append the data as a tuple
                all_comments.append((author_name, comment, published_at))

            # Check if there is a next page of comments
            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break  # Exit if no more pages

    return all_comments

# Function to write comments to Google Sheets
def write_to_google_sheets(comments_data):
    # Open Google Sheets
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    # Write each comment to a new row in the sheet
    for i, (author_name, comment, published_at) in enumerate(comments_data):
        sheet.append_row([i + 1, author_name, comment, published_at])  # Add a row with comment data

# Main execution
if __name__ == "__main__":
    # Get comments from multiple videos
    comments_data = get_youtube_comments(VIDEO_IDS)

    # Write the comments to Google Sheets
    write_to_google_sheets(comments_data)

    print(f"Successfully fetched and saved {len(comments_data)} comments to Google Sheets.")
