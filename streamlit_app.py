# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothies :cup_with_straw:")
st.write("Choose the fruits you want in your custom Streamlit smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothies: ")
st.write("The name on your Smoothie will be: ", name_on_order)

# Snowflake connection
try:
    cnx = st.connection("Snowflake")
    session = cnx.session()
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    
    # Convert dataframe to list for multiselect
    fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

    # Create a multi-select widget
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_list,
        max_selections=5
    )

    # Display the selected ingredients
    if ingredients_list:
        # Initialize an empty string to concatenate selected ingredients
        ingredients_string = ', '.join(ingredients_list)

        # Display the concatenated string of selected ingredients
        st.write(ingredients_string)

        my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')"""

        time_to_insert = st.button('Submit Order')

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.write("Please ensure your Snowflake connection is properly configured in the secrets.")
