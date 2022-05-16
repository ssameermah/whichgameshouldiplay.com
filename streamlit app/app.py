from re import L
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import json
from streamlit_lottie import st_lottie
import requests 
import streamlit as st
from PIL import Image
from rec_functions import multi_game_normal, multi_game_advance 

df = pd.read_csv('game_rating.csv',index_col=0)
# game_groupby_users_Ratings = df.groupby('Users')['user_rating']
# game_groupby_users_Ratings = pd.DataFrame(game_groupby_users_Ratings.count())
# user_list_min50_ratings = game_groupby_users_Ratings[game_groupby_users_Ratings['user_rating'] > 4].index
# df_games =  df[df['Users'].isin(user_list_min50_ratings)]
# # df_games.to_csv('game_rating.csv')

img = Image.open('console wallpaper.png')
st.set_page_config(layout="wide",page_title='whichgameshouldiplay',page_icon="🎮")

hide_menu_style = """
    <style>
 
    footer {visibility : hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html= True)

page_bg_img = '''
    <style>
    .stApp {
    background-image: url('https://t3.ftcdn.net/jpg/04/32/19/92/360_F_432199214_DHg0zMd2KuEYMSF7ehvyFVnqkyp7dXrg.jpg');
    background-size: 1922px 1000px;
    background-repeat: no-repeat;
    background-attachment: scroll;
    }
    </style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)


header = st.container()
game_input = st.container()
feedback = st.container()


with header:
    # st.title('Video Game Recommendation')
    
    # st.header('Which game would you probably like next?')
    st.markdown("<h1 style='text-align: center; color: white;'>Video Game Recommendation</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: white;'>Which game would you probably like next?</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white;'>Please provide the games you enjoy</p>", unsafe_allow_html=True)
    # st.text('')
    # def load_lottieurl(url:str):
    #     r = requests.get(url)
    #     if r.status_code != 200:
    #         return None
    #     return r.json()

    # lottie_console = load_lottieurl('https://lottiefiles.com/44376-3d-gamepad-animation')
    # st_lottie(
    #     lottie_console
    # )

with game_input:
    col_a, col_b, col_c = st.columns(3)
    search_type = col_b.radio(
     "Choose between normal or advance search",
     ('Normal', 'Advance'))
    col_b.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    col_1,col_2,col_3 = st.columns(3)
    M = [0,1,2]
    a = df['Game_name'].unique()
    L = []
    for i in range(len(a)):
        L.append(a[i]) 

    #game recommendation


    if search_type == 'Normal':
        
        a_1 = col_1.selectbox('Game Name',(L),key = "a_1")
        b_1 = col_2.selectbox('Game Name',(L),key = "b_1")
        c_1 = col_3.selectbox('Game Name',(L),key = "c_1")

        game_list = [a_1,b_1,c_1]
        if col_2.button('Get Recommendations'):
            if a_1 != b_1 != c_1:
                col_2.text("Here are some games that we think you might enjoy!")
                col_2.write(multi_game_normal(game_list))
            else:
                col_2.text('Please input 3 different games')
        
        
    elif search_type == 'Advance':
     
        a_1 = col_1.selectbox('Game Name',(L),key="a_1")
        a_2 = col_1.select_slider('Game Graphics Quality and Reliability Score',[0,1,2,3,4],key = "a_2")
        # a_3 = col_1.slider('Game Reliability Score',0,1,2,key = "a_3")
        a_3 = col_1.select_slider('Game Replayable and Enjoyable Score',[0,1,2,3,4],key = "a_3")
        # a_5 = col_1.slider('Game Enjoyable Score',0,1,2,key = "a_5")
        a_4 = col_1.slider('Game Price Score',0,1,2,key = "a_4")
        a = a_2+a_3+a_4
        col_1.text(f'Total Score: {a}')
        b_1 = col_2.selectbox('Game Name',(L),key = "b_1")
        b_2 = col_2.select_slider('Game Graphics Quality and Reliability Score',[0,1,2,3,4],key = "b_2")
        # b_3 = col_2.slider('Game Reliability Score',0,1,2,key = "b_3")
        b_3 = col_2.select_slider('Game Replayable and Enjoyable Score',[0,1,2,3,4],key = "b_3")
        # b_5 = col_2.slider('Game Enjoyable Score',0,1,2,key = "b_5")
        b_4 = col_2.slider('Game Price Score',0,1,2,key = "b_4")
        b = b_2+b_3+b_4
        col_2.text(f'Total Score: {b}')
        c_1 = col_3.selectbox('Game Name',(L),key = "c_1")
        c_2 = col_3.select_slider('Game Graphics Quality and Reliability Score',[0,1,2,3,4],key = "c_2")
        # c_3 = col_3.slider('Game Reliability Score',0,1,2,key = "c_3")
        c_3 = col_3.select_slider('Game Replayable and Enjoyable Score',[0,1,2,3,4],key = "c_3")
        # c_5 = col_3.slider('Game Enjoyable Score',0,1,2,key = "c_5")
        c_4 = col_3.slider('Game Price Score',0,1,2,key = "c_4")
        c = c_2+c_3+c_4
        col_3.text(f'Total Score: {c}')

        # col_2.text('Game Graphics Quality and Reliablity Score: \nRate on 0 - 4 scale.\nAre the Graphics good and the game reliable?')
        # # col_2.text('Game Reliability Score: Rate Reliability of game on 0 - 2 scale.\nDoes the game crash or lags?')
        # col_2.text('Game Replayable and Enjoyable Score: \nRate on 0 - 4 scale.\nWill you replay this game often and how enjoyable is it?')
        # # col_2.text('Game Enjoyable Score: Rate Enjoyability of game on 0 - 2 scale.\nHow much do you enjoy this game?')
        # col_2.text('Game Price Score: \nRate on 0 - 2 scale.\nAre you happy with the price for this game?')
        # col_2.text('Please provide the scores for the game')

        game_dict = {a_1:a,b_1:b,c_1:c}
        if col_2.button('Get Recommendations'):
            if a_1 != b_1 != c_1:
                col_2.text("Here are some games that we think you might enjoy!")
                col_2.write(multi_game_advance(game_dict))
            else:
                col_2.text('Please input three different games and their scores')


with feedback:
    # st.title('Video Game Recommendation')
    
    # st.header('Which game would you probably like next?')
    st.markdown("<h2 style='text-align: center; color: white;'>Post your Feedback</h2>", unsafe_allow_html=True)
    col_1,col_2,col_3 = st.columns(3)

    col_2.markdown("<p style='text-align: left; color: white;'>Please provide your inputs to help us improve\n the algorithm</p>", unsafe_allow_html=True)
    col_2.write("Please fill [link](https://forms.gle/iwvFxcWo5zhNEVCB8) to contribute. Thank you :)")