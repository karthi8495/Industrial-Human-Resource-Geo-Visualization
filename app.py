import streamlit as st
import pandas as pd
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title= "HRM",layout= "wide", initial_sidebar_state= "expanded",
                   menu_items={'About': """# This Flat Resale page is created by *Prabakaran!"""})
st.markdown("<h1 style='text-align: center; color: Red;'>Industrial Human Resource Geo-Visualization</h1>", unsafe_allow_html=True)


data = pd.read_csv("D:\\GUVI AI & ML\\Capstoneproject5_Placement_Projects\\Code\\final_file_hr.csv")

unique_states = sorted(data['State'].unique())
selected_state = st.sidebar.selectbox("Select State", unique_states, key="state_selector_unique")

filtered_districts = sorted(data[data['State'] == selected_state]['District'].unique())
selected_district = st.sidebar.selectbox("Select District", filtered_districts, key="district_selector_unique")

state_data = data[(data['State'] == selected_state)]
district_data = data[(data['District'] == selected_district)]

st.write(f"Showing data for {selected_state} - {selected_district}")

total_state_workers = state_data['MainWorkersTotalPersons'].sum()
st.write(f"Total number of state workers: {total_state_workers}")
total_district_workers = district_data['MainWorkersTotalPersons'].sum()
st.write(f"Total number of district workers: {total_district_workers}")

st.subheader("Data Summary")
st.write(data.describe())




filtered_nic_names = data[data['District'] == selected_district]['NICName'].unique()
filtered_nic_names = [nic.replace('[', '').replace(']', '').replace("'", "") for nic in filtered_nic_names]
filtered_nic_names = [nic.capitalize() for nic in filtered_nic_names]
filtered_nic_names = sorted(filtered_nic_names)

selected_nic_name = st.sidebar.selectbox("Select NIC Name", filtered_nic_names, key="nic_name_selector")




# Plotting data for Rural, Main, and Urban workers
rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

rural_data = data[rural_cols].sum().values
main_data = data[['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']].iloc[0].values
urban_data = data[urban_cols].sum().values

fig, ax = plt.subplots(figsize=(10, 6))
x_labels = ['Rural', 'Main', 'Urban']
ax.bar(x_labels, rural_data, color='#7C00FE', label='Rural')
ax.bar(x_labels, main_data, bottom=rural_data, color='#F9E400', label='Main')
ax.bar(x_labels, urban_data, bottom=rural_data + main_data, color='#F5004F', label='Urban')
ax.set_title(f"{selected_state} - {selected_district} - Workers Distribution")
ax.legend()
st.pyplot(fig)




# Plotting data for Marginal workers (using pie chart)
marginal_cols_rural = ['MarginalWorkersRuralPersons', 'MarginalWorkersRuralMales', 'MarginalWorkersRuralFemales']
marginal_cols_urban = ['MarginalWorkersUrbanPersons', 'MarginalWorkersUrbanMales', 'MarginalWorkersUrbanFemales']

marginal_data_rural = data[marginal_cols_rural].sum().values
marginal_data_urban = data[marginal_cols_urban].sum().values

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(marginal_data_rural, labels=marginal_cols_rural, autopct='%1.1f%%', startangle=90, colors=['#7C00FE', '#F9E400', '#F5004F'])
ax.set_title(f"{selected_state} - {selected_district} - Rural Marginal Workers Distribution")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(marginal_data_urban, labels=marginal_cols_urban, autopct='%1.1f%%', startangle=90, colors=['#7C00FE', '#F9E400', '#F5004F'])
ax.set_title(f"{selected_state} - {selected_district} - Urban Marginal Workers Distribution")
st.pyplot(fig)



import plotly.express as px

# Filterd data for Main, Rural, and Urban workers
main_cols = ['MainWorkersTotalPersons', 'MainWorkersTotalMales', 'MainWorkersTotalFemales']
rural_cols = ['MainWorkersRuralPersons', 'MainWorkersRuralMales', 'MainWorkersRuralFemales']
urban_cols = ['MainWorkersUrbanPersons', 'MainWorkersUrbanMales', 'MainWorkersUrbanFemales']

main_data = data[['State'] + main_cols].groupby('State').sum().reset_index()
rural_data = data[['State'] + rural_cols].groupby('State').sum().reset_index()
urban_data = data[['State'] + urban_cols].groupby('State').sum().reset_index()

# Melt the data to have a single column for worker type and another for the count
main_data_melted = main_data.melt(id_vars='State', var_name='WorkerType', value_name='Count')

# Plotting the differences in counts
fig = px.bar(main_data_melted, x='State', y='Count', color='WorkerType', 
             title='Differences in Main, Rural, and Urban Workers Counts (State-wise)',
             labels={'Count': 'Total Workers Count'},
             color_discrete_sequence=['#7C00FE', '#F9E400', '#F5004F'],
             template='plotly_white')

# Update the layout for better visualization
fig.update_layout(barmode='group', xaxis_title='State', yaxis_title='Total Workers Count (Log Scale)',
                  showlegend=True, yaxis_type="log")

# Display the chart
st.plotly_chart(fig)



# Geo-Map Visualization
data = pd.read_csv("D:\\GUVI AI & ML\\Capstoneproject5_Placement_Projects\\Code\\final_file_hr.csv")

state_data = data[(data['State'] == selected_state)]
district_data = data[(data['District'] == selected_district)]

folium_map = folium.Map(location=[28.6139, 77.2090], zoom_start=5)

marker_cluster = MarkerCluster().add_to(folium_map)

for idx, row in state_data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    total_workers = row['MainWorkersTotalPersons']
    male_female_ratio = row['MaleFemaleRatio']
    popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
    folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

for idx, row in district_data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    total_workers = row['MainWorkersTotalPersons']
    male_female_ratio = row['MaleFemaleRatio']
    popup_text = f"State: {selected_state}<br>District: {selected_district}<br>Total Workers: {total_workers}<br>Male-Female Ratio: {male_female_ratio}"
    folium.Marker([lat, lon], popup=popup_text).add_to(marker_cluster)

st.components.v1.html(folium_map._repr_html_(), width=1200, height=500)
