from st_aggrid import AgGrid
import pandas

data = pandas.read_csv("test.csv")

AgGrid(data)