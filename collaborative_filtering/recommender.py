from main.models import Product, Review

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django_pandas.io import read_frame

def gen_similarity_matrix(x = 5 , y = 100):
    # Read data
    ratings = read_frame(Review.objects.all(), ['product_name', 'rating', 'username'], verbose=False)
    # ratings.head()

    # Remove irrelevant columns
    # ratings.drop(['Content'], axis=1, inplace=True)
    # print(len(ratings.index))
    ratings.drop_duplicates(inplace=True)
    # print(len(ratings.index))
    # ratings.info()

    # Print dataset info
    print('Dataset has', ratings['product_name'].nunique(), 'products')
    print('Dataset has', ratings['username'].nunique(), 'reviewers')
    print('Dataset has ratings in range', sorted(ratings['rating'].unique()))

    # Filter to keep reviewers with at least x or 5 reviews to test due to lack of similarity
    reviewer_ratings = ratings.groupby('username').agg(rating_counts = ('rating', 'count')).reset_index().sort_values(by='rating_counts', ascending=False)#.to_excel("reviewer_rating_counts.xlsx")
    reviewer_ratings_GT5 = reviewer_ratings[reviewer_ratings['rating_counts']>x].drop(['rating_counts'], axis=1)

    # Filter to keep products with at least y or 100 reviews for managable calculations
    avg_ratings = ratings.groupby('product_name').agg(mean_rating = ('rating', 'mean'),
                                                    rating_counts = ('rating', 'count')).reset_index()
    avg_ratings_GT100 = avg_ratings[avg_ratings['rating_counts']>y]
    # avg_ratings_GT100.info()

    # Check most popular products
    avg_ratings.sort_values(by='rating_counts', ascending=False)#.head()

    ratings_GT100 = pd.merge(ratings, avg_ratings_GT100[['product_name']], on='product_name', how='inner')
    ratings_GT100 = pd.merge(ratings_GT100, reviewer_ratings_GT5[['username']], on='username', how='inner')
    # ratings_GT100.info()

    # Create Reviewer-Rating matrix
    matrix = ratings_GT100.pivot_table(index='username', columns='product_name', values='rating')
    # matrix.head()

    # Normalize the matrix based on each reviewer's average rating
    matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 'rows')
    # matrix_norm.head()

    # Measure similarity with pearson correlation
    matrix_similarity = matrix_norm.T.corr()
    # matrix_similarity.head()
    
    # Save matrices to files
    matrix.to_excel('matrix.xlsx', index=True)
    matrix_norm.to_excel('matrix_norm.xlsx', index=True)
    matrix_similarity.to_excel('matrix_similarity.xlsx', index=True)

# target, similarity threshold(0.3), how many similar reviewers(10), how many top products(10)
def make_prediction(target_reviewer = 'J***.', similarity_thresh = 0.3, n = 10, m = 10):#, product = ''): # target reviewer placeholder default value
    # Load dataframe from file
    matrix = pd.read_excel("matrix.xlsx", index_col=0)
    # Testing
    matrix_norm = pd.read_excel("matrix_norm.xlsx", index_col=0)
    matrix_similarity = pd.read_excel("matrix_similarity.xlsx", index_col=0)
    
    '''
    # Unspecified product assumes output at most top m most recommended products
    if product == '':
        # Load other dataframes from file
        matrix_norm = pd.read_excel("matrix_norm.xlsx", index_col=0)
        matrix_similarity = pd.read_excel("matrix_similarity.xlsx", index_col=0)
    # Specified product unrates the product to be included in predictions
    else:
        # Unrate the product in the dataframe
        matrix[product] = np.nan
        # Recalculate dataframes to include product as unrated
        matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 'rows')
        matrix_similarity = matrix_norm.T.corr()
    '''

    # Remove target from list of similar reviewers
    matrix_similarity.drop(index=target_reviewer, inplace=True)

    # matrix_similarity.head()

    # no.of similar reviewers
    # n = 10

    # similarity threshold
    # similarity_thresh = 0.3

    # get top n similar reviewers
    similar_reviewers = matrix_similarity[matrix_similarity[target_reviewer]>similarity_thresh][target_reviewer]

    # Print top n similar reviewers
    print(f'The similar reviewers for {target_reviewer} are', similar_reviewers.head(n))

    target_reviewer_reviewed = matrix_norm[matrix_norm.index == target_reviewer].dropna(axis=1, how='all')
    # target_reviewer_reviewed

    similar_reviewer_products = matrix_norm[matrix_norm.index.isin(similar_reviewers.index)].dropna(axis=1, how='all')
    # similar_reviewer_products

    similar_reviewer_products.drop(target_reviewer_reviewed.columns,axis=1, inplace=True, errors='ignore')
    # similar_reviewer_products

    # A dictionary to store item scores
    item_score = {}

    # Loop through items
    for i in similar_reviewer_products.columns:
        # Get the ratings for product i
        product_rating = similar_reviewer_products[i]
        # Create a variable to store the score
        total = 0
        # Create a variable to store the number of scores
        count = 0
        # Loop through similar users
        for u in similar_reviewers.index:
            # If the product has rating
            if pd.isna(product_rating[u]) == False:
                # Score is the sum of user similarity score multiply by the product rating
                score = similar_reviewers[u] * product_rating[u]
                # Add the score to the total score for the product so far
                total += score
                # Add 1 to the count
                count +=1
        # Get the average score for the item
        item_score[i] = total / count

    # Convert dictionary to pandas dataframe
    item_score = pd.DataFrame(item_score.items(), columns=['product', 'product_score'])
        
    # Sort the product by score
    ranked_item_score = item_score.sort_values(by='product_score', ascending=False)

    # Select top m products
    # m = 10
    # ranked_item_score.head(m)

    # Average rating for the picked user
    avg_rating = matrix[matrix.index == target_reviewer].T.mean()[target_reviewer]

    # Print the average product rating for user 1
    print(f'The average product rating for user {target_reviewer} is {avg_rating:.2f}')

    # Calcuate the predicted rating
    ranked_item_score['predicted_rating'] = ranked_item_score['product_score'] + avg_rating

    # Take a look at the data
    # ranked_item_score.head(m)
    top_m = ranked_item_score.head(m)
    predictions = []
    for i in range(len(top_m.index)):
        predictions.append([target_reviewer, ranked_item_score.iloc[i]['product'], ranked_item_score.iloc[i]['predicted_rating']])
    return predictions # return username, product, prediction

