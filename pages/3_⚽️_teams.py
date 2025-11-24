import streamlit as st
import requests
import base64

st.set_page_config(
    page_title="Players",
    page_icon="🏃🏼",
    layout="wide"
)

@st.cache_data
def load_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    req = requests.get(url, headers=headers)
    return req.content 

def load_image_base64(url):
    img_bytes = load_image(url)
    return "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode()

df_data = st.session_state["data"]

clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = df_data[(df_data["Club"] == club)].set_index("Name")

df_filtered["Photo"] = df_filtered["Photo"].apply(load_image_base64)
df_filtered["Flag"] = df_filtered["Flag"].apply(load_image_base64)

st.image(load_image(df_filtered.iloc[0]["Club Logo"]))
st.markdown(f"## {club}")

columns = ["Age", "Photo", "Flag", "Overall", 'Value(£)', 'Wage(£)', 'Joined', 
            'Height(cm.)', 'Weight(lbs.)',
            'Contract Valid Until', 'Release Clause(£)']

st.dataframe(
    df_filtered[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall", format="%d", min_value=0, max_value=100
        ),
        "Wage(£)": st.column_config.ProgressColumn(
            "Weekly Wage", format="£%f",
            min_value=0, max_value=df_filtered["Wage(£)"].max()
        ),
        "Photo": st.column_config.ImageColumn("Photo"),
        "Flag": st.column_config.ImageColumn("Country"),
    }
)
