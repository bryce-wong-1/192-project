import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px


# Connect to the SQLite database
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()

# SQL to fetch data from VoltageLog, selecting only the needed columns
sql_query = 'SELECT Seconds, Voltage FROM VoltageLog'
cursor.execute(sql_query)

# Fetch the rows from the query
rows = cursor.fetchall()

# Close the database connection
conn.close()

# Convert the results to a pandas DataFrame and set 'Seconds' as the index
df = pd.DataFrame(rows, columns=['Seconds', 'Voltage'])
df.set_index('Seconds', inplace=True)

# Streamlit user interface
st.title("Voltage Data Over Time")
st.dataframe(df.reset_index())  # Display DataFrame without index

# Create visualizations

# Create a Plotly Express line chart
fig = px.line(df.reset_index(), x='Seconds', y='Voltage', title='Voltage Over Time')

choice = ['Voltage Scatter Chart', 'Voltage Line Chart', 'Voltage Area Chart']
select = st.selectbox("Choose a chart",choice)
match select:
    case 'Voltage Line Chart':
        st.plotly_chart(fig)  
    case 'Voltage Scatter Chart':
        st.scatter_chart(df)
    case 'Voltage Area Chart':
        st.area_chart(df)
    case _:
        st.scatter_chart(df)

