import streamlit as st
import pandas as pd

st.title("☕ Starbucks Store Visualizer")

DATA_URL = 'https://raw.githubusercontent.com/YingphanH/my_streamlit/main/directory.csv'

@st.cache_data
def load_data(nrows=None):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# --- Load and clean data ---
data = load_data()
data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
data = data.dropna(subset=['latitude', 'longitude'])

st.sidebar.header("Filter Options")

# --- Country Filter ---
countries = sorted(data['country'].dropna().unique())
select_all_countries = st.sidebar.checkbox("Select all countries", value=True)

if select_all_countries:
    selected_countries = countries
else:
    selected_countries = st.sidebar.multiselect(
        "🌍 Select country/countries:",
        options=countries,
        default=[]
    )

# --- Ownership Type Filter ---
ownership_options = sorted(data['ownership type'].dropna().unique())
select_all_ownership = st.sidebar.checkbox("Select all ownership types", value=True)

if select_all_ownership:
    selected_ownership = ownership_options
else:
    selected_ownership = st.sidebar.multiselect(
        "🏢 Select ownership types:",
        options=ownership_options,
        default=[]
    )

# --- Apply Filters ---
filtered_data = data[
    (data['country'].isin(selected_countries)) &
    (data['ownership type'].isin(selected_ownership))
]

st.metric("Number of Starbucks locations", len(filtered_data))

]

st.write(
    f"### Showing {len(filtered_data)} stores "
    f"in {', '.join(selected_countries[:3]) + ('...' if len(selected_countries) > 3 else '')} "
    f"for ownership types: {', '.join(selected_ownership)}"
)

# --- Map Visualization ---
st.subheader("📍 Store Locations on Map")
st.map(filtered_data, latitude='latitude', longitude='longitude')
st.metric("Number of Starbucks locations", len(filtered_data))

# --- Optional: View Filtered Table ---
with st.expander("🔎 View filtered data table"):
    st.dataframe(filtered_data)


