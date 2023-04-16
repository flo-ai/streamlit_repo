
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

#add text box, normalize json data ->  encapsulated in a try-except block
streamlit.header("Fruityvice Fruit Advice")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')     
    if not fruit_choice:
          streamlit.error("Please select a fruit to get information")
    else: 
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
         fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
         streamlit.dataframe(fruityvice_normalized)
         
except URLError as e:
      streamlit.error()


         
streamlit.stop() 

#connector info 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)


#add second textbox
add_my_fruit = streamlit.text_input('What fruit would you like to add?', "jackfruit")
streamlit.write("Thanks for adding",add_my_fruit)

#add insert query
my_cur.execute("insert into fruit_load_list values('from streamlit')")
               
                  
