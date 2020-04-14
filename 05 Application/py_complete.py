import pandas as pd
import numpy as np
import pickle

with open('./data/cosine_sim.p', 'rb') as read_file: # movie cosine products
    cosine_sim = pickle.load(read_file)      # 10381 x 10381 numbers
df = pd.read_csv('./data/moviemapped.csv') # movie id / tag id / relevance
indices = pd.read_csv('./data/indices.csv',header=None,names=['title', 'TagmovieId']) # title - tagmovie id (0-10380)
with open('./data/svdpred.p', 'rb') as read_file: # movie cosine products
    svd = pickle.load(read_file)      # 10381 x 10381 numbers
ratings = pd.read_csv('data/ratings.csv')




def content_tag_recommender(title):#, cosine_sim=cosine_sim, df=df, indices=indices):
    # Obtain the index of the movie that matches the title
    #print("title",title)
    #idx = indices[title]
    #print("idx",idx)
    idx = indices[(indices["title"] == title[0])].index[0]
    # Get the pairwsie similarity scores of all movies with that movie
    # And convert it into a list of tuples as described above
    sim_scores = list(enumerate(cosine_sim[idx]))
    #  with "Toy Story (1995)" in title
    # [(0, 0.9999999999999999), (1, 0.7743635326655509), (2, 0.7054215147240148), (3, 0.6530303898449995) ....

    # Sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #[(0, 0.9999999999999999), (4331, 0.958830919528648), (2769, 0.9555216674015985), (2064, 0.9488923890883056)

    # Get the scores of the 100 most similar movies. Ignore the first movie.
    sim_scores = sim_scores[1:101]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    #[4331, 2769, 2064, 5445, 9070, 7994, 4602, 3809 ......

    # Return the top 10 most similar movies
    df3 = df['title'].iloc[movie_indices]
    df3.to_csv('./data/contentreco.csv')
    return

# function to return the list of movies recommended
def cross_rating(UID,MID):
    rating = ratings[(ratings['userId'] == UID) & (ratings['movieId'] == MID)]['rating']
    if rating.size == 0:
        rate = 0
    elif rating.size == 1:
        rate = rating.values[0]
    return rate

def collaborative_recommender(viewer,title):
    df4 = pd.read_csv('./data/contentreco.csv',names = ['TagmovieId','title'],header = None)
    df5 = pd.merge(df4, df, left_index=True, on=['title'])
    df5['givenrating'] = df5.apply(lambda x: cross_rating(viewer,x['movieId']), axis=1)
    df5['predrating'] = df5.apply(lambda x: svd.predict(viewer, x['movieId']).est, axis=1)
    df5['rating'] = df5.apply(lambda x: x['givenrating'] if x['givenrating'] != 0 else(x['predrating']) , axis=1)
    df6 = df5.sort_values(['rating'],ascending=[0])
    df6.to_csv('./data/hybridreco.csv') # to keep trace of the end result
    df7 = df6[(df6['givenrating'] != df6['rating'])].head(5) # return only what viewer did not see before
    cols = [1]
    df8 = df7[df7.columns[cols]]
    #return df7.head()
    return df8
