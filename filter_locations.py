import pandas

data = pandas.read_csv("permits-2020-onwards.csv")
coordinates = data[["LATITUDE", "LONGITUDE"]]
coordinates_list = []

for i in coordinates.iterrows():
    coordinates_list.append((i[1][0], i[1][1]))