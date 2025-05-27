# ✅ 小羅公車通 · 公車代碼總抓器 + 詳細站點擷取器 + 路線WKT轉GeoPackage（台北 eBus）

import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import time
import geopandas as gpd
from playwright.sync_api import sync_playwright

# 先抓所有路線清單（route_id + route_name）
def fetch_route_list():
    url = "https://ebus.gov.taipei/Routes"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    routes = []
    for a in soup.select("a[href^='/Route/StopsOfRoute']"):
        name = a.get_text(strip=True)
        href = a['href']
        route_id = href.split('=')[-1]
        routes.append({"id": route_id, "name": name})
    with open("routes_list.json", "w", encoding="utf-8") as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)
    print(f"✅ 共取得 {len(routes)} 條公車路線，已儲存為 routes_list.json")
    return routes

# 擷取站牌資訊（可略過，保留用於未來）
def fetch_route_stops(route_id, route_name, direction="go"):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        if direction == "come":
            try:
                page.click('a.stationlist-come-go-gray.stationlist-come')
                page.wait_for_timeout(1000)
            except:
                pass
        page.wait_for_timeout(1500)
        content = page.content()
        browser.close()

    # 解析 HTML 中的站牌資訊
    pattern = re.compile(
        r'<li>.*?<span class="auto-list-stationlist-position.*?">(.*?)</span>\s*'
        r'<span class="auto-list-stationlist-number">\s*(\d+)</span>\s*'
        r'<span class="auto-list-stationlist-place">(.*?)</span>.*?'
        r'<input[^>]+name="item\\.UniStopId"[^>]+value="(\d+)"[^>]*>.*?'
        r'<input[^>]+name="item\\.Latitude"[^>]+value="([\d\.]+)"[^>]*>.*?'
        r'<input[^>]+name="item\\.Longitude"[^>]+value="([\d\.]+)"[^>]*>',
        re.DOTALL
    )

    matches = pattern.findall(content)
    if not matches:
        print(f"⚠️ 找不到 {route_name} 的站牌資料，略過")
        return []

    stops = []
    for arrival, number, name, sid, lat, lon in matches:
        stops.append({
            "route_id": route_id,
            "route_name": route_name,
            "stop_number": int(number),
            "stop_name": name,
            "stop_id": sid,
            "lat": float(lat),
            "lon": float(lon),
            "direction": direction
        })

    print(f"✅ {route_name} ({direction}) 共 {len(stops)} 站")
    return stops

# 擷取路線的 WKT 線段（從 HTML embedded json 中取出）
def fetch_route_wkt(route_id, route_name):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(2000)
        content = page.content()
        browser.close()

    pattern = r'JSON\.stringify\s*\(\s*(\{[\s\S]*?\})\s*\)'
    match = re.search(pattern, content)
    if not match:
        print(f"❌ 無法取得 {route_name} 的 WKT json，略過")
        return pd.DataFrame()

    json_dict = json.loads(match.group(1))
    wkts = {k: v for k, v in json_dict.items() if k.startswith("wkt")}

    df = pd.DataFrame(wkts.items(), columns=["wkt_id", "wkt_string"])
    df["route_id"] = route_id
    df["route_name"] = route_name
    df["geometry"] = gpd.GeoSeries.from_wkt(df["wkt_string"])
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    return gdf

if __name__ == "__main__":
    all_routes = fetch_route_list()
    geo_df = gpd.GeoDataFrame()

    for route in all_routes:
        try:
            gdf = fetch_route_wkt(route_id=route["id"], route_name=route["name"])
            if not gdf.empty:
                geo_df = pd.concat([geo_df, gdf], ignore_index=True)
        except Exception as e:
            print(f"❌ {route['name']} 失敗：{e}")
        time.sleep(1)

    geo_df.to_file("ebus_taipei_routes.gpkg", layer="data_routes_wkt", driver="GPKG")
    print(f"📦 所有路線圖資已儲存，共 {len(geo_df)} 筆 WKT。")
