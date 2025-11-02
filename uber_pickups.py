import streamlit as st
import pandas as pd
import numpy as np

st.title('Starbucks visualize')

DATE_COLUMN = 'date/time'
DATA_URL = 'https://raw.githubusercontent.com/YingphanH/my_streamlit/main/directory.csv'

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)



#st.subheader('Number of pickups by hour')
#hist_values = np.histogram(
    #data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

#st.bar_chart(hist_values)

#hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#st.subheader(f'Map of all pickups at {hour_to_filter}:00')

#st.map(filtered_data)

# Convert columns to numeric (in case they are strings)
data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

# Drop rows where lat/lon are missing or invalid
data = data.dropna(subset=['latitude', 'longitude'])

st.sidebar.header("Filter Options")

ownership_options = sorted(data['ownership type'].dropna().unique())

selected_ownership = st.sidebar.multiselect(
    "Select ownership types to display:",
    options=ownership_options,
    default=ownership_options  # show all by default
)

# Filter data based on selection
filtered_data = data[data['ownership type'].isin(selected_ownership)]

st.write(f"### Showing {len(filtered_data)} stores ({', '.join(selected_ownership)})")

# --- Map visualization ---
st.subheader("📍 Store Locations on Map")
st.map(filtered_data, latitude='latitude', longitude='longitude')

# Optional: table of filtered data
with st.expander("See filtered data table"):
    st.dataframe(filtered_data)















