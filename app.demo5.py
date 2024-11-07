#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

# Load the saved model
model = joblib.load('/Altamash/Excelr code/PROJECTS/PROJECT_ ENERGY_PRODUCTION/energy_model.pkl')

# Set page configuration
st.set_page_config(page_title="Energy Production Predictor", page_icon="⚡", layout="centered")

# Set background image using HTML/CSS styling
def set_background_image(image_url):
    page_bg_img = f'''
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url({image_url});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
    }}
    h1, h2, h3, h4, h5, h6, p {{
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call the function to set background image (New background URL)
set_background_image("https://wallpapersmug.com/download/1366x768/46b360/lake-night-huts-lanterns.jpg")

# Title of the app with color and header
st.markdown("<h1 style='text-align: center;'>⚡ Energy Production Prediction App ⚡</h1>", unsafe_allow_html=True)

# Instructions with white text
st.markdown("""
### <span style='color:white;'>🌡️ Predict energy production based on the following inputs:</span>
- <span style='color:white;'>**Temperature (T)**: Impact of environmental temperature on energy production.</span>
- <span style='color:white;'>**Exhaust Vacuum (V)**: Effect of exhaust vacuum on the system.</span>
- <span style='color:white;'>**Ambient Pressure (AP)**: Ambient pressure's role in energy production.</span>
- <span style='color:white;'>**Relative Humidity (RH)**: Influence of humidity levels on efficiency.</span>
""", unsafe_allow_html=True)

# Create input fields in the sidebar
st.sidebar.header("Input Parameters")
temp = st.sidebar.number_input('🌡️ Temperature (°C)', min_value=-50.0, max_value=100.0, value=25.0)
vac = st.sidebar.number_input('🌀 Exhaust Vacuum (cm Hg)', min_value=0.0, max_value=100.0, value=50.0)
ap = st.sidebar.number_input('🌬️ Ambient Pressure (mbar)', min_value=0.0, max_value=1100.0, value=1013.0)
rh = st.sidebar.number_input('💧 Relative Humidity (%)', min_value=0.0, max_value=100.0, value=50.0)

# Add a button for prediction
if st.button('Predict Energy Production'):
    # Create input array for prediction
    input_data = np.array([[temp, vac, ap, rh]])
    
    # Perform the prediction using the loaded model
    prediction = model.predict(input_data)[0]

    # Display the prediction result with a nice card effect
    st.markdown(f"""
        <div style="background-color:rgba(255, 255, 255, 0.8);padding:10px;border-radius:10px;text-align:center;">
            <h2>🔋 Predicted Energy Production: <span style='color:green;'>{prediction:.2f} MW</span></h2>
        </div>
    """, unsafe_allow_html=True)

    # Plotting inputs vs predicted energy output using Plotly (updated, more attractive graph)
    factors = ['Temperature', 'Exhaust Vacuum', 'Ambient Pressure', 'Relative Humidity']
    values = [temp, vac, ap, rh]
    
    # Use a radial bar chart for a more visually appealing representation
    fig = go.Figure(go.Barpolar(
        r=values,
        theta=factors,
        marker=dict(color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']),
        name='Input Values'
    ))
    
    fig.update_layout(
        title='Input Factor Values',
        font_size=16,
        polar=dict(
            radialaxis=dict(range=[0, 100], visible=True),
            angularaxis=dict(tickfont=dict(size=12))
        ),
        showlegend=False
    )
    st.plotly_chart(fig)

    # Progress bar style chart for energy production
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        title={'text': "Energy Production (MW)", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [None, max(200, prediction * 1.5)], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "green"},
            'bgcolor': "lightgray",
            'borderwidth': 2,
            'bordercolor': "gray",
        }
    ))

    st.plotly_chart(gauge_fig)
    
# Footer
st.markdown("<h4 style='color:white;text-align:center;'>Powered by Machine Learning ⚙️</h4>", unsafe_allow_html=True)


# In[ ]:




