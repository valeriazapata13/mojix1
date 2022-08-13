import streamlit as st
st.write("hello there!")
color = st.color_picker('Pick A Color', '#00565D')
st.write('The current color is', color)

st.balloons()

image = Image.open('image.jpg')
st.image(image, caption='schnauzer mini')

