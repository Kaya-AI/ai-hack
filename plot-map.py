import plotly.graph_objects as go
import pandas as pd

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


from dash import Dash, dcc, html

# Use Dash to display on a website
app = Dash()
app.layout = html.Div([
  dcc.Graph(figure=fig, id="permits-map", style={'width': '90vw', 'height': '90vh'})
])

app.run_server(debug=True)