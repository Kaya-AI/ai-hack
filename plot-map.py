import plotly.graph_objects as go
import pandas as pd

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
  )
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

# Use Dash to display on a website
app = Dash(
  external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
  ]
)
app.layout = html.Div([
  dcc.Graph(figure=fig, id="permits-map", style={'width': '90vw', 'height': '65vh'}),
  dch.ChatSimple(
    messages=[
      {
        "direction": "recieved",
        "avatar": avatarURL,
        "content": "What would you like help with?",
        "timestamp": int(math.floor(time.time() * 1000))
      }
    ],
    id="chatbot",
    style = {"margin": "20px auto", "maxWidth": "900px", "border": "2px solid red"},
    avatarOutgoing = userURL
  )
])

@app.callback(
  Output("chatbot", "messages"),
  Input("chatbot", "value_on_submit"),
  State("chatbot", "messages"),
  prevent_initial_call=True
)
def reply_message(value_on_submit, msg_list):
  msg_list.append(
    {
      "direction": "recieved",
      "avatar": avatarURL,
      "content": ask_ai.agent.run(value_on_submit),
      "timestamp": int(math.floor(time.time() * 1000))
    }
  )

  return msg_list

app.run_server(debug=True)