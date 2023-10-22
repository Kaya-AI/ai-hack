import plotly.graph_objects as go
import pandas as pd
import streamlit as st

avatar = open("avatar.txt", "r")
avatarURL = avatar.read()
avatar.close()

user = open("user.txt", "r")
userURL = user.read()
user.close()

# Read the data
data = pd.read_csv("last-month.csv") # This is just last month for testing, use permits-2020-onwards.csv for since 2020

mapbox_access_token = "pk.eyJ1Ijoicm9sYW5kZ2F2cmlsZXNjdSIsImEiOiJjajl6a2RiOXQ4c2xzMndzNDhkaWZpb3V6In0.7U26AzhPUHIYO_rfRZZReA"

# Make the figures
fig = go.Figure(go.Scattermapbox(
  lat=data["LATITUDE"],
  lon=data["LONGITUDE"],
  mode='markers',
  marker=go.scattermapbox.Marker(
    size=3,
    opacity=0.6
  ),
  hovertext=data["ADDRESS"]
))

fig.update_layout(
  hovermode='closest',
  mapbox=dict(
    accesstoken=mapbox_access_token,
    bearing=0,
    center=go.layout.mapbox.Center(
      lat=40.730610,
      lon=-73.935242
    ),
    pitch=0,
    zoom=10
  )
)

from dash import Input, Output, State, Dash, dcc, html
from dash.exceptions import PreventUpdate
import dash_chat_components as dch
import math, time

import ask_ai

st.title("Kaya")

st.plotly_chart(fig)

if "messages" not in st.session_state:
  st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter a message"):
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})
  # Display user message in chat message container
  with st.chat_message("user"):
    st.markdown(prompt)
  # Display assistant response in chat message container
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.text("Thinking...")
    ai_message = ask_ai.ask_agent(prompt)
    message_placeholder.markdown(ai_message)
  st.session_state.messages.append({"role": "assistant", "content": ai_message})