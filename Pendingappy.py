# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 
import pandas as pd
# Write directly to the app
st.title("Example Streamlit App :balloon:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")


# Get the current credentials
session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')== False)
editable_df = st.data_editor(my_dataframe)




if st.button("Submit Changes"):
    for idx, row in editable_df.iterrows():
        # Update only if there is a change
        query = f"""
        UPDATE smoothies.public.orders
        SET ORDER_FILLED = {row['ORDER_FILLED']}
        WHERE ORDER_UID = {row['ORDER_UID']};
            """
        session.sql(query).collect()  # Execute update in Snowflake
   
    st.success('Someone clicked the button.', icon ="👍")
