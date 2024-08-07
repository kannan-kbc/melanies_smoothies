# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your app :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order=st.text_input('name_on_smoothie')
st.write('The Name on your smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert snowpark data frame to a pandas data frame so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredients_list = st.multiselect(
   'Choose upto 5 Ingrediants:',my_dataframe,
    max_selections=5)

ingredients_string = ''
#st.write("You selected:", my_dataframe)
if ingredients_list:
    ingredients_string = ''


for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    st.subheader(fruit_chosen + 'Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    
#st.write(ingredients_string)


 
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

#st.write(my_insert_stmt)
#st.text

time_to_insert = st.button('submit order')

if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")







