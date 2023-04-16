
import streamlit
import pandas
#load data
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.title("My Parent's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')


#add multiselect widget
streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))

streamlit.header('🍌🥭 Build your own fruit smoothie 🥝🍇')
streamlit.dataframe(my_fruit_list)


                                
               
                  
