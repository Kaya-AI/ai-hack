import pandas
import plotly.graph_objects as go

data = pandas.read_csv("permits-2020-onwards.csv")
types = []
values = []

for i in data.columns:
    types.append(i)
for i in data.columns:
    values.append(data[i][:100])

fig = go.Figure(data=[go.Table(header=dict(values=types),
                 cells=dict(values=values))
                     ])
fig.update_layout(width=7000)
fig.show()