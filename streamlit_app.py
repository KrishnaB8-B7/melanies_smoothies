# Import python packages
import streamlit as st
import requests

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruis you want in your custom Smoothie!");

#option = st.selectbox('what is your favorate fruit?',('Banana','Strawberries','Peaches'));

#st.write('You favorate fruit is:', option);

from snowflake.snowpark.functions import col 

name_on_order = st.text_input('Name on Smoothie')
st.write('Name on the smoothie id:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    

    time_to_insert = st.button('Submit the Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

#copied from snowflake
