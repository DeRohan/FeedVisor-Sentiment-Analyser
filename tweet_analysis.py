import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Pre-Processing Data from Dataset
def readData(file_path="Datasets/twitter_dataset.csv"): #File path is optional
    data = pd.read_csv(file_path)
    data['Text'] = data['Text'].apply(refine_text)
    return data

def refine_text(text):
    text = re.sub(r'[^\w\s]', '', text) #Removing punctuations
    return text.lower()

def rank_text(tweets):
    vector = TfidfVectorizer()
    tfidf_matrix = vector.fit_transform(tweets['Text'])
    return tfidf_matrix, vector


def get_tweets(query, tfidf_matrix, tweets, vector, alpha=0.05):
    query = refine_text(query)
    query = vector.transform([query])
    score = cosine_similarity(query, tfidf_matrix)
    tweet_indexes = score.argsort()[0][::-1]
    results = []

    #Getting only top ranked tweets using Cosine Similarity
    for index in tweet_indexes:
        sim_score = score[0][index]
        if sim_score >= alpha:
            results.append((index, sim_score))
        else:
            break
    #Top 20 Tweets
    if(len(results) > 20):
        results = results[:20]
    results = [tweets.iloc[index] for index, _ in results]
    return pd.DataFrame(results) 


if __name__ == "__main__":
    query = input("Enter your Query: ")
    data = readData()
    tf_idf, vector = rank_text(data)

    res = get_tweets(query, tf_idf, data, vector)
    
    for index, row in res.iterrows():
        print(f"Tweet ID: {row['Tweet_ID']}")
        print(f"Username: {row['Username']}")
        print(f"Text: {row['Text']}")
        print(f"Retweets: {row['Retweets']}")
        print(f"Likes: {row['Likes']}")
        print(f"Timestamp: {row['Timestamp']}")
        print()