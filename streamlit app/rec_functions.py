from re import L
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_color_codes()
sns.set(style="whitegrid")
from scipy.stats import zscore
from sklearn import metrics
from sklearn.model_selection import train_test_split as sk_train_test
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
import math
import streamlit as st

df = pd.read_csv('game_rating.csv',index_col=0)


train_data, test_data = sk_train_test(df, test_size =.20, random_state=10)
#Only selecting users who have given more than 4 game reviews
df1 = df['Users'].value_counts().rename_axis('Users').reset_index(name='counts')
#df1 = df1[df1['counts'] > 10]
df_test = df.merge(df1,how='inner', on ='Users') 
#Creating a matrix with users in the rows and game_name as the columns

matrix = df_test.pivot_table(columns='Game_name', index='Users', values='user_rating', fill_value=0)

#function to centre all values in the matrix

def center(row):
    new_row = (row - row.mean()) / (row.max() - row.min())
    return new_row
matrix_std = matrix.apply(center)

def gameRec_modified(g):
    dota = matrix_std[g]
#Calculate Pearson Sim with all other games.
    dota = matrix.corrwith(dota).dropna()
#create a DF to show how many times each game has been played and the mean time it has been played
    gameData = df_test.groupby('Game_name').agg({'user_rating': [np.size, np.mean]})
#Filter out any game played by less than n players.
    gameSim = gameData['user_rating']['size'] >= 0
    df = gameData[gameSim].join(pd.DataFrame(dota, columns=['similarity']))
    return df['similarity']

#multiple games recommendation - function to recommend based on multiple input games.
x = list(matrix.keys())
df_4 = pd.DataFrame(x , columns= ["Game_name"])
index_list = []
def multi_game_normal(game_list):
    df_4['Total_similarity'] = 0
    #loop based on number of games entered
    for i in game_list:
        new_col = list(gameRec_modified(i))
        df_4[i] = new_col
        df_4['Total_similarity'] = df_4['Total_similarity'] + df_4[i]
    #average of similarity by number of games.
    df_4['Total_similarity'] = df_4['Total_similarity']/len(game_list)
    
    return df_4[['Game_name','Total_similarity']].sort_values(['Total_similarity'], ascending=False)[len(game_list):20] # to reomve games entered as input

x = list(matrix.keys())
df_4 = pd.DataFrame(x , columns= ["Game_name"])

def multi_game_advance(game_dict):
    df_4['Total_similarity'] = 0
    games = []
    rating_sum = 0
    
    for key in game_dict:
        #condition when only in game is input with rating
        if len(game_dict.keys())==1:
            if game_dict.get(key)==0:
                new_col = list(gameRec_modified(key))
                df_4[key] = new_col
                df_4['Total_similarity'] = df_4['Total_similarity'] + df_4[key]
                print(df_4[['Game_name','Total_similarity']])
                return df_4[['Game_name','Total_similarity']].sort_values(['Total_similarity'], ascending=True)[0:20]
            else:
                new_col = list(gameRec_modified(key))
                df_4[key] = new_col
                df_4['Total_similarity'] = df_4['Total_similarity'] + df_4[key]
                df_5 = df_4[df_4["Game_name"] != key]
                max_val = df_5['Total_similarity'].max()
                min_val = df_5['Total_similarity'].min()
                #print(max_val, min_val)
                adder=(max_val - min_val)/10
                max_range = min_val + adder*game_dict.get(key)
                df_out = df_5.loc[df_5['Total_similarity']<= max_range]
                return df_out[['Game_name','Total_similarity']].sort_values(['Total_similarity'], ascending=False)[0:20]
        else:
            new_col = list(gameRec_modified(key))
            df_4[key] = new_col
            df_4[key] = df_4[key]*((0.1)*game_dict.get(key))
            df_4['Total_similarity'] = df_4['Total_similarity'] + df_4[key]
            games.append(key)
            rating_sum+= game_dict.get(key)
            

    df_4['Total_similarity'] = df_4['Total_similarity']/len(game_dict)
    df_5 = df_4[~df_4["Game_name"].isin(games)]
    #if rating_sum==0:
    #    return df_5[['Game_name','Total_similarity']].sort_values(['Total_similarity'], ascending=True)[0:20]
    max_val = df_5['Total_similarity'].max()
    min_val = df_5['Total_similarity'].min()
    adder=(max_val - min_val)/10
    max_range = min_val + adder*(math.ceil(rating_sum/len(games)))
    df_6 = df_5.loc[df_5['Total_similarity']<= max_range]

    return df_6[['Game_name','Total_similarity']].sort_values(['Total_similarity'], ascending=False)[0:20]