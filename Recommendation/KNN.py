#!/usr/bin/env python
# coding: utf-8

# # Recommendation Using KNN algorithm

# In[6]:


import os
import pandas as pd

# read data
data_path = 'C:\\Users\\suraj\\Documents\\Recommendation'
visitor_filename = 'Visitor-2020-09-03.csv'
ratings_filename = 'LocationReview-2020-09-03.csv'
location_filname='Location-2020-09-03.csv'


# In[7]:


os.getcwd()


# In[8]:


# read data
df_visitor = pd.read_csv(
    os.path.join(data_path, visitor_filename),

    usecols=['user'],
    dtype={'user': 'int32'})

df_ratings = pd.read_csv(
    os.path.join(data_path, ratings_filename),
    usecols=['commenter', 'location', 'rating'],
    dtype={'commenter': 'int32', 'location': 'int32', 'rating': 'float32'})

df_location = pd.read_csv(
    os.path.join(data_path,location_filname),

    usecols=['id','title'],
    dtype={'id': 'int32','title':'str'})


# In[9]:


df_visitor.head()
df_visitor.shape


# In[10]:


df_ratings.head()


# In[11]:


df_ratings.shape


# In[12]:


from scipy.sparse import csr_matrix
# pivot ratings into movie features
df_location_features = df_ratings.pivot(
    index='location',
    columns='commenter',
    values='rating'
).fillna(0)


# In[13]:


mat_location_features = csr_matrix(df_location_features.values)


# In[14]:


df_location_features.head()


# In[15]:


from sklearn.neighbors import NearestNeighbors
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)


# In[16]:


num_users = len(df_ratings.commenter.unique())
num_items = len(df_ratings.location.unique())
print('There are {} unique users and {} unique location in this data set'.format(num_users, num_items))


# In[17]:


df_ratings_cnt_tmp = pd.DataFrame(df_ratings.groupby('rating').size(), columns=['count'])
df_ratings_cnt_tmp


# In[18]:


# there are a lot more counts in rating of zero
total_cnt = num_users * num_items
rating_zero_cnt = total_cnt - df_ratings.shape[0]

df_ratings_cnt = df_ratings_cnt_tmp.append(
    pd.DataFrame({'count': rating_zero_cnt}, index=[0.0]),
    verify_integrity=True,
).sort_index()
df_ratings_cnt


# In[19]:


#log normalise to make it easier to interpret on a graph
import numpy as np
df_ratings_cnt['log_count'] = np.log(df_ratings_cnt['count'])
df_ratings_cnt


# In[20]:


import matplotlib.pyplot as plt
plt.style.use('ggplot')

# get_ipython().run_line_magic('matplotlib', 'inline')
ax = df_ratings_cnt[['count']].reset_index().rename(columns={'index': 'rating score'}).plot(
    x='rating score',
    y='count',
    kind='bar',
    figsize=(12, 8),
    title='Count for Each Rating Score (in Log Scale)',
    logy=True,
    fontsize=12,
)
ax.set_xlabel("location rating score")
ax.set_ylabel("number of ratings")


# In[21]:


# get rating frequency
#number of ratings each location got.
df_location_cnt = pd.DataFrame(df_ratings.groupby('location').size(), columns=['count'])
df_location_cnt.head()


# In[22]:


#now we need to take only location that have been rated atleast 5 times to get some idea of the reactions of users towards it

popularity_thres = 5
popular_location = list(set(df_location_cnt.query('count >= @popularity_thres').index))
df_ratings_drop_location = df_ratings[df_ratings.location.isin(popular_location)]
print('shape of original ratings data: ', df_ratings.shape)
print('shape of ratings data after dropping unpopular location: ', df_ratings_drop_location.shape)


# In[23]:



# get number of ratings given by every user
df_users_cnt = pd.DataFrame(df_ratings_drop_location.groupby('commenter').size(), columns=['count'])
df_users_cnt.head()


# In[24]:


# filter data to come to an approximation of user likings.
ratings_thres = 5
active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
df_ratings_drop_users = df_ratings_drop_location[df_ratings_drop_location.commenter.isin(active_users)]
print('shape of original ratings data: ', df_ratings.shape)
print('shape of ratings data after dropping both unpopular movies and inactive users: ', df_ratings_drop_users.shape)


# In[25]:


# pivot and create movie-user matrix
location_user_mat = df_ratings_drop_users.pivot(index='location', columns='commenter', values='rating').fillna(0)
#map movie titles to images
location_to_idx = {
    location: i for i, location in 
    enumerate(list(df_location.set_index('id').loc[location_user_mat.index].title))
}
# transform matrix to scipy sparse matrix
location_user_mat_sparse = csr_matrix(location_user_mat.values)


# In[26]:


location_user_mat_sparse


# In[27]:


# define model
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10, n_jobs=-1)
# fit
model_knn.fit(location_user_mat_sparse)


# In[28]:


from fuzzywuzzy import fuzz


# In[29]:


def fuzzy_matching(mapper, fav_location, verbose=True):
    """
    return the closest match via fuzzy ratio. 
    
    Parameters
    ----------    
    mapper: dict, map movie title name to index of the movie in data

    fav_movie: str, name of user input movie
    
    verbose: bool, print log if True

    Return
    ------
    index of the closest match
    """
    match_tuple = []
    # get match
    for title, idx in mapper.items():
        ratio = fuzz.ratio(title.lower(), fav_location.lower())
        if ratio >= 60:
            match_tuple.append((title, idx, ratio))
    # sort
    match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
    if not match_tuple:
        print('Oops! No match is found')
        return
    if verbose:
        print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
    return match_tuple[0][1]


# In[30]:


def make_recommendation(model_knn, data, mapper, fav_location, n_recommendations):
    """
    return top n similar movie recommendations based on user's input movie


    Parameters
    ----------
    model_knn: sklearn model, knn model

    data: movie-user matrix

    mapper: dict, map movie title name to index of the movie in data

    fav_movie: str, name of user input movie

    n_recommendations: int, top n recommendations

    Return
    ------
    list of top n similar movie recommendations
    """
    # fit
    model_knn.fit(data)
    # get input movie index
    print('You have input movie:', fav_location)
    idx = fuzzy_matching(mapper, fav_location, verbose=True)
    
    print('Recommendation system start to make inference')
    print('......\n')
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    
    raw_recommends =         sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    # print recommendations
    print('Recommendations for {}:'.format(fav_location))
    for i, (idx, dist) in enumerate(raw_recommends):
        print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))


# In[31]:


location_to_idx


# In[32]:


my_favorite = 'Pashupatinath'


# In[33]:


d=make_recommendation(model_knn=model_knn,
    data=location_user_mat_sparse,
     fav_location=my_favorite,
    mapper=location_to_idx,
    n_recommendations=5)


# In[ ]:




