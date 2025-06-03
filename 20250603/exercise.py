import folium

# 模擬站點資料
stops = [
    {"順序": 1, "站名": "出發站A", "lat": 25.0330, "lon": 121.5654},
    {"順序": 2, "站名": "站B", "lat": 25.0350, "lon": 121.5700},
    {"順序": 3, "站名": "站C", "lat": 25.0400, "lon": 121.5750},
    {"順序": 4, "站名": "終點站D", "lat": 25.0450, "lon": 121.5800},
]

# 建立地圖，中心點選在第一站附近
m = folium.Map(location=[25.0330, 121.5654], zoom_start=14)

# 用線連結站點經緯度
line_coords = [(stop["lat"], stop["lon"]) for stop in stops]
folium.PolyLine(line_coords, color="blue", weight=5, opacity=0.7).add_to(m)

# 標記每個站點，出發站用綠色，終點站用紅色，其餘用藍色
for stop in stops:
    color = "blue"
    if stop["順序"] == 1:
        color = "green"
    elif stop["順序"] == len(stops):
        color = "red"
    folium.CircleMarker(
        location=(stop["lat"], stop["lon"]),
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f'{stop["順序"]}. {stop["站名"]}'
    ).add_to(m)

# 儲存為 HTML 檔
m.save("/mnt/data/demo_direct_bus_route.html")
print("互動地圖已儲存為 demo_direct_bus_route.html")
