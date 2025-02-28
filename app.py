import streamlit as st
import pandas as pd
from my_main_upd import *

key_input = st.sidebar.text_input("Ключевые слова:")
sort_select = st.sidebar.selectbox("Сортировка:", 
                     options = {"Сначала дешевле" : " Сначала дешевле ", 
                                "Сначала дороже" : " Сначала дороже ",
                                "Сначала новые" : " Сначала новые ",
                                "По релевантности" : " По релевантности ",
                                "По популярности" : " По популярности "})

st.markdown("**Добро пожаловать!**")
st.markdown("Здесь будут результаты Вашего поиска!")

button = st.sidebar.button("Поехали!", key = "btn_scrape")

if st.session_state.get("btn_scrape"):
    df = scrape_to_table(key_input, sort_select)
    data_to_show = df[["title", "price"]].head(5)
    st.table(data_to_show) # dataframe
    
    col1, col2, col3 = st.columns(3)

    with col1:
        img1 = df.loc[0, "image_link"]
        st.image(img1)

    with col2:
        img2 = df.loc[1, "image_link"]
        st.image(img2)

    with col3:
        img3 = df.loc[2, "image_link"]
        st.image(img3)


