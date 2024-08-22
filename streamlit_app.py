# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies:cup_with_straw:")
st.write("Choose the fruits you want in your custome Streamlit!")

# import streamlit as st

name_on_order = st.text_input("Name on Smoothies: ")
st.write("The name on your Smoothie will be: ", name_on_order)


# Snowflake connection
    cnx = st.connection("Snowflake")
    session = cnx.session()
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))

# Create a multi-select widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
      my_dataframe, #['Ingredients']  # Specify the column to use for options
      max_selections=5
)

# Display the selected ingredients
if ingredients_list:
    # Display the selected ingredients as a list
    # st.write('You selected:', ingredients_list)
    
    # Initialize an empty string to concatenate selected ingredients
    ingredients_string = ''

    # Concatenate the selected ingredients into a single string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  # Add a space or any delimiter you prefer

    # Display the concatenated string of selected ingredients
    st.write(ingredients_string)
    my_insert_stmt = """INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
    st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
