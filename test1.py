import streamlit as st
st.write("hello there!")
color = st.color_picker('Pick A Color', '#00565D')
st.write('The current color is', color)

d = st.date_input(
     "When's your birthday",
     datetime.date(2019, 7, 6))
st.write('Your birthday is:', d)
