
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError


#load data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.title("My Parent's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')


#add multiselect widget
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


#show df
streamlit.header('🍌🥭 Build your own fruit smoothie 🥝🍇')
streamlit.dataframe(fruits_to_show)

#get fruit function
def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


#add text box, normalize json data ->  encapsulated in a try-except block
streamlit.header("Fruityvice Fruit Advice")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')     
    if not fruit_choice:
          streamlit.error("Please select a fruit to get information")
    else: 
         fruityvice_normalized = get_fruityvice_data(fruit_choice)
         streamlit.dataframe(fruityvice_normalized)
         
except URLError as e:
      streamlit.error()
 
streamlit.header("The fruit load list contains:")

#snowflake functions
def get_fruit_load_list():     #gets fruits
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()


#button to load fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

#add fruit    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('test')")
        return "Thanks for adding " + new_fruit

        
#add second textbox
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):     #adds button
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)               
                  