# NOT WORKING
def test_accuracy(n = 10, m = 10):
    # Find buyers who reviewed at least n products
    ratings = read_frame(Review.objects.all(), ['product_name', 'rating', 'username'], verbose=False)
    ratings.drop_duplicates(inplace=True)
    rating_count = ratings.copy(deep=True).groupby('product_name').agg(rating_counts = ('rating', 'count')).reset_index()
    rating_count.sort_values(by='rating_counts', ascending=False)#.head()
    if isinstance(n, str):
        n = int(n)
    rating_count = rating_count.head(n)
    
    # Pick random m buyers to predict for
    #ratings = pd.merge(rating_count['product_name'], ratings, on='product_name', how='inner')
    review_count = ratings.copy(deep=True).groupby('username').agg(rating_counts = ('rating', 'count')).reset_index()
    review_count.sort_values(by='rating_counts', ascending=False)#.head()
    if isinstance(m, str):
        m = int(m)
    review_count = review_count.head(m)
    
    # Make list of products and users to look out for
    product_list = []
    user_list = []
    for i in range(len(rating_count)):
        product_list.append(rating_count.iloc[i]['product_name'])
    for i in range(len(review_count)):
        user_list.append(review_count.iloc[i]['username'])
    
    # Predict the score for each product for a total of n predictions
    results = []
    for i in range(len(user_list)):
        print("USER IS", user_list[i])
        results.append(make_prediction(user_list[i]))
    
    # Get predicted values and compare
    for i in range(len(results)):
        if results[i][0] in user_list and results[i][1] in product_list:
            actual_rating = Review.objects.all.filter(product_name=results[i][1], username=results[i][0])[0].rating
            print("Predicted", results[i][0], "rating", results[i][1], "as", results[i][2], "vs actual rating of", actual_rating)
            
# Product Report
# Top n products with highest rating and the most reviews (or the most reviews and the highest rating)
def top_products(n = 10, priority = "rating"):

    df = read_frame(Review.objects.all(), ['product_name', 'rating', 'username', 'comment'], verbose=False)
    
    df1 = df.groupby('product_name').agg(rating_counts = ('rating', 'count'), rating_max = ('rating', 'max')).reset_index().sort_values(by='rating_counts', ascending=False)
    
    if priority == "rating":
        df1.sort_values(by=['rating_max', 'rating_counts'], ascending=False, inplace=True)
    else:
        df1.sort_values(by=['rating_counts', 'rating_max'], ascending=False, inplace=True)
    
    return df1.head(n)

# Top m reviewers with the highest number of reviews and their average ratings given
def top_reviewers(m = 10):
    
    df = read_frame(Review.objects.all(), ['product_name', 'rating', 'username', 'comment'], verbose=False)
    
    df1 = df.groupby('username').agg(rating_counts = ('rating', 'count'),
                                     min_rating = ('rating', 'min'),
                                     max_rating = ('rating', 'max'),
                                     avg_rating = ('rating', 'mean')
                                     ).reset_index().sort_values(by='rating_counts', ascending=False)
    
    return df1.head(m)

# EXPERIMENTAL

def word_count(str):
    counts = dict()
    words = str.split()
    
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

# Top i keywords from top n product names
def top_prodname_keywords(df):
    namelist = df['product_name'].tolist()
    keywords = " ".join(str(name) for name in namelist)
    return word_count(keywords)

# Top j keywords from top n product descriptions
def top_prodesc_keywwords(df):
    namelist = df['product_name'].tolist()
    prodlist = Product.objects.filter(name__in=namelist)
    keywords = " ".join(str(prod.description) for prod in prodlist)
    return word_count(keywords)
    
# Top k keywords from top n product reviews
def top_prodrev_keywords(df):
    namelist = df['product_name'].tolist()
    revlist = Review.objects.filter(product_name__in=namelist).exclude(comment="nan")
    keywords = " ".join(str(rev.comment) for rev in revlist)
    return word_count(keywords)