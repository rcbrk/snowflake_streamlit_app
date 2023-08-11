
import streamlit
import pandas
import requests

import snowflake.connector
from urllib.error import URLError

####################

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

####################

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado'])

if not fruits_selected :
    fruits_selected = list(my_fruit_list.index)

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

####################

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(fc):
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fc}")
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

try :
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    streamlit.write('The user entered ', fruit_choice)
    if not fruit_choice:
        streamlit.error("please select a fruit")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))

except URLError as e :
    streamlit.error()

####################

streamlit.header("View Our fruit list :")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

def insert_fruit(ft):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('{ft}')")
    
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.dataframe(get_fruit_load_list())
    my_cnx.close()

fruit_toadd = streamlit.text_input('What fruit would you like to add ?')
streamlit.write('The user added ', fruit_toadd)

if streamlit.button('Add fruit to load list') and fruit_toadd != '':
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    insert_fruit(fruit_toadd)
    my_cnx.close()
    streamlit.text(f'Thanks adding {fruit_toadd}')
