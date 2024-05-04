from Modules.mods import *

#Pre-Processing Data from Dataset
def readData(file_path="Datasets/twitter_dataset.csv"): #File path is optional
    data = pd.read_csv(file_path)
    data['Text'] = data['Text'].apply(refine_text)
    return data

def refine_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #Remove @mentions
    text = re.sub(r'#', '', text) #Remove "#" symbol
    text = re.sub(r'[^\w\s]', '', text) #Removing punctuations
    return text.lower()

def rank_text(tweets):
    vector = TfidfVectorizer()
    tfidf_matrix = vector.fit_transform(tweets['Text']) #Ranking Tweets using TF-IDF Weighting
    return tfidf_matrix, vector

#Using Vader Sentiment
def getVaderSentiment(text):
    obj = SentimentIntensityAnalyzer()
    return obj.polarity_scores(text)

def vader_analysis_score(score):
    if score['compound'] >= 0.05:
        return "Positive"
    elif score['compound'] <= -0.5:
        return 'Negative'
    else:
        return 'Neutral'

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
    # if(len(results) > 20):
    #     results = results[:20]
    results = [tweets.iloc[index] for index, _ in results]
    return pd.DataFrame(results) 


def main(query):
    data = readData()
    tf_idf, vector = rank_text(data)
    # query = input("Enter your Query: ")
    result_tweets = get_tweets(query, tf_idf, data, vector)
    vader_analysis = result_tweets
    tb_analysis = result_tweets
    
    #Vader Sentiment Analyser
    vader_analysis['Polarity'] = vader_analysis['Text'].apply(getVaderSentiment)
    vader_analysis['Class'] = vader_analysis['Polarity'].apply(vader_analysis_score)
    class_counts = vader_analysis['Class'].value_counts()



    # # Plotting the barh chart
    # plt.figure(figsize=(10, 6))
    # class_counts.plot(kind='barh', color='red')
    # plt.title(f'Tweets Based on Keyword {query} using Vader Sentiment Analyser')
    # plt.ylabel('Sentiment Class')
    # plt.xlabel('Number of Tweets')
    # plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    # plt.grid(axis='y')  # Add gridlines along the y-axis
    # plt.tight_layout() 
    # plt.show()
    return vader_analysis

# if __name__ == "__main__":
#     main()