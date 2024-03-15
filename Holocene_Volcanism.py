import folium
import pandas
import openpyxl

#Wczytujemy dane z pliku tekstowego za pomoca pandasa
data = pandas.read_excel(r"C:\Users\Mateusz\OneDrive\Desktop\Python Project 1\Holocene.xlsx")
#data = pandas.read_csv(r"C:\Users\Mateusz\OneDrive\Desktop\Python Project 1\Holocene.csv", on_bad_lines="skip")

#"Bierzemy" kolumny LAT i LON, nazywamy je lat i lon
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
nam = list(data["NAME"])
#pop = list(data["POP2005"])

def color_producer(el):
    if elevation < 0:
        return "blue"
    elif 0 <= elevation < 1000:
        return "green"
    elif 1000 <= elevation < 2000:
        return "orange"
    else:
        return "red"
    
#def population_number(pop):
    #if population <


html = """
Volcano Name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

#Robimy mape, startuje ona od naszego domu
map = folium.Map(
    location=[50.284423552013294, 18.881675711624098],
    zoom_start = 5)

#Custom Ikony - Nie dzialaj kiedy jest ich wiecej
#icon = folium.features.CustomIcon("https://icons.iconarchive.com/icons/icons8/halloween/256/spider-icon.png", icon_size=(24,24))

#Robimy feature group, czyli smietniczek do ktorego bedziemy dodawali ikonki
feature_group_Volcanos = folium.FeatureGroup(name="Volcanos") 

#Tutaj loop, gdzie dla latitue i longitute (nazwy wymyslone) w funkcji zipnietej zczytujacej dane lat i lon, dodajemy markery dla lat i long osobno
for latitude, longitude, elevation, name in zip(lat, lon, elev, nam):
    iframe = folium.IFrame(html=html % (name, name, elevation), width=200, height=100)
    feature_group_Volcanos.add_child(folium.CircleMarker(location=[latitude, longitude], radius = 6, popup = folium.Popup(iframe),
    fill_color = color_producer(elevation), color="black", weight= 0.5, fill_opacity = 1.0))


#I do smietniczka laduja smieci tj. add_child

feature_group_Population = folium.FeatureGroup(name="Population")
#Tu dodajemy "obwódkę" do mapy, która dzieli to na kraje
feature_group_Population.add_child(folium.GeoJson(data=open("world.json", "r", encoding='utf-8-sig').read(),
style_function=lambda x: {
    "fillColor": "green" if x["properties"]["POP2005"] < 10000000
                          else "orange" if 10000000 <= x["properties"]["POP2005"] < 40000000
                          else "red",
                         "color" : "black", "weight": 0.5}))

map.add_child(feature_group_Population)
map.add_child(feature_group_Volcanos)
map.add_child(folium.LayerControl())

#I ze smietniczka smieci wysypujemy do mapy dodajac do mapy
map.save("HoloceneVolcanic_Map.html")
