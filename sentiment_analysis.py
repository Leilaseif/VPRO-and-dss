from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create a SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()

# Example comment
comment = "This video is amazing! AI is changing everything."

# Analyze the sentiment
score = analyzer.polarity_scores(comment)

# Print the result
print(f"Sentiment score: {score}")
