import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
import nltk     

file_path = 'C:/Users/PC/OneDrive/Desktop/SQL/Final project/DEPI/Datasets/Origin/store_reviews_with_states.csv'
data = pd.read_csv(file_path)

data.columns = data.columns.str.strip()
data['rating_int'] = data['rating'].str.extract('(\d)').astype(int)

def categorize_rating(rating):
    if rating in [1, 2]:
        return 'Negative'
    elif rating == 3:
        return 'Neutral'
    else:
        return 'Positive'

data['sentiment'] = data['rating_int'].apply(categorize_rating)

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
data['nltk_sentiment'] = data['review'].apply(lambda x: sia.polarity_scores(x)['compound'])
data['nltk_sentiment_category'] = data['nltk_sentiment'].apply(lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral')

sentiment_counts = data['sentiment'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Sentiment Distribution of Reviews')
plt.axis('equal')
plt.show()

plt.figure(figsize=(8, 6))
plt.hist(data['rating_int'], bins=np.arange(0.5, 6.5, 1), edgecolor='black', align='mid')
plt.xticks(range(1, 6))
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.grid(axis='y')
plt.show()

print(data[['review', 'rating_int', 'sentiment', 'nltk_sentiment', 'nltk_sentiment_category']].head())
