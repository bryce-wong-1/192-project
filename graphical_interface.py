import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px


# Connect to the SQLite database
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()
# SQL to fetch data from VoltageLog, selecting only the needed columns
def set_tabs(tab):
    query = f'SELECT Seconds, {tab} FROM {tab}Log'
    cursor.execute(query)
    # Fetch the rows from the query
    rows = cursor.fetchall()
    # Convert the results to a pandas DataFrame and set 'Seconds' as the index
    df = pd.DataFrame(rows, columns=['Seconds', f'{tab}'])
    df.set_index('Seconds', inplace=True)
    return df

def graphs(tab, df):
    st.subheader(f"{tab} Data Over Time")
    st.dataframe(df.reset_index())  # Display DataFrame without index
    fig = px.line(df.reset_index(), x='Seconds', y=f'{tab}', title=f'{tab} Over Time')
    with st.container(border = True):
        choice = ['Line Chart', 'Scatter Chart', 'Area Chart']
        select = st.selectbox("Choose a chart",choice, key = tab)
        match select:
            case 'Line Chart':
                st.plotly_chart(fig)  # Display the plotly chart in Streamlit
            case 'Scatter Chart':
                st.scatter_chart(df)
            case 'Area Chart':
                st.area_chart(df)
            case _:
                st.plotly_chart(fig)
st.title("Vehicle Efficiency Insight Tool")        
tab1, tab2, tab3, tab4 = st.tabs(['Voltage', 'Current', 'Power', 'References'])
# Streamlit user interface


# Create visualizations
with tab1:
    df = set_tabs('Voltage')
    graphs('Voltage', df)

with tab2:
    df = set_tabs('Current')
    graphs('Current', df)
    
with tab3:
    df = set_tabs('Power')
    graphs('Power', df)
with tab4:
    with st.container(border=True):
        st.markdown(
            """
            Assumptions: 
            
            - Calculations are based on a Postal Vehicle 
            - Efficiency of system is ~ 2750 rpm (DC Motor) / 3000 rpm (Flywheel angular velocity needed to accelerate to 25-40 mph) = 91.6% 
            - Startup factor is assumed to lower gas mileage by ~10%\ - 40% 
            - Assume vehicle must travel 5 feet to confidently overcome inertia 
            - Postal vehicles get ~ 8.2 - 8.6 MPG (https://www.reuters.com/business/sustainable-business/white-house-epa-urge-us-postal-service-conduct-new-review-vehicle-plan-2022-02-02/) 
            - All postal service vehicles made 12.7 million stops in 2016 (https://facts.usps.com/size-and-scope/) 
            - Postal service vehicles travel ~10,000 miles annually (https://www.motorbiscuit.com/exactly-how-many-miles-usps-mail-truck-last/) 
            - There are 7,600 vehicles in operation (https://www.uspsoig.gov/reports/audit-reports/fuel-consumption-and-cost-risk-mitigation) 
            """
            )
    with st.container(border = True):
        st.markdown(
            """
            Variables: 
            - FS = Fuel Spent without system 
            - SF = Startup Factor 
            - MOIV = Miles to overcome inertia of vehicle 
            - MPG = MPG of vehicle 
            - STOPS = Number of stops 
            - DISTANCE = Total miles traveled 
            - FSS = Fuel Spent with system 
            - E = efficiency of system 
            - FE = Fuel Efficiency 
            - SAVED = Fuel Saved 
            - PS = Potential Savings per vehicle 
            - PSN = Potential Savings Nationally 
            - DPG = Diesel prices per gallon 
            """
            )

        st.image('Calculations.png', caption='Calculations')
    with st.container(border=True):
        st.image("HandDrawing.png", caption = "Hand drawing of circuit")
        st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                padding-left:40px;
            }
            </style>
            ''', unsafe_allow_html=True)

 
# Close the database connection
conn.close()
